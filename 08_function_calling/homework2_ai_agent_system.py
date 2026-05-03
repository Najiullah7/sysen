#!/usr/bin/env python
# homework2_ai_agent_system.py
# Homework 2: Integrated AI Agent System (Labs 6, 7, and 8)
# Pairs with HOMEWORK2.md
# Tim Fraser
#
# This script combines:
# - LAB 6: multi-agent orchestration (2-3 agents with distinct roles)
# - LAB 7: custom RAG retrieval from a project-specific CSV
# - LAB 8: function calling tools for data/API interaction

# 0. SETUP ###################################

## 0.1 Load Packages #################################

import json  # for serializing context payloads between agents
import re  # for tokenizing search queries
import requests  # for API requests in custom tools
import pandas as pd  # for working with tabular retrieval data
import functions as tool_runtime  # runtime module where tool names are resolved

# Load helper wrappers from this module
from functions import agent_run, df_as_text

## 0.2 Configuration #################################

MODEL = "smollm2:1.7b"
COURSE_DATA = "07_rag/data/course_resources.csv"


# 1. DEFINE TOOL FUNCTIONS ###################################

def search_course_resources(query, top_n=5, document=COURSE_DATA):
    """
    Search course resources with simple keyword + phrase matching.
    Returns list[dict] so downstream agents can consume structured context.
    """

    # Read the source and normalize user query
    df = pd.read_csv(document)
    query_clean = str(query).strip().lower()
    query_tokens = [tok for tok in re.findall(r"[a-z0-9]+", query_clean) if len(tok) >= 3]

    # Match across core columns used in LAB 7
    searchable_columns = ["title", "category", "difficulty", "keywords", "content"]
    mask = pd.Series(False, index=df.index)

    for column in searchable_columns:
        col = df[column].fillna("").str.lower()
        col_mask = col.str.contains(query_clean, regex=False)
        for token in query_tokens:
            col_mask = col_mask | col.str.contains(token, regex=False)
        mask = mask | col_mask

    # Keep a small set of relevant fields for cleaner agent prompts
    results = (df[mask]
               .head(int(top_n))
               .filter(items=["id", "title", "category", "difficulty", "keywords", "content"]))
    return results.to_dict(orient="records")


