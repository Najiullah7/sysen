# 📌 LAB

## Create Your Own RAG AI Query

🕒 *Estimated Time: 30-45 minutes*

---

## 📋 Lab Overview

Create your own data source (text file, CSV, or SQLite database) relevant to your project, implement a search function, and build a complete RAG query workflow. This lab combines data preparation, search function implementation, and LLM integration.

---

## ✅ Your Tasks

### Task 1: Create Your Data Source

- [x] Choose **1 data source type** based on your project needs. Eg:
  - **CSV file selected**: [`course_resources.csv`](data/course_resources.csv) with 10 entries about systems engineering and AI workflows.
- [x] Ensure your data has enough content to make meaningful searches (at least 5-10 items/entries)

### Task 2: Implement Your Search Function

- [x] Choose one of the example scripts as a template:
  - [`02_txt.py`](02_txt.py) or [`02_txt.R`](02_txt.R) for text files
  - [`03_csv.py`](03_csv.py) or [`03_csv.R`](03_csv.R) for CSV files
  - [`04_sqlite.py`](04_sqlite.py) or [`04_sqlite.R`](04_sqlite.R) for SQLite databases
- [x] Adapt the script's search function to match your data structure and needs:
  - Implemented in [`my_custom_rag_query.py`](my_custom_rag_query.py)
  - Search matches query terms across `title`, `category`, `difficulty`, `keywords`, and `content`
  - Returns structured JSON with `query`, `match_count`, and `results`
- [x] Test your search function with a sample query.
  - Test query used: `simulation risk`

### Task 3: Build Your RAG Query Workflow

- [x] Set up the configuration (MODEL, PORT, OLLAMA_HOST, document path)
- [x] Add in your search function
- [x] Pass your results as a JSON to the LLM
- [x] Design a system prompt (role) that instructs the LLM on how to process your data
- [x] Test your complete workflow with multiple queries, and fix your prompt if necessary
  - Main query used: `How can I design a safer simulation-based decision process?`
  - Prompt asks for a concise markdown response with recommendations, steps, and caution.


---

## 📤 To Submit

- For credit: Submit:
  1. Complete RAG workflow script: [`my_custom_rag_query.py`](my_custom_rag_query.py)
  2. Screenshot showing output from running: `python 07_rag/my_custom_rag_query.py`
  3. Brief explanation:
     - I created a custom CSV data source (`course_resources.csv`) so the RAG workflow can retrieve course-relevant engineering concepts instead of generic examples. This gives the model grounded context tied to systems engineering decision support.
     - The search function reads the CSV with pandas and performs case-insensitive matching across multiple columns (`title`, `category`, `difficulty`, `keywords`, and `content`). It then returns JSON containing the query, number of matches, and top results.
     - The system prompt instructs the LLM to use only the retrieved JSON and output a concise markdown response with a recommendation summary, three action steps, and one caution. This keeps responses structured and reduces hallucinated content.

---

![](../docs/images/icons.png)

---

← 🏠 [Back to Top](#LAB)
