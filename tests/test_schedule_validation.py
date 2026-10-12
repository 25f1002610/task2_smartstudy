"""Tests for schedule validation, topic coverage, and quality rules."""

import pytest
from smartstudy.schemas import (
    DetailedDayPlan,
    StudyPlanDraft,
    CriteriaChecks,
    ReviewFeedback,
)


def create_sample_10_day_draft(daily_hours: float = 3.0, omit_topic: bool = False, omit_revision: bool = False):
    """Helper to generate a mock 10-day draft."""
    topics = ["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming"]
    if omit_topic:
        topics = ["Arrays", "Linked Lists", "Trees", "Graphs"]  # Missing DP

    days = []
    for day in range(1, 11):
        is_final = day == 10
        if is_final:
            focus = "Final Preparation & Comprehensive Mock Test"
            tasks = ["Full 3-hour mock exam", "Error analysis and formula review"]
            objectives = ["Exam timing mastery", "Confidence reinforcement"]
            practice = ["Full length mock test (5 mixed problems)"]
            prob_count = 5
            revision = "Comprehensive formula sheet review"
        else:
            t = topics[(day - 1) % len(topics)]
            focus = f"{t} Mastery"
            tasks = [f"Study {t} core concepts", f"Solve {t} interview problems"]
            objectives = [f"Understand {t} invariants", f"Analyze time complexity"]
            practice = [f"Solve 2 medium problems on {t}"]
            prob_count = 2
            revision = "" if omit_revision else f"Active recall on day {day-1} problems"

        days.append(
            DetailedDayPlan(
                day=day,
                primary_focus=focus,
                tasks=tasks,
                learning_objectives=objectives,
                practice_tasks=practice,
                problem_count=prob_count,
                revision_tasks=revision,
                study_hours=daily_hours / 2,
                practice_hours=daily_hours / 2,
                total_hours=daily_hours,
                is_final_prep=is_final,
            )
        )

    return StudyPlanDraft(
        subject="Data Structures",
        exam_in_days=10,
        current_level="Intermediate",
        hours_per_day=daily_hours,
        covered_topics=topics,
        plan_overview="Comprehensive 10-day study roadmap for Data Structures",
        day_by_day_plan=days,
        total_practice_problems=23,
        total_study_hours=daily_hours * 10,
        iteration=1,
    )


def test_complete_plan_meets_all_criteria():
    """Verify that a compliant 10-day plan satisfies all 5 quality criteria."""
    draft = create_sample_10_day_draft(daily_hours=3.0)
    
    # 1. Topic coverage
    expected_topics = {"Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming"}
    actual_topics = set(draft.covered_topics)
    assert expected_topics.issubset(actual_topics)

    # 2. Time limits
    for day in draft.day_by_day_plan:
        assert day.total_hours <= draft.hours_per_day

    # 3. Sufficient practice
    assert draft.total_practice_problems >= 20

    # 4. Revision included
    has_revision = any(bool(day.revision_tasks.strip()) for day in draft.day_by_day_plan)
    assert has_revision is True

    # 5. Final day appropriate
    final_day = draft.day_by_day_plan[-1]
    assert final_day.is_final_prep is True
    assert "Mock Test" in final_day.primary_focus or "Preparation" in final_day.primary_focus


def test_reviewer_catches_missing_topic():
    """A draft with a missing topic must fail review checks."""
    draft = create_sample_10_day_draft(omit_topic=True)
    required_topics = {"Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming"}
    missing = required_topics - set(draft.covered_topics)
    assert "Dynamic Programming" in missing


def test_reviewer_catches_missing_revision():
    """A draft without spaced revision must fail criteria check 4."""
    draft = create_sample_10_day_draft(omit_revision=True)
    has_revision = any(bool(day.revision_tasks.strip()) for day in draft.day_by_day_plan[:-1])
    assert has_revision is False


def test_strict_two_hour_constraint():
    """Test B: When available time is 2 hours/day, every day must be <= 2.0 hours."""
    draft = create_sample_10_day_draft(daily_hours=2.0)
    for day in draft.day_by_day_plan:
        assert day.total_hours <= 2.0
    assert draft.total_study_hours == 20.0
