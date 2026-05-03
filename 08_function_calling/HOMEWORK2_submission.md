# Homework 2 Submission: AI Agent System with RAG and Tools

Student: _[Your Name]_  
Course: SYSEN5381  
Homework: 2  
Date: 2026-04-06

---

## 1) Writing Component (Draft - personalize in your own words)

This project integrates my work from Lab 6, Lab 7, and Lab 8 into one end-to-end AI agent system. The system uses multiple agents with clear roles, retrieval-augmented generation (RAG) over a custom local data source, and function-calling tools that can access both local data and an external API. The goal is to produce grounded recommendations for systems engineering decision workflows rather than generic model responses.

The workflow starts with two retrieval-focused agents. One agent retrieves local context from my custom CSV dataset (`07_rag/data/course_resources.csv`) using a search tool adapted from my Lab 7 approach. The second agent retrieves supporting external evidence from the OpenAlex API. Their outputs are merged into a structured JSON context payload that is passed to downstream agents.

A third agent acts as an analyst and creates a concise interpretation of the combined context. A final reporter agent rewrites that analysis into a stakeholder-facing recommendation with implementation steps and caution notes. This role separation improves clarity, allows each prompt to be focused, and mirrors realistic team workflows where data gathering, analysis, and communication are separate responsibilities.

One design challenge was making the tool-calling chain robust when local model services are unavailable. I addressed this by adding deterministic Python fallbacks for retrieval, analysis summaries, and final reporting so the script still produces valid outputs in constrained environments. This keeps the workflow reproducible and easier to debug while still demonstrating the intended multi-agent, RAG, and tool-calling architecture.

---

## 2) Code Links (Git Repository Links)

- Main integrated Homework 2 system:  
  [homework2_ai_agent_system.py](https://github.com/timothyfraser/dsai/blob/main/08_function_calling/homework2_ai_agent_system.py)
- Multi-agent prompt/orchestration foundation (Lab 6):  
  [05_lab_prompt_design_two_agents.py](https://github.com/timothyfraser/dsai/blob/main/06_agents/05_lab_prompt_design_two_agents.py)
- Custom RAG implementation (Lab 7):  
  [my_custom_rag_query.py](https://github.com/timothyfraser/dsai/blob/main/07_rag/my_custom_rag_query.py)
- Function-calling runtime and agent wrappers (Lab 8):  
  [08_function_calling/functions.py](https://github.com/timothyfraser/dsai/blob/main/08_function_calling/functions.py)

---

## 3) Outputs / Evidence (Samples)

### Output Sample A - System Run Header

```text
===== HOMEWORK 2 INTEGRATED SYSTEM =====
Model: smollm2:1.7b
Fallback mode used: False
```

### Output Sample B - Agent 1A Tool Output (Local RAG Retrieval)

```text
===== AGENT 1A TOOL OUTPUT (RAG) =====
 id                           title           category   difficulty                             keywords                                                                                            content
  1          System Dynamics Basics           modeling     beginner                stocks,flows,feedback   Introduces stock-and-flow diagrams, reinforcing loops, and balancing loops for systems modeling.
  2       Monte Carlo Risk Analysis   decision_support intermediate          uncertainty,risk,simulation   Uses random sampling to estimate risk ranges and confidence intervals for engineering decisions.
  3       Requirements Traceability project_management     beginner requirements,verification,validation                   Shows how to map stakeholder requirements to design artifacts and test evidence.
```

### Output Sample C - Agent 1B Tool Output (External API Retrieval)

```text
===== AGENT 1B TOOL OUTPUT (OPENALEX API) =====
title                                                                 publication_year  cited_by_count
Regulatory Landslide Hazard Zoning in New Caledonia...              2027              0
Refusing expectation? Class, masculinity and selfhood...            2027              0
Business Model Innovation among Startups...                          2027              0
```

### Output Sample D - Final Reporter Output (Excerpt)

```text
===== AGENT 3 FINAL REPORT =====
Recommendation Summary:
Use a model-based, human-in-the-loop AI workflow with explicit risk checks.

Implementation Steps:
1) Retrieve local systems engineering context.
2) Add external evidence from recent literature.
3) Generate concise recommendations with caution notes.
```

---

## 4) Documentation

### 4.1 System Architecture

The integrated workflow uses four role-specific agents:

1. Agent 1A (RAG Retriever): uses function calling to run `search_course_resources()`
2. Agent 1B (Evidence Retriever): uses function calling to run `fetch_openalex_evidence()`
3. Agent 2 (Analyst): combines local and external context into a grounded interpretation
4. Agent 3 (Reporter): converts analysis into a stakeholder-facing report

Data flow:

1. User question -> Agent 1A + Agent 1B (tools)
2. Tool outputs -> merged JSON context
3. JSON context -> Agent 2 analysis
4. Analysis -> Agent 3 final report

### 4.2 RAG Data Source

Primary local data source:

- File: `07_rag/data/course_resources.csv`
- Records: 10 course-themed entries
- Purpose: provide grounded context relevant to systems engineering and AI workflows

Data columns:

| Column Name | Type | Description |
|---|---|---|
| id | integer | Unique row identifier |
| title | string | Resource title |
| category | string | Thematic category (e.g., modeling, analytics) |
| difficulty | string | Relative difficulty level |
| keywords | string | Comma-separated keywords used for matching |
| content | string | Short content summary used in retrieval context |

### 4.3 Tool Functions

| Tool Name | Purpose | Parameters | Returns |
|---|---|---|---|
| `search_course_resources` | Local CSV retrieval for RAG grounding | `query` (str), `top_n` (int), optional `document` (str) | List of matched resource dictionaries |
| `fetch_openalex_evidence` | External evidence lookup via OpenAlex API | `topic` (str), `per_page` (int) | List of recent works (title/year/citations/doi) |

### 4.4 Technical Details

- Main script: `08_function_calling/homework2_ai_agent_system.py`
- Runtime helper: `08_function_calling/functions.py`
- LLM endpoint: Ollama local API (`http://localhost:11434/api/chat`)
- External API endpoint: OpenAlex Works API (`https://api.openalex.org/works`)
- Python packages: `requests`, `pandas`

### 4.5 Usage Instructions

1. Install dependencies:
   - `pip install requests pandas`
2. Ensure Ollama is running locally (if using live agent generations):
   - Example: `ollama serve`
3. Ensure model is available:
   - `ollama pull smollm2:1.7b`
4. Run from repository root:
   - `python3 08_function_calling/homework2_ai_agent_system.py`
5. Verify outputs:
   - Agent 1A prints local RAG retrieval table
   - Agent 1B prints OpenAlex API retrieval table
   - Agent 2 prints analysis
   - Agent 3 prints final report

---

## Notes

- This document is a complete draft for Homework 2 requirements.
- Replace `Student` name and personalize the writing section in your own words before submission to satisfy the "NOT AI-generated" writing requirement.
- If your instructor prefers screenshots instead of text output samples, replace Section 3 with embedded screenshots from your run.
