"""Coordinator Agent for SmartStudy.

Normalizes the student's natural language request into a validated, structured
requirements object and stores it in the session state under `student_requirements`.
"""

from __future__ import annotations

import os
from google.adk.agents import Agent

# Model configuration with environment variable support
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

COORDINATOR_INSTRUCTION = """You are the Coordinator Agent for SmartStudy, an intelligent multi-agent study planner.

Your mission is to analyze the student's input and extract structured study requirements.

Examine the student's message and output a clean, well-structured JSON object matching these fields:
- `subject`: Name of the subject/course (e.g., "Data Structures", "Operating Systems", "Machine Learning")
- `exam_in_days`: Integer number of days remaining until the exam (e.g., 10). If an exam date is provided, compute the days remaining.
- `current_level`: Proficiency level ("Beginner", "Intermediate", or "Advanced"). If not explicitly stated, infer reasonably or default to "Intermediate".
- `topics`: List of distinct strings representing all topics the student needs to cover (e.g., ["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming"]).
- `hours_per_day`: Float/number of hours available to study each day (e.g., 3.0).
- `preferences`: Any explicit preferences (e.g., weak topics, preferred topic order, focus areas), or null if none.
- `constraints`: Any specific time or schedule constraints stated by the student, or null if none.
- `is_valid`: Boolean - true if essential requirements (subject, topics, exam_in_days, hours_per_day) are present or can be reliably inferred.
- `missing_fields`: List of missing essential fields if the request is incomplete (e.g. ["topics", "hours_per_day"]).

CRITICAL RULES:
1. Always preserve the user's stated constraints and topic list.
2. If essential inputs are missing (e.g. user just says "Make a study plan"), mark `is_valid: false` and list what is missing.
3. Output ONLY the JSON object. Do not wrap in markdown quotes if possible, or provide valid parseable JSON.
"""

def create_coordinator_agent(model: str = DEFAULT_MODEL) -> Agent:
    """Creates the Coordinator Agent."""
    return Agent(
        name="coordinator_agent",
        description="Normalizes student input into structured study requirements",
        model=model,
        instruction=COORDINATOR_INSTRUCTION,
        output_key="student_requirements",
    )
