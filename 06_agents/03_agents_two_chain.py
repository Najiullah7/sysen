#!/usr/bin/env python
# 03_agents_two_chain.py
# Simple 2-Agent Workflow Example
# Pairs with 03_agents.py / ACTIVITY_multi_agent_workflow.md
# Tim Fraser (adapted example)

# This script demonstrates a minimal 2-agent workflow.
# Agent 1: Takes raw project data and produces a plain-language summary.
# Agent 2: Takes the summary and produces formatted output for stakeholders.

# 0. SETUP ###################################

## 0.1 Load Packages #################################

from functions import agent_run  # helper to run agents


# 1. RAW DATA ###################################

# In a real example, this might come from a CSV or API.
# Here we define a short text description so the focus is on the agents.
raw_data = """
We have project completion times in days for five projects:
Project A: 45 days
Project B: 60 days
Project C: 30 days
Project D: 75 days
Project E: 50 days
Assume all projects targeted 45 days.
"""


# 2. AGENT 1 - DATA SUMMARY AGENT ###################################

role1 = (
    "You are a project data analyst. "
    "Given raw text about project completion times, "
    "you produce a concise summary of performance: "
    "which projects were on time, which were late, and overall patterns."
)

task1 = (
    "Summarize the project performance based on the raw data below. "
    "Focus on which projects were late vs on time and any clear bottlenecks.\n\n"
    f"RAW DATA:\n{raw_data}"
)

summary = agent_run(role=role1, task=task1, output="text")


# 3. AGENT 2 - FORMATTING / COMMUNICATION AGENT ###################################

role2 = (
    "You are a communications specialist for engineering leadership. "
    "Given an analytical summary, you produce a short, formatted briefing "
    "for busy stakeholders. Use clear headings and bullet points."
)

task2 = (
    "Take the analytical summary below and turn it into a short briefing note "
    "for leadership. Include a one-sentence overview, 3–5 key bullet points, "
    "and 1–2 recommended next steps.\n\n"
    f"ANALYTICAL SUMMARY:\n{summary}"
)

briefing = agent_run(role=role2, task=task2, output="text")


# 4. VIEW RESULTS ###################################

print("===== AGENT 1: DATA SUMMARY =====")
print(summary)
print()
print("===== AGENT 2: FORMATTED BRIEFING =====")
print(briefing)

