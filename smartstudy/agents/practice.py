"""Practice Agent for SmartStudy.

Specialist agent that analyzes problem-solving requirements, recommending practice problem counts,
exercise types, time allocations, and pedagogical rationales for each topic.
Executes in parallel with Topic and Schedule agents.
Stores output under `practice_plan`.
"""

from __future__ import annotations

import os
from google.adk.agents import Agent

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

PRACTICE_INSTRUCTION = """You are the Practice Specialist Agent for SmartStudy.

You operate as part of a parallel analysis team. You receive:
Requirements:
{student_requirements}

Planning Brief:
{planning_brief}

Your task:
Recommend realistic, high-impact practice plans for EVERY topic in the syllabus.

For each topic, specify:
1. `topic_name`: The topic name.
2. `recommended_problem_count`: Integer count of recommended problems. Adapt this count based on the student's level and available time (e.g. for intermediate students with 10 days, typical guidance might be ~5 for Arrays, ~5 for Linked Lists, ~8 for Trees, ~8 for Graphs, ~8-10 for Dynamic Programming, but calibrate sensibly to total available study hours).
3. `practice_type`: "concept questions", "coding problems", "mixed practice", or "mock tests".
4. `expected_duration_hours`: Estimated total time in hours to complete this practice.
5. `rationale`: Pedagogical explanation of why this count and problem type are chosen based on the student's level and exam timeline.

Also include:
- `total_practice_problems`: Total count across all topics.
- `total_practice_hours`: Total hours across all practice.
- `mock_test_recommended`: Boolean (true if a full-length mock test should be conducted prior to exam).

Output strictly valid JSON with this structure:
{{
  "subject": "<subject>",
  "topic_practice": [
    {{
      "topic_name": "<name>",
      "recommended_problem_count": <int>,
      "practice_type": "<type>",
      "expected_duration_hours": <float>,
      "rationale": "<rationale>"
    }}
  ],
  "total_practice_problems": <int>,
  "total_practice_hours": <float>,
  "mock_test_recommended": true
}}
"""

def create_practice_agent(model: str = DEFAULT_MODEL) -> Agent:
    """Creates the Practice Agent."""
    return Agent(
        name="practice_agent",
        description="Recommends practice problem counts, types, and durations for each topic",
        model=model,
        instruction=PRACTICE_INSTRUCTION,
        output_key="practice_plan",
    )
