"""Planning Agent for SmartStudy.

Synthesizes the student's normalized requirements into a high-level strategic planning brief,
setting concrete parameters and guidelines for the specialist agents (Topic, Practice, Schedule).
Stores output under `planning_brief`.
"""

from __future__ import annotations

import os
from google.adk.agents import Agent

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

PLANNING_INSTRUCTION = """You are the Planning Agent for SmartStudy.

You receive the student's normalized requirements:
{student_requirements}

Your responsibility is to formulate a high-level strategic planning brief that guides the three specialist agents (Topic Agent, Practice Agent, and Schedule Agent) who will execute next in parallel.

Analyze the total study budget:
- Total Study Hours = exam_in_days * hours_per_day
- Assess the difficulty and volume of the topic list relative to the time available.
- Define a realistic pacing strategy:
  * Early phase: foundational concepts and core algorithms
  * Mid phase: complex data structures, trees, graphs, and dynamic programming
  * Late phase: synthesis, mixed practice, timed mock tests, and comprehensive revision.

Output a structured JSON object with:
- `subject`: Name of subject
- `exam_in_days`: Number of days
- `current_level`: Student proficiency
- `topics`: List of topics to cover
- `hours_per_day`: Daily study hour limit
- `total_available_hours`: Total hours budget (days * hours_per_day)
- `strategy_summary`: Clear overview of pacing, topic ordering, and study/practice balance
- `guidelines_for_specialists`: Explicit instructions for:
  * Topic Agent: how to weigh priorities given the deadline and level
  * Practice Agent: target problem intensity and mix (coding vs concepts)
  * Schedule Agent: day-by-day distribution ensuring daily hours <= hours_per_day, with revision and a final prep / mock test day.

Output strictly valid JSON.
"""

def create_planning_agent(model: str = DEFAULT_MODEL) -> Agent:
    """Creates the Planning Agent."""
    return Agent(
        name="planning_agent",
        description="Prepares strategic planning brief for specialist agents",
        model=model,
        instruction=PLANNING_INSTRUCTION,
        output_key="planning_brief",
    )
