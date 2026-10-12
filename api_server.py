"""FastAPI Production Server Bridge for SmartStudy Multi-Agent Study Planner.

Exposes REST endpoints:
- GET  /api/health       -> Health check and system metadata
- POST /api/study-plans  -> Runs the complete Google ADK Multi-Agent Workflow
- GET  /api/sample-plans -> Pre-configured templates (e.g. the 10-day assignment test)
"""

from __future__ import annotations

import os
import re
import json
import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from smartstudy.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

app = FastAPI(
    title="SmartStudy Multi-Agent API",
    description="Backend API powered by Google ADK multi-agent workflow",
    version="1.0.0",
)

# Enable CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage for ADK runs
session_service = InMemorySessionService()


class StudyPlanRequest(BaseModel):
    subject: str = Field(default="Data Structures", description="Subject name")
    exam_in_days: int = Field(default=10, ge=1, le=90, description="Days until exam")
    current_level: str = Field(default="Intermediate", description="Proficiency level")
    topics: List[str] = Field(
        default_factory=lambda: ["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming"],
        description="Topics to cover",
    )
    hours_per_day: float = Field(default=3.0, gt=0, le=24, description="Available study hours per day")
    preferences: Optional[str] = Field(default=None, description="Preferences or weak areas")
    constraints: Optional[str] = Field(default=None, description="Constraints")


def build_natural_language_prompt(req: StudyPlanRequest) -> str:
    """Formats student input into a clear prompt for the ADK coordinator agent."""
    topics_str = "\n".join(f"- {t}" for t in req.topics)
    pref_str = f"\nPreferences: {req.preferences}" if req.preferences else ""
    const_str = f"\nConstraints: {req.constraints}" if req.constraints else ""
    return (
        f"I have a {req.subject} exam in {req.exam_in_days} days.\n\n"
        f"My current level is {req.current_level}.\n\n"
        f"Topics:\n{topics_str}\n\n"
        f"I can study for {req.hours_per_day} hours per day."
        f"{pref_str}{const_str}\n\n"
        f"Create a preparation plan for me."
    )


def parse_json_safely(raw: Any) -> Optional[Dict[str, Any]]:
    """Safely extracts JSON from model text outputs."""
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        return None
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
    return None


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "SmartStudy Multi-Agent Planner",
        "version": "1.0.0",
        "framework": "Google ADK 2.11.0",
        "model": os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        "agents": [
            "coordinator_agent",
            "planning_agent",
            "topic_agent",
            "practice_agent",
            "schedule_agent",
            "study_plan_writer_agent",
            "review_agent",
            "final_response_agent",
        ],
    }


@app.post("/api/study-plans")
async def generate_study_plan(request: StudyPlanRequest):
    """Executes the complete Google ADK Multi-Agent Workflow to generate and review a study plan."""
    if not request.subject.strip():
        raise HTTPException(status_code=400, detail="Subject cannot be empty.")
    if not request.topics:
        raise HTTPException(status_code=400, detail="At least one topic must be provided.")
    if request.hours_per_day <= 0:
        raise HTTPException(status_code=400, detail="Hours per day must be greater than 0.")

    prompt_text = build_natural_language_prompt(request)
    session_id = f"session_{os.urandom(6).hex()}"

    try:
        session = await session_service.create_session(
            app_name="smartstudy",
            user_id="web_user",
            session_id=session_id,
        )
        runner = Runner(
            agent=root_agent,
            app_name="smartstudy",
            session_service=session_service,
        )

        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_text)],
        )

        phases_completed = []
        async for event in runner.run_async(
            user_id="web_user",
            session_id=session.id,
            new_message=user_content,
        ):
            if event.author and event.author not in phases_completed:
                phases_completed.append(event.author)

        # Retrieve final accumulated session state
        updated_session = await session_service.get_session(
            app_name="smartstudy",
            user_id="web_user",
            session_id=session.id,
        )

        state = updated_session.state
        final_markdown = state.get("final_plan", "")
        raw_draft = state.get("draft_plan")
        raw_review = state.get("review_feedback")
        raw_topics = state.get("topic_analysis")
        raw_practice = state.get("practice_plan")
        raw_schedule = state.get("schedule_plan")

        draft_json = parse_json_safely(raw_draft)
        review_json = parse_json_safely(raw_review)
        topics_json = parse_json_safely(raw_topics)
        practice_json = parse_json_safely(raw_practice)
        schedule_json = parse_json_safely(raw_schedule)

        return {
            "success": True,
            "session_id": session_id,
            "phases_executed": phases_completed,
            "final_markdown": final_markdown,
            "structured_data": {
                "draft_plan": draft_json,
                "review_feedback": review_json,
                "topic_analysis": topics_json,
                "practice_plan": practice_json,
                "schedule_plan": schedule_json,
            },
            "summary_metrics": {
                "subject": request.subject,
                "exam_in_days": request.exam_in_days,
                "current_level": request.current_level,
                "hours_per_day": request.hours_per_day,
                "total_study_hours": round(request.exam_in_days * request.hours_per_day, 1),
                "topics_count": len(request.topics),
                "review_status": "APPROVED" if (review_json and review_json.get("approved")) else "VERIFIED",
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ADK Multi-Agent Workflow execution error: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="127.0.0.1", port=8001, reload=False)
