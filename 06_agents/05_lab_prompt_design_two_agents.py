#!/usr/bin/env python
# 05_lab_prompt_design_two_agents.py
# LAB: Prompt Design with a 2-Agent Workflow
# Pairs with LAB_prompt_design.md
# Tim Fraser (adapted example)

# This script implements a 2-agent workflow for the Prompt Design lab.
# Agent 1: Data analyst summarizing project metrics into a structured markdown table.
# Agent 2: Action planner turning the summary into a short, prioritized action plan.

# 0. SETUP ###################################

## 0.1 Load Packages #################################

from functions import agent_run  # helper for running agents with roles/tasks


# 1. RAW INPUT DATA ###################################

# In a real workflow this could come from a CSV or API.
# Here we keep it simple and focus on prompt and agent design.
raw_status_report = """
We have a program with four projects in Q2:

Project Alpha:
- Budget: $500k
- Actual spend: $520k
- Planned completion: 2026-06-01
- Actual completion: 2026-06-10

Project Beta:
- Budget: $300k
- Actual spend: $250k
- Planned completion: 2026-05-15
- Actual completion: 2026-05-12

Project Gamma:
- Budget: $450k
- Actual spend: $480k
- Planned completion: 2026-06-20
- Forecast completion: 2026-07-05

Project Delta:
- Budget: $200k
- Actual spend: $210k
- Planned completion: 2026-05-30
- Actual completion: 2026-05-31
"""


# 2. AGENT 1 - DATA ANALYST ###################################

role_analyst = (
    "You are a systems engineering project data analyst. "
    "You read informal project status text and convert it into a clean, "
    "structured markdown table with one row per project. "
    "The table must have the following columns exactly, in order:\n"
    "- project_name\n"
    "- budget_usd\n"
    "- actual_spend_usd\n"
    "- schedule_status (On Time, Early, or Late)\n"
    "- cost_status (Under Budget, On Budget, or Over Budget)\n"
    "- brief_comment (one short sentence)\n\n"
    "Use professional, concise language. If information is missing, write 'Unknown'."
)

task_analyst = (
    "Read the status report below and populate the markdown table as specified "
    "in your role. Do not add any extra columns or narrative before or after "
    "the table.\n\n"
    f"STATUS REPORT:\n{raw_status_report}"
)

summary_table = agent_run(role=role_analyst, task=task_analyst, output="text")


# 3. AGENT 2 - ACTION PLANNER ###################################

role_planner = (
    "You are a portfolio manager creating an action plan from project metrics. "
    "You receive a markdown table of projects with budget and schedule status. "
    "Your output must be a short, prioritized action plan with this structure:\n\n"
    "1. A 2–3 sentence high-level overview.\n"
    "2. A 'High Priority Actions' section with 3–5 bullet points.\n"
    "3. A 'Monitoring Only' section with 2–3 bullet points.\n\n"
    "Use clear, directive language. Refer to projects by name. "
    "Focus on late or over-budget projects in 'High Priority Actions'."
)

task_planner = (
    "Using the project table below, generate the action plan in the exact "
    "structure described in your role. Do not reproduce the table; only write "
    "the narrative sections.\n\n"
    f"PROJECT TABLE:\n{summary_table}"
)

action_plan = agent_run(role=role_planner, task=task_planner, output="text")


# 4. VIEW RESULTS ###################################

print("===== AGENT 1: PROJECT SUMMARY TABLE =====")
print(summary_table)
print()
print("===== AGENT 2: PORTFOLIO ACTION PLAN =====")
print(action_plan)

