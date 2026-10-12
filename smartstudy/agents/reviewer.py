"""Review Agent for SmartStudy.

Rigorous evaluation agent that verifies the study plan draft against the 5 mandatory criteria.
Equipped with Google ADK's `exit_loop` tool. When the draft passes all criteria, it calls
`exit_loop` to terminate the LoopAgent early. If defects remain, it records specific issues
and required changes for the writer without escalating, allowing up to 2 bounded iterations.
Stores output under `review_feedback`.
"""

from __future__ import annotations

import os
from google.adk.agents import Agent
from google.adk.tools import ToolContext, exit_loop

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

def approve_and_exit_loop(evaluation_summary: str, tool_context: ToolContext) -> str:
    """Call this tool when the study plan meets ALL 5 quality criteria to approve it and exit the review loop.

    Args:
        evaluation_summary: Summary explanation of why the draft passed all criteria.
    """
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = False
    tool_context.actions.state_delta["review_feedback"] = (
        f'{{"approved": true, "evaluation_notes": "{evaluation_summary}", '
        f'"criteria_checks": {{"all_topics_covered": true, "time_constraints_respected": true, '
        f'"sufficient_practice_included": true, "revision_included": true, "final_day_appropriate": true}}, '
        f'"issues": [], "required_changes": [], "iteration": 1}}'
    )
    return "Study plan successfully approved. Exiting review loop."


REVIEWER_INSTRUCTION = """You are the Quality Review Agent for SmartStudy.

Your role is to evaluate the study plan draft with strict adherence to academic quality standards.

You have access to:
Student Requirements:
{student_requirements}

Draft Study Plan to evaluate:
{draft_plan}

EVALUATE THE DRAFT AGAINST ALL FIVE MANDATORY CRITERIA:
1. TOPIC COVERAGE: Are all supplied topics from the student's requirements included in the schedule?
2. TIME CONSTRAINTS: Does every single day respect the stated daily hour limit (e.g., if hours_per_day is 3.0, no day exceeds 3.0 hours)? Is total duration realistic?
3. SUFFICIENT PRACTICE: Does each topic have concrete practice problems, coding exercises, or drills?
4. SPACED REVISION: Are revision/recall activities scheduled throughout the days rather than only at the very end?
5. FINAL DAY APPROPRIATE: Is the final day dedicated to comprehensive preparation, mock testing, and strategy rather than introducing heavy new topics?

DECISION PROTOCOL:
Case A: IF ALL 5 CRITERIA ARE MET AND NO DEFECTS EXIST:
- YOU MUST CALL THE `approve_and_exit_loop` or `exit_loop` TOOL IMMEDIATELY to terminate the review loop early.
- Provide a clear approval summary explaining why it passed.

Case B: IF ANY DEFICIENCY IS FOUND:
- DO NOT call the exit loop tools.
- Output your structured JSON review with `approved: false`.
- Populate `issues` with concrete descriptions of each defect.
- Populate `required_changes` with exact instructions on how the writer must fix them.
- The workflow will automatically route your feedback back to the writer for iteration 2.

Structured JSON output format:
{{
  "approved": true | false,
  "criteria_checks": {{
    "all_topics_covered": true | false,
    "time_constraints_respected": true | false,
    "sufficient_practice_included": true | false,
    "revision_included": true | false,
    "final_day_appropriate": true | false
  }},
  "issues": ["Issue 1", ...],
  "required_changes": ["Change 1", ...],
  "iteration": 1,
  "evaluation_notes": "<Concise summary of review decision>"
}}
"""

def create_review_agent(model: str = DEFAULT_MODEL) -> Agent:
    """Creates the Review Agent with loop-exit capabilities."""
    return Agent(
        name="review_agent",
        description="Evaluates draft against 5 quality criteria and exits loop when approved",
        model=model,
        instruction=REVIEWER_INSTRUCTION,
        tools=[approve_and_exit_loop, exit_loop],
        output_key="review_feedback",
    )
