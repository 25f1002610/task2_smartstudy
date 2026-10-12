"""Topic Agent for SmartStudy.

Specialist agent that analyzes each topic in the student's syllabus for priority,
difficulty, conceptual learning focus, and recommended duration.
Executes in parallel with Practice and Schedule agents.
Stores output under `topic_analysis`.
"""

from __future__ import annotations

import os
from google.adk.agents import Agent

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

TOPIC_INSTRUCTION = """You are the Topic Specialist Agent for SmartStudy.

You operate as part of a parallel analysis team. You receive:
Requirements:
{student_requirements}

Planning Brief:
{planning_brief}

Your task:
Analyze every single topic listed in the student's syllabus. For every topic, provide:
1. `topic_name`: The exact topic name from the student's list.
2. `priority`: "High", "Medium", or "Low" based on exam frequency, foundational importance, and difficulty.
3. `difficulty`: "Easy", "Medium", or "Hard" relative to the student's current proficiency level.
4. `learning_focus`: Specific core concepts, algorithms, edge cases, and theoretical underpinnings to master.
5. `recommended_study_duration_hours`: Recommended hours devoted to theory, conceptual understanding, and dry-running for this topic.

Ensure ALL topics provided in the requirements are analyzed individually.
Include a `summary` field giving an overarching assessment of the syllabus difficulty and recommended topic sequencing.

Output strictly valid JSON with this format:
{{
  "subject": "<subject>",
  "topics": [
    {{
      "topic_name": "<name>",
      "priority": "High" | "Medium" | "Low",
      "difficulty": "Easy" | "Medium" | "Hard",
      "learning_focus": "<key concepts>",
      "recommended_study_duration_hours": <float>
    }}
  ],
  "summary": "<syllabus analysis>"
}}
"""

def create_topic_agent(model: str = DEFAULT_MODEL) -> Agent:
    """Creates the Topic Agent."""
    return Agent(
        name="topic_agent",
        description="Analyzes syllabus topics for priority, difficulty, and learning focus",
        model=model,
        instruction=TOPIC_INSTRUCTION,
        output_key="topic_analysis",
    )
