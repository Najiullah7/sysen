#!/usr/bin/env python3
"""
Run Stage 1 + Stage 2 for ACTIVITY_assigner against local Ollama.

Usage:
  1) Ensure Ollama is running:
       ollama serve
  2) Ensure model exists:
       ollama list
  3) Run:
       python3 assigner.py
"""

import json
import urllib.request

MODEL = "gemma3:latest"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = """You are a managing partner at a consulting firm making staffing assignments.
Your job is to read unstructured descriptions of staff members and clients,
then assign each staff member to exactly 2 clients based on fit.

Return:
1. An assignment table with columns: Staff Member | Client 1 | Client 2 | Rationale (1 sentence)
2. A brief paragraph (3–5 sentences) summarizing your overall assignment logic

Rules:
- Each staff member gets exactly 2 clients
- Each client is assigned to exactly 1 staff member
- No client may be left unassigned
- Base assignments on demonstrated fit — skills, experience, communication style
- Flag any assignments where fit is weak and explain why
"""

STAFF_CLIENT_DATA = """--- STAFF ---

Alex Chen
Senior consultant, 9 years experience. Background in financial services and
regulatory compliance. Known for being methodical and detail-oriented.
Prefers clients who are organized and have clear deliverables.
Not great with ambiguous or fast-moving projects.

Brianna Okafor
Mid-level consultant, 4 years experience. Specialist in nonprofit and public
sector work. Very strong communicator — clients love her. Comfortable with
messy, evolving scopes. Has done a lot of stakeholder engagement work.

Carla Mendez
Senior consultant, 7 years experience. Deep expertise in healthcare and life
sciences. Data-heavy work is her strength — she's built several dashboards and
automated reporting tools. Tends to be blunt and efficient; not the warmest
bedside manner but clients respect her results.

Dana Park
Junior consultant, 2 years experience. Background is in marketing and consumer
research. Eager and creative. Better on smaller, well-defined tasks.
Still building confidence with senior client stakeholders.

Elliot Vasquez
Partner-level, 15 years experience. Generalist with a strong track record in
strategy and organizational change. Good relationship manager. Prefers high-stakes,
high-visibility engagements. Gets bored on smaller tactical work.

Fiona Marsh
Mid-level consultant, 5 years experience. Former journalist turned researcher.
Excellent writer and communicator. Often assigned to deliverable-heavy projects
(reports, white papers, presentations). Works well independently.
Prefers clients who give her creative latitude.

--- CLIENTS ---

Client A — Riverdale Community Health Clinic
Small nonprofit health clinic undergoing a strategic planning process.
Moderate budget. Stakeholders include the board, medical staff, and community
advocates. Very collaborative, but decisions are slow due to committee structure.
Main need: facilitation support and a written strategic plan.

Client B — Atlas Financial Group
Large regional bank. Highly regulated environment. Project involves auditing
their compliance documentation and recommending process improvements.
Very organized client — they have a detailed project plan. Expects formal
deliverables and regular status reports.

Client C — BrightPath Schools (Charter Network)
Fast-growing charter school network. Expanding from 3 to 8 schools.
Needs help with org design and HR policy. Client is enthusiastic but somewhat
disorganized. Decision-maker is the founder/CEO — she's visionary but hard to pin
down for meetings.

Client D — Nexagen Pharmaceuticals
Mid-size pharma company. Project is a data audit and KPI dashboard buildout
for their clinical operations team. Technical stakeholders who want results,
not hand-holding. Timeline is tight.

Client E — Greenway Transit Authority
Regional transit agency. Unionized workforce. Project involves a service
redesign study with significant community engagement components.
Political sensitivities — several board members have conflicting opinions.
Long timeline, phased project.

Client F — Solstice Consumer Goods
Consumer packaged goods brand. Needs a market research summary and brand
positioning analysis ahead of a product launch. Fun client, collaborative,
lots of back and forth. Not a huge budget. Creative work valued.

Client G — Meridian Capital Partners
Private equity firm. Fast-moving, high-expectations. Needs an org assessment
of a portfolio company. Very low patience for process — they want findings fast.
Elliot has a pre-existing relationship with the managing partner.

Client H — Harbor City Government (Parks Dept.)
Municipal parks department doing a 10-year capital planning study.
Lots of stakeholders — parks staff, city council, community groups.
Needs public engagement support and a formal report for the city council.

Client I — ClearView Diagnostics
Healthcare tech startup. Building a clinical decision support tool.
Needs help structuring their regulatory strategy and drafting FDA submission
materials. Technical and regulatory complexity is high. Startup culture —
informal, fast, sometimes chaotic.

Client J — The Holloway Foundation
Private philanthropy. Wants a landscape scan and strategic options memo on
workforce development funding. Small team, thoughtful, low-maintenance.
Primarily needs a polished, well-written deliverable.

Client K — Summit Retail Group
Multi-location retail chain. Undergoing a cost reduction initiative.
Wants operational benchmarking and process recommendations.
Client stakeholders are skeptical of consultants — they've had bad experiences
before. Need someone who can build trust quickly.

Client L — Vance Biomedical Research Institute
Academic research institute. Needs help redesigning their grant reporting
process and building a data tracking system. Methodical, detail-oriented
stakeholders. Comfortable with technical complexity.
"""

USER_PROMPT_STAGE_1 = f"""Below are descriptions of our 6 staff members and 12 clients.
Please make the best possible assignments.

{STAFF_CLIENT_DATA}
"""

# Edit these after seeing Stage 1 output:
SURPRISED_STAFF = "Dana Park"
SURPRISED_CLIENT = "Client G — Meridian Capital Partners"

USER_PROMPT_STAGE_2 = f"""I'm not sure about the assignment of {SURPRISED_STAFF} to {SURPRISED_CLIENT}.
Can you reconsider this pairing and either defend it or suggest an alternative?
"""


def call_ollama(system_prompt: str, user_prompt: str, model: str = MODEL) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_CHAT_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    return body["message"]["content"]


def main() -> None:
    print(f"\nUsing model: {MODEL}\n")

    print("=" * 80)
    print("STAGE 1 OUTPUT: INITIAL ASSIGNMENT")
    print("=" * 80)
    stage1 = call_ollama(SYSTEM_PROMPT, USER_PROMPT_STAGE_1)
    print(stage1)

    print("\n" + "=" * 80)
    print("STAGE 2 OUTPUT: STRESS TEST FOLLOW-UP")
    print("=" * 80)
    print(f"Follow-up tested: {SURPRISED_STAFF} <-> {SURPRISED_CLIENT}\n")
    stage2 = call_ollama(SYSTEM_PROMPT, USER_PROMPT_STAGE_2)
    print(stage2)

    print("\nDone. Take screenshots of Stage 1 table + Stage 2 follow-up.")


if __name__ == "__main__":
    main()