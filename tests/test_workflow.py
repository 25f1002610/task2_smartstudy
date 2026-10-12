"""Tests for Google ADK Multi-Agent Workflow Architecture."""

import pytest
from smartstudy.agent import (
    root_agent,
    coordinator_agent,
    planning_agent,
    parallel_analysts,
    topic_agent,
    practice_agent,
    schedule_agent,
    review_loop,
    writer_agent,
    review_agent,
    final_response_agent,
)
from smartstudy.agents.reviewer import approve_and_exit_loop
from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent
from google.adk.tools import exit_loop


def test_agent_roles_and_topology():
    """Verify that all seven required roles + final agent are instantiated and correctly wired."""
    assert isinstance(root_agent, SequentialAgent)
    assert len(root_agent.sub_agents) == 5

    # Stage 1: Coordinator
    assert root_agent.sub_agents[0].name == "coordinator_agent"
    assert root_agent.sub_agents[0].output_key == "student_requirements"

    # Stage 2: Planning
    assert root_agent.sub_agents[1].name == "planning_agent"
    assert root_agent.sub_agents[1].output_key == "planning_brief"

    # Stage 3: Parallel Analysts
    parallel_stage = root_agent.sub_agents[2]
    assert isinstance(parallel_stage, ParallelAgent)
    assert len(parallel_stage.sub_agents) == 3
    
    sub_names = [a.name for a in parallel_stage.sub_agents]
    assert "topic_agent" in sub_names
    assert "practice_agent" in sub_names
    assert "schedule_agent" in sub_names

    # Check distinct output keys on parallel agents
    assert topic_agent.output_key == "topic_analysis"
    assert practice_agent.output_key == "practice_plan"
    assert schedule_agent.output_key == "schedule_plan"

    # Stage 4: Review Loop
    loop_stage = root_agent.sub_agents[3]
    assert isinstance(loop_stage, LoopAgent)
    assert loop_stage.max_iterations == 2
    assert len(loop_stage.sub_agents) == 2
    assert loop_stage.sub_agents[0].name == "study_plan_writer_agent"
    assert loop_stage.sub_agents[0].output_key == "draft_plan"
    assert loop_stage.sub_agents[1].name == "review_agent"
    assert loop_stage.sub_agents[1].output_key == "review_feedback"

    # Check exit_loop / approve_and_exit_loop tools in reviewer
    reviewer = loop_stage.sub_agents[1]
    assert exit_loop in reviewer.tools
    assert approve_and_exit_loop in reviewer.tools

    # Stage 5: Final Response Agent
    assert root_agent.sub_agents[4].name == "final_response_agent"
    assert root_agent.sub_agents[4].output_key == "final_plan"


def test_loop_agent_bounded_to_two_iterations():
    """Ensure the loop agent has a strict maximum of 2 iterations."""
    assert review_loop.max_iterations == 2


def test_no_output_key_collisions():
    """Verify that all state keys are unique to prevent collisions."""
    keys = [
        coordinator_agent.output_key,
        planning_agent.output_key,
        topic_agent.output_key,
        practice_agent.output_key,
        schedule_agent.output_key,
        writer_agent.output_key,
        review_agent.output_key,
        final_response_agent.output_key,
    ]
    assert len(keys) == len(set(keys)), f"Duplicate output keys found: {keys}"
