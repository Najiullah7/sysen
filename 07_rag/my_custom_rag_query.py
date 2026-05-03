# my_custom_rag_query.py
# Custom RAG workflow using a course-themed CSV source
# Pairs with LAB_custom_rag_query.md
# Tim Fraser
#
# This script shows a complete custom Retrieval-Augmented Generation (RAG) workflow.
# It creates a domain-specific search over a CSV file, then passes retrieved JSON
# context to an LLM so the response stays grounded in the data.

# 0. SETUP ###################################

## 0.1 Load Packages #################################

import json  # for converting retrieval results to JSON
import re  # for tokenizing user queries into searchable terms
import pandas as pd  # for reading and filtering tabular data

# Load helper function for calling the LLM
from functions import agent_run

## 0.2 Configuration #################################

# Model and host configuration for local Ollama
MODEL = "smollm2:135m"
PORT = 11434
OLLAMA_HOST = f"http://localhost:{PORT}"
DOCUMENT = "07_rag/data/course_resources.csv"


# 1. SEARCH FUNCTION ###################################

def search(query, document, top_n=5):
    """
    Search the custom CSV file using keyword matches across key text columns.

    Parameters
    ----------
    query : str
        Search phrase provided by the user.
    document : str
        Path to the CSV document.
    top_n : int
        Maximum number of matched rows to return.

    Returns
    -------
    str
        JSON string with matched records and basic metadata.
    """

    # Read source data and normalize text for case-insensitive matching
    df = pd.read_csv(document)
    query_clean = query.strip().lower()
    query_tokens = [token for token in re.findall(r"[a-z0-9]+", query_clean) if len(token) >= 3]

    # Match query against multiple text fields and tokens to improve recall
    searchable_columns = ["title", "category", "difficulty", "keywords", "content"]
    mask = pd.Series(False, index=df.index)
    for column in searchable_columns:
        column_text = df[column].fillna("").str.lower()
        # Keep full-phrase matching when possible, then expand to token-level matching
        column_mask = column_text.str.contains(query_clean, regex=False)
        for token in query_tokens:
            column_mask = column_mask | column_text.str.contains(token, regex=False)
        mask = mask | column_mask

    # Keep top matches and provide a predictable response format
    matched = df[mask].head(top_n)
    payload = {
        "query": query,
        "match_count": int(matched.shape[0]),
        "results": matched.to_dict(orient="records"),
    }
    return json.dumps(payload, indent=2)


# 2. TEST SEARCH FUNCTION ###################################

print("Testing custom search function...")
test_query = "simulation risk"
test_result = search(test_query, DOCUMENT)
print(test_result)
print()


# 3. RAG WORKFLOW ###################################

# User-style question for the RAG pipeline
user_question = "How can I design a safer simulation-based decision process?"
retrieved_context = search(user_question, DOCUMENT)

# System prompt that tells the model how to use retrieved data
role = (
    "You are a systems engineering assistant. Use ONLY the provided JSON data to answer. "
    "Write 120-180 words in markdown with: "
    "1) a short recommendation summary, "
    "2) three actionable steps, and "
    "3) one caution about overconfidence."
)

try:
    # Generate a grounded response from retrieved records
    result = agent_run(role=role, task=retrieved_context, model=MODEL, output="text")
    print("Generated RAG response:")
    print(result)
except Exception as error:
    # Keep the script informative even if Ollama is not running
    print(f"LLM call failed: {error}")
    print("Start Ollama and try again. Retrieval output above is still valid.")
