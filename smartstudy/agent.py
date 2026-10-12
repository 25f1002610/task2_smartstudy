"""Root agent entry point for SmartStudy Multi-Agent Study Planner.

Constructs the complete Google ADK multi-agent workflow:
1. Sequential Stage 1: Coordinator Agent (normalizes student requirements)
2. Sequential Stage 2: Planning Agent (prepares strategic brief)
3. Parallel Stage: ParallelAgent with Topic Agent, Practice Agent, Schedule Agent
4. Loop Stage: LoopAgent with Study Plan Writer Agent & Review Agent (max_iterations=2, exit_loop)
5. Sequential Stage 5: Final Response Agent (presents complete approved plan)
"""

from __future__ import annotations

import os
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Suppress ADK deprecation notices for SequentialAgent/ParallelAgent/LoopAgent
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load environment configuration (.env)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
load_dotenv()

from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent

from .agents.coordinator import create_coordinator_agent
from .agents.planning import create_planning_agent
from .agents.topic import create_topic_agent
from .agents.practice import create_practice_agent
from .agents.schedule import create_schedule_agent
from .agents.writer import create_writer_agent
from .agents.reviewer import create_review_agent
from .agents.final_response import create_final_response_agent

# Get model from environment
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Instantiate all 7 specialist and coordinator agents + final response agent
coordinator_agent = create_coordinator_agent(model=MODEL)
planning_agent = create_planning_agent(model=MODEL)

topic_agent = create_topic_agent(model=MODEL)
practice_agent = create_practice_agent(model=MODEL)
schedule_agent = create_schedule_agent(model=MODEL)

# Parallel execution stage for independent analysis
parallel_analysts = ParallelAgent(
    name="parallel_analysts",
    description="Executes topic, practice, and schedule analyses in parallel",
    sub_agents=[topic_agent, practice_agent, schedule_agent],
)

writer_agent = create_writer_agent(model=MODEL)
review_agent = create_review_agent(model=MODEL)

# Bounded review loop with max_iterations=2 and early termination via exit_loop
review_loop = LoopAgent(
    name="review_loop",
    description="Bounded writer-reviewer loop with maximum 2 iterations and early exit",
    sub_agents=[writer_agent, review_agent],
    max_iterations=2,
)

final_response_agent = create_final_response_agent(model=MODEL)

# Master Sequential Workflow
root_agent = SequentialAgent(
    name="smartstudy_planner",
    description="Multi-agent intelligent study planner workflow using Google ADK",
    sub_agents=[
        coordinator_agent,
        planning_agent,
        parallel_analysts,
        review_loop,
        final_response_agent,
    ],
)