def fetch_openalex_evidence(topic="systems engineering", per_page=5):
    """
    Pull lightweight evidence from the OpenAlex Works API (public endpoint).
    Returns a compact list of recent works to support final recommendations.
    """

    # OpenAlex search endpoint (no API key required for basic use)
    url = "https://api.openalex.org/works"
    params = {
        "search": topic,
        "per-page": int(per_page),
        "sort": "publication_year:desc"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()

    # Keep only fields needed for analysis
    records = []
    for item in payload.get("results", []):
        records.append({
            "title": item.get("display_name", ""),
            "publication_year": item.get("publication_year", ""),
            "cited_by_count": item.get("cited_by_count", 0),
            "doi": item.get("doi", "")
        })
    return records


# Register tool functions into the runtime used by functions.agent()
tool_runtime.search_course_resources = search_course_resources
tool_runtime.fetch_openalex_evidence = fetch_openalex_evidence


# 2. TOOL METADATA ###################################

tool_search_resources = {
    "type": "function",
    "function": {
        "name": "search_course_resources",
        "description": "Search the local course resources CSV for RAG context relevant to a user question.",
        "parameters": {
            "type": "object",
            "required": ["query", "top_n"],
            "properties": {
                "query": {"type": "string", "description": "User question or topic keywords."},
                "top_n": {"type": "number", "description": "Maximum number of records to return."},
                "document": {"type": "string", "description": "Optional CSV path."}
            }
        }
    }
}

tool_openalex = {
    "type": "function",
    "function": {
        "name": "fetch_openalex_evidence",
        "description": "Get recent scholarly evidence related to a topic from OpenAlex.",
        "parameters": {
            "type": "object",
            "required": ["topic", "per_page"],
            "properties": {
                "topic": {"type": "string", "description": "Topic or search phrase."},
                "per_page": {"type": "number", "description": "Number of papers to fetch."}
            }
        }
    }
}


# 3. MULTI-AGENT ORCHESTRATION ###################################

def extract_first_tool_output(tool_result):
    """Extract tool output from agent_run(..., output='tools') result."""
    if isinstance(tool_result, list) and len(tool_result) > 0:
        return tool_result[0].get("output", [])
    return []


def resolve_tool_or_fallback(tool_result, fallback_fn, fallback_kwargs):
    """
    Return tool output when present; otherwise run deterministic fallback function.
    This covers cases where the model responds with text instead of a tool call.
    """
    extracted = extract_first_tool_output(tool_result)
    if isinstance(extracted, list) and len(extracted) > 0:
        return extracted, False
    return fallback_fn(**fallback_kwargs), True


def deterministic_analysis(rag_rows, evidence_rows):
    """Fallback analysis when Ollama is unavailable."""
    rag_df = pd.DataFrame(rag_rows)
    evidence_df = pd.DataFrame(evidence_rows)

    rag_count = len(rag_df)
    evidence_count = len(evidence_df)
    top_categories = (rag_df["category"].value_counts().head(3).to_dict()
                      if "category" in rag_df.columns else {})

    return (
        "## Deterministic Analysis (Fallback)\n"
        f"- Retrieved {rag_count} local RAG records from the course dataset.\n"
        f"- Retrieved {evidence_count} external evidence records from OpenAlex.\n"
        f"- Most frequent local categories: {top_categories if top_categories else 'N/A'}.\n"
        "- Recommended direction: combine local course guidance with recent external evidence.\n"
    )


def deterministic_report(question, rag_rows, evidence_rows):
    """Fallback report when Ollama is unavailable."""
    rag_titles = [row.get("title", "") for row in rag_rows[:3]]
    paper_titles = [row.get("title", "") for row in evidence_rows[:3]]
    return (
        "# Integrated Recommendation Report (Fallback)\n\n"
        f"Question: {question}\n\n"
        "## Recommendation Summary\n"
        "Use a human-in-the-loop workflow that combines simulation risk analysis, structured prompt "
        "evaluation, and clear safety checks before operational decisions.\n\n"
        "## Retrieved Local Context\n"
        + "\n".join([f"- {title}" for title in rag_titles]) + "\n\n"
        "## External Evidence Sample\n"
        + "\n".join([f"- {title}" for title in paper_titles]) + "\n\n"
        "## Caution\n"
        "Do not deploy recommendations without independent validation and a documented review checkpoint."
    )


def prompt_user_question():
    """
    Ask the user for a question in the terminal.
    If the user presses Enter, use a default question.
    """
    default_question = "How can I build a safer AI-enabled decision workflow for systems engineering teams?"
    print("Enter your question for the multi-agent system.")
    user_input = input("Question (press Enter to use default): ").strip()
    if user_input == "":
        return default_question
    return user_input


# User question driving the full pipeline (interactive terminal input)
user_question = prompt_user_question()

# Agent 1A: Retrieval agent calls local RAG tool
role1a = (
    "You are a retrieval agent. Always call search_course_resources to gather local CSV context. "
    "Return only tool output."
)
task1a = (
    f"Find RAG context for this question with top_n=5: {user_question}"
)

# Agent 1B: Evidence agent calls API tool
role1b = (
    "You are an evidence scout. Always call fetch_openalex_evidence to gather recent external evidence. "
    "Return only tool output."
)
task1b = "Fetch 5 recent OpenAlex works for topic 'systems engineering risk'."

# Agent 2: Analyst combines both retrieved contexts
role2 = (
    "You are a systems engineering analyst. Use only the provided JSON context. "
    "Write concise markdown with: "
    "1) what local course data suggests, "
    "2) what external evidence adds, and "
    "3) two practical design recommendations."
)

# Agent 3: Reporter produces final stakeholder-ready output
role3 = (
    "You are a technical report writer. Produce a short markdown report with sections: "
    "Recommendation Summary, Implementation Steps (3 bullets), and Caution."
)

# Execute pipeline with robust fallbacks
fallback_mode = False
try:
    agent1a_raw = agent_run(role=role1a, task=task1a, tools=[tool_search_resources], output="tools", model=MODEL)
    rag_records, used_fallback = resolve_tool_or_fallback(
        tool_result=agent1a_raw,
        fallback_fn=search_course_resources,
        fallback_kwargs={"query": user_question, "top_n": 5}
    )
    fallback_mode = fallback_mode or used_fallback
except Exception as error:
    print(f"Tool-calling fallback for local retrieval: {error}")
    rag_records = search_course_resources(query=user_question, top_n=5)
    fallback_mode = True

try:
    agent1b_raw = agent_run(role=role1b, task=task1b, tools=[tool_openalex], output="tools", model=MODEL)
    evidence_records, used_fallback = resolve_tool_or_fallback(
        tool_result=agent1b_raw,
        fallback_fn=fetch_openalex_evidence,
        fallback_kwargs={"topic": "systems engineering risk", "per_page": 5}
    )
    fallback_mode = fallback_mode or used_fallback
except Exception as error:
    print(f"Tool-calling fallback for API retrieval: {error}")
    try:
        evidence_records = fetch_openalex_evidence(topic="systems engineering risk", per_page=5)
    except Exception as api_error:
        print(f"API retrieval failed: {api_error}")
        evidence_records = []
    fallback_mode = True

# Build shared context for Agent 2
combined_context = {
    "question": user_question,
    "local_rag_results": rag_records,
    "openalex_results": evidence_records
}
combined_context_text = json.dumps(combined_context, indent=2)

try:
    analysis = agent_run(role=role2, task=combined_context_text, output="text", model=MODEL)
except Exception as error:
    print(f"Analyst fallback: {error}")
    analysis = deterministic_analysis(rag_records, evidence_records)
    fallback_mode = True

try:
    final_report = agent_run(role=role3, task=analysis, output="text", model=MODEL)
except Exception as error:
    print(f"Reporter fallback: {error}")
    final_report = deterministic_report(user_question, rag_records, evidence_records)
    fallback_mode = True


# 4. VIEW OUTPUTS ###################################

rag_df = pd.DataFrame(rag_records)
evidence_df = pd.DataFrame(evidence_records)

print("===== HOMEWORK 2 INTEGRATED SYSTEM =====")
print(f"Model: {MODEL}")
print(f"Fallback mode used: {fallback_mode}")
print()

print("===== AGENT 1A TOOL OUTPUT (RAG) =====")
if rag_df.empty:
    print("No RAG records found.")
else:
    print(df_as_text(rag_df.head(5)))
print()

print("===== AGENT 1B TOOL OUTPUT (OPENALEX API) =====")
if evidence_df.empty:
    print("No external evidence records found.")
else:
    print(df_as_text(evidence_df.head(5)))
print()

print("===== AGENT 2 ANALYSIS =====")
print(analysis)
print()

print("===== AGENT 3 FINAL REPORT =====")
print(final_report)
