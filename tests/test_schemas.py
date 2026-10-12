"""Tests for SmartStudy Pydantic Schemas and Contracts."""

import pytest
from pydantic import ValidationError
from smartstudy.schemas import (
    StudentRequirements,
    PlanningBrief,
    TopicAnalysisItem,
    TopicAnalysis,
    PracticePlanItem,
    PracticePlan,
    DayScheduleItem,
    SchedulePlan,
    DetailedDayPlan,
    StudyPlanDraft,
    CriteriaChecks,
    ReviewFeedback,
    FinalStudyPlan,
)


def test_student_requirements_valid():
    """Valid student requirements should parse cleanly."""
    req = StudentRequirements(
        subject="Data Structures",
        exam_in_days=10,
        current_level="Intermediate",
        topics=["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming"],
        hours_per_day=3.0,
        preferences="Prefer Trees and Graphs before DP",
        constraints="No more than 3 hours per day",
    )
    assert req.subject == "Data Structures"
    assert req.exam_in_days == 10
    assert len(req.topics) == 5
    assert req.hours_per_day == 3.0
    assert req.is_valid is True


def test_student_requirements_invalid_hours():
    """Hours per day must be positive and <= 24."""
    with pytest.raises(ValidationError):
        StudentRequirements(
            subject="Algorithms",
            exam_in_days=5,
            current_level="Beginner",
            topics=["Sorting"],
            hours_per_day=0,  # Invalid: gt 0 required
        )

    with pytest.raises(ValidationError):
        StudentRequirements(
            subject="Algorithms",
            exam_in_days=5,
            current_level="Beginner",
            topics=["Sorting"],
            hours_per_day=25,  # Invalid: le 24 required
        )


def test_schedule_plan_daily_hours_validation():
    """Daily schedule validator must reject days that exceed max allowed hours."""
    valid_days = [
        DayScheduleItem(
            day=1,
            topics_and_tasks=["Arrays review", "Solve 5 problems"],
            study_duration_hours=1.5,
            practice_duration_hours=1.5,
            revision_activity="Recall time complexities",
            daily_total_hours=3.0,
        ),
        DayScheduleItem(
            day=2,
            topics_and_tasks=["Linked Lists"],
            study_duration_hours=1.0,
            practice_duration_hours=1.5,
            revision_activity="Review pointer edge cases",
            daily_total_hours=2.5,
        ),
    ]

    plan = SchedulePlan(
        subject="Data Structures",
        total_days=2,
        max_daily_hours_allowed=3.0,
        daily_schedule=valid_days,
        total_scheduled_hours=5.5,
        schedule_strategy="Evenly paced",
    )
    assert len(plan.daily_schedule) == 2

    # Now test an invalid day exceeding limit
    invalid_days = [
        DayScheduleItem(
            day=1,
            topics_and_tasks=["Heavy DP session"],
            study_duration_hours=2.0,
            practice_duration_hours=2.0,
            revision_activity="None",
            daily_total_hours=4.0,  # Exceeds 3.0!
        )
    ]

    with pytest.raises(ValidationError):
        SchedulePlan(
            subject="Data Structures",
            total_days=1,
            max_daily_hours_allowed=3.0,
            daily_schedule=invalid_days,
            total_scheduled_hours=4.0,
            schedule_strategy="Overloaded day",
        )


def test_review_feedback_contract():
    """Review feedback should properly encapsulate approval and criteria checks."""
    criteria = CriteriaChecks(
        all_topics_covered=True,
        time_constraints_respected=True,
        sufficient_practice_included=True,
        revision_included=True,
        final_day_appropriate=True,
    )
    fb = ReviewFeedback(
        approved=True,
        criteria_checks=criteria,
        issues=[],
        required_changes=[],
        iteration=1,
        evaluation_notes="Plan satisfies all quality benchmarks.",
    )
    assert fb.approved is True
    assert len(fb.issues) == 0
    assert fb.criteria_checks.all_topics_covered is True
