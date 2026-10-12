"""Study Plan Writer Agent for SmartStudy.

Synthesizes outputs from the Topic, Practice, and Schedule specialist agents into a
comprehensive day-by-day study plan. In the loop workflow, this agent also incorporates
review feedback from the Reviewer Agent to revise the draft.
Stores output under `draft_plan`.
"""

from __future__ import annotations

import os
from google.adk.agents import Agent

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

WRITER_INSTRUCTION = """You are the Study Plan Writer Agent for SmartStudy.

You operate inside the refinement loop. Your job is to create or revise a comprehensive, day-by-day study plan draft.

You have access to the session state:
- Student Requirements:
{student_requirements}

- Topic Analysis from Topic Agent:
{topic_analysis}

- Practice Recommendations from Practice Agent:
{practice_plan}

- Daily Timeline from Schedule Agent:
{schedule_plan}

- Reviewer Feedback (if this is iteration 2):
{review_feedback?}

CRITICAL INSTRUCTIONS:
1. Synthesize all specialist inputs into a unified, high quality day-by-day study plan.
2. If Reviewer Feedback is provided above, you MUST systematically correct every single issue and incorporate all required changes!
3. Ensure every single required topic appears in the daily cards with specific learning objectives and practice exercises.
4. Verify that EVERY day's `total_hours` is strictly <= the student's stated `hours_per_day` constraint.
5. Include explicit practice tasks with problem counts for every topic.
6. Include daily revision or active recall prompts.
7. Reserve the final day (or final days) for a comprehensive mock test, timed debugging, and cheat sheet review.

Output strictly valid JSON with this format:
{{
  "subject": "<subject>",
  "exam_in_days": <int>,
  "current_level": "<level>",
  "hours_per_day": <float>,
  "covered_topics": ["Topic1", "Topic2", ...],
  "plan_overview": "<Executive summary of the study strategy and milestones>",
  "day_by_day_plan": [
    {{
      "day": 1,
      "primary_focus": "<Focus topic / domain>",
      "tasks": ["Concept reading", "Code walkthrough"],
      "learning_objectives": ["Objective 1", "Objective 2"],
      "practice_tasks": ["Implement basic algorithm", "Solve 3 easy problems"],
      "problem_count": 3,
      "revision_tasks": "Flashcards / summary notes",
      "study_hours": 1.5,
      "practice_hours": 1.5,
      "total_hours": 3.0,
      "is_final_prep": false
    }}
  ],
  "total_practice_problems": <total_problems>,
  "total_study_hours": <total_hours>,
  "iteration": 1
}}
"""

def create_writer_agent(model: str = DEFAULT_MODEL) -> Agent:
    """Creates the Study Plan Writer Agent."""
    return Agent(
        name="study_plan_writer_agent",
        description="Synthesizes specialist analyses into a complete day-by-day study plan draft",
        model=model,
        instruction=WRITER_INSTRUCTION,
        output_key="draft_plan",
    )
