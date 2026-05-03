# lab_ai_reporter.py
# AI-Powered Data Reporter (LAB)
# Pairs with LAB_ai_reporter.md
# Tim Fraser

# This script completes the AI Reporter lab: it queries the Census API from the
# previous lab, processes the data, sends it to an AI model with a structured
# prompt, and saves the generated report. Demonstrates end-to-end pipeline:
# API -> process -> prompt -> AI -> report.

# 0. SETUP ###################################

## 0.1 Load Packages #################################

# pip install requests python-dotenv (and markdown python-docx for multiple formats)
import json
import os
import requests
from dotenv import load_dotenv

# Optional: uncomment to save as .html and .docx as in 05_reporting.py
# import markdown
# from docx import Document

# Load .env from script directory or project root (for CENSUS_API_KEY, OPENAI_API_KEY)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv()
load_dotenv(os.path.join(_script_dir, ".env"))
load_dotenv(os.path.join(_script_dir, "..", ".env"))

# 1. DATA PIPELINE ###################################

## 1.1 Fetch API Data #################################

# Reuse the Census API query from 01_query_api (my_good_query.py).
# Endpoint: Economic Census 2022, base statistics. Returns establishments,
# receipts, employment by NAICS industry for the US.
api_key = os.getenv("CENSUS_API_KEY")
if not api_key:
    raise ValueError("CENSUS_API_KEY not found in .env. Add it from 01_query_api lab.")

url = "https://api.census.gov/data/2022/ecnbasic"
params = {
    "get": "NAICS2022,NAICS2022_LABEL,NAME,GEO_ID,ESTAB,RCPTOT,EMP",
    "for": "us:*",
    "key": api_key,
}

response = requests.get(url, params=params)
response.raise_for_status()
raw = response.json()

## 1.2 Process and Format for AI #####################

# Use first row as headers, take 20 rows for enough variety without excess tokens
headers = raw[0]
rows = raw[1:21]
records = [dict(zip(headers, row)) for row in rows]

# Build a compact text summary for the prompt (reduces token use and keeps focus)
# Include record count and a few sample rows so the AI can describe structure and values
data_for_ai = (
    f"Total records (sample): {len(records)}. "
    f"Columns: {', '.join(headers)}. "
    f"Sample rows (first 3): {json.dumps(records[:3], indent=2)}. "
    f"Remaining rows (next 5): {json.dumps(records[3:8])}."
)

# 2. DESIGN PROMPT AND CALL AI ###################################

## 2.1 Prompt ########################################

# Clear instructions: what to return (summary, insights, format) so output is consistent
system_instruction = (
    "You are a data analyst. Given a sample of Census Economic data, "
    "write a short, professional report. Use markdown: headings, bullet points, "
    "and 2-3 short paragraphs. Be concise."
)
user_prompt = (
    "Census API data (2022 ecnbasic, US):\n\n"
    f"{data_for_ai}\n\n"
    "Write a brief report (about 150-200 words) with:\n"
    "1. **Summary**: What this dataset is and what the sample shows.\n"
    "2. **Key insights**: 3-4 bullet points (e.g., top industries, ranges of ESTAB/RCPTOT/EMP).\n"
    "3. **Recommendation**: One sentence on how this data could be used next.\n"
    "Use markdown headings (##) and bullets."
)

## 2.2 Call OpenAI ####################################

# Uses same pattern as 04_openai.py. For Ollama local/cloud, swap in 02_ollama / 03_ollama_cloud.
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("OPENAI_API_KEY not found in .env. Add it for AI reporting.")

openai_url = "https://api.openai.com/v1/chat/completions"
openai_headers = {
    "Authorization": f"Bearer {openai_key}",
    "Content-Type": "application/json",
}
openai_body = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_prompt},
    ],
}

print("\n🚀 Fetching data and requesting AI report...\n")
resp = requests.post(openai_url, headers=openai_headers, json=openai_body)
resp.raise_for_status()
report_text = resp.json()["choices"][0]["message"]["content"]

# 3. SAVE REPORT ###################################

## 3.1 Write .md and .txt ###########################

report_md = os.path.join(_script_dir, "lab_report.md")
report_txt = os.path.join(_script_dir, "lab_report.txt")

with open(report_md, "w", encoding="utf-8") as f:
    f.write(report_text)
with open(report_txt, "w", encoding="utf-8") as f:
    f.write(report_text)

print("📝 AI Report (preview):\n")
print(report_text)
print("\n✅ Report saved:")
print(f"   {report_md}")
print(f"   {report_txt}")
print("\n✅ Lab AI Reporter complete.\n")
