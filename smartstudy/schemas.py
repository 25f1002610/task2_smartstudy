"""Pydantic schemas and output contracts for SmartStudy Multi-Agent Planner."""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class StudentRequirements(BaseModel):
    """Normalized student request extracted by Coordinator Agent."""
    subject: str = Field(description="Subject name, e.g. Data Structures")
    exam_in_days: int = Field(ge=1, description="Days remaining until the exam")
    current_level: str = Field(description="Proficiency level: Beginner, Intermediate, or Advanced")
    topics: List[str] = Field(min_length=1, description="List of topics to cover")
    hours_per_day: float = Field(gt=0, le=24, description="Available study hours per day")
    preferences: Optional[str] = Field(default=None, description="Preferred order or weak topic preferences")
    constraints: Optional[str] = Field(default=None, description="Any explicit constraints stated by the student")
    is_valid: bool = Field(default=True, description="Whether essential inputs were provided")
    missing_fields: List[str] = Field(default_factory=list, description="List of any missing essential fields")


class PlanningBrief(BaseModel):
    """Structured planning brief produced by Planning Agent."""
    subject: str = Field(description="Subject name")
    exam_in_days: int = Field(description="Days remaining")
    current_level: str = Field(description="Proficiency level")
    topics: List[str] = Field(description="List of topics")
    hours_per_day: float = Field(description="Hours available per day")
    total_available_hours: float = Field(description="Total study budget (days * hours/day)")
    strategy_summary: str = Field(description="High level strategy and pacing")
    guidelines_for_specialists: str = Field(description="Specific directions for topic, practice, and schedule agents")


class TopicAnalysisItem(BaseModel):
    """Analysis for an individual topic."""
    topic_name: str = Field(description="Name of the topic")
    priority: str = Field(description="Priority level: High, Medium, or Low")
    difficulty: str = Field(description="Relative difficulty: Easy, Medium, or Hard")
    learning_focus: str = Field(description="Key concepts and learning focus")
    recommended_study_duration_hours: float = Field(gt=0, description="Recommended hours for learning this topic")


class TopicAnalysis(BaseModel):
    """Output contract for Topic Agent."""
    subject: str = Field(description="Subject name")
    topics: List[TopicAnalysisItem] = Field(description="Detailed analysis for every topic")
    summary: str = Field(description="Overview of curriculum difficulty and sequencing")


class PracticePlanItem(BaseModel):
    """Practice recommendation for an individual topic."""
    topic_name: str = Field(description="Name of the topic")
    recommended_problem_count: int = Field(ge=1, description="Recommended count of problems")
    practice_type: str = Field(description="Type: concept questions, coding problems, mixed practice, or mock tests")
    expected_duration_hours: float = Field(gt=0, description="Expected time required for practice")
    rationale: str = Field(description="Rationale based on difficulty and student proficiency")


class PracticePlan(BaseModel):
    """Output contract for Practice Agent."""
    subject: str = Field(description="Subject name")
    topic_practice: List[PracticeItem] = Field(default_factory=list, description="Practice recommendations per topic")
    total_practice_problems: int = Field(default=0, description="Total problem count across all topics")
    total_practice_hours: float = Field(default=0.0, description="Total practice duration")
    mock_test_recommended: bool = Field(default=True, description="Whether a comprehensive mock test is included")


# Alias PracticeItem to PracticePlanItem for compatibility
PracticeItem = PracticePlanItem


class DayScheduleItem(BaseModel):
    """Daily schedule breakdown produced by Schedule Agent."""
    day: int = Field(ge=1, description="Day number (1-indexed)")
    topics_and_tasks: List[str] = Field(description="List of specific study tasks")
    study_duration_hours: float = Field(ge=0, description="Hours allocated to new concept learning")
    practice_duration_hours: float = Field(ge=0, description="Hours allocated to practice problems")
    revision_activity: str = Field(description="Active recall or revision activity")
    daily_total_hours: float = Field(gt=0, description="Sum of study + practice hours")
    is_final_prep: bool = Field(default=False, description="Whether this day is reserved for final review / mock test")


class SchedulePlan(BaseModel):
    """Output contract for Schedule Agent."""
    subject: str = Field(description="Subject name")
    total_days: int = Field(description="Total days scheduled")
    max_daily_hours_allowed: float = Field(description="Stated daily hour limit")
    daily_schedule: List[DayScheduleItem] = Field(description="Day-by-day plan")
    total_scheduled_hours: float = Field(description="Sum of all daily hours")
    schedule_strategy: str = Field(description="Explanation of pacing and rest/revision buffers")

    @model_validator(mode="after")
    def validate_daily_limits(self) -> SchedulePlan:
        for day_item in self.daily_schedule:
            if day_item.daily_total_hours > self.max_daily_hours_allowed + 0.05:  # small float tolerance
                raise ValueError(
                    f"Day {day_item.day} total hours ({day_item.daily_total_hours}h) exceeds "
                    f"stated limit ({self.max_daily_hours_allowed}h)"
                )
        return self


class DetailedDayPlan(BaseModel):
    """Day plan included in the complete Study Plan Draft."""
    day: int = Field(ge=1, description="Day number")
    primary_focus: str = Field(description="Main topic or focus for the day")
    tasks: List[str] = Field(description="Actionable study tasks")
    learning_objectives: List[str] = Field(description="Key concepts to master")
    practice_tasks: List[str] = Field(description="Specific practice problems or coding exercises")
    problem_count: int = Field(ge=0, description="Target problem count for today")
    revision_tasks: str = Field(description="Revision or active recall activity")
    study_hours: float = Field(ge=0, description="Study hours")
    practice_hours: float = Field(ge=0, description="Practice hours")
    total_hours: float = Field(gt=0, description="Daily total hours")
    is_final_prep: bool = Field(default=False, description="True if final review / mock test day")


class StudyPlanDraft(BaseModel):
    """Complete draft study plan synthesized by Study Plan Writer Agent."""
    subject: str = Field(description="Subject name")
    exam_in_days: int = Field(description="Number of days")
    current_level: str = Field(description="Current level")
    hours_per_day: float = Field(description="Hours per day")
    covered_topics: List[str] = Field(description="All topics covered in this plan")
    plan_overview: str = Field(description="Executive summary of the study plan")
    day_by_day_plan: List[DetailedDayPlan] = Field(description="Day-by-day schedule")
    total_practice_problems: int = Field(description="Total problem count")
    total_study_hours: float = Field(description="Grand total hours")
    iteration: int = Field(default=1, description="Draft iteration number (1 or 2)")


class CriteriaChecks(BaseModel):
    """Checks for the 5 mandatory quality criteria."""
    all_topics_covered: bool = Field(description="1. Are all supplied topics covered?")
    time_constraints_respected: bool = Field(description="2. Does schedule fit within available time and daily limit?")
    sufficient_practice_included: bool = Field(description="3. Is sufficient practice included?")
    revision_included: bool = Field(description="4. Is revision included throughout the plan?")
    final_day_appropriate: bool = Field(description="5. Is the final day appropriate for exam preparation?")


class ReviewFeedback(BaseModel):
    """Structured feedback produced by Review Agent."""
    approved: bool = Field(description="True if draft passes all 5 criteria, False otherwise")
    criteria_checks: CriteriaChecks = Field(description="Individual checks for the 5 criteria")
    issues: List[str] = Field(default_factory=list, description="List of concrete deficiencies found")
    required_changes: List[str] = Field(default_factory=list, description="Specific corrections required")
    iteration: int = Field(description="Current review iteration number (1 or 2)")
    evaluation_notes: str = Field(description="Summary of reviewer evaluation")


class FinalStudyPlan(BaseModel):
    """Final presentation plan produced by Final Response Agent."""
    subject: str = Field(description="Subject name")
    exam_in_days: int = Field(description="Total days")
    current_level: str = Field(description="Level")
    hours_per_day: float = Field(description="Daily hours limit")
    total_hours: float = Field(description="Total study hours")
    total_practice_problems: int = Field(description="Total practice problems")
    covered_topics: List[str] = Field(description="All covered topics")
    review_status: str = Field(description="'APPROVED' or 'REVISED_WITH_REMARKS'")
    review_iteration: int = Field(description="Total review iterations completed")
    review_summary: str = Field(description="Summary of review evaluation")
    day_by_day_plan: List[DetailedDayPlan] = Field(description="Day cards data")
    markdown_presentation: str = Field(description="Beautiful human-readable Markdown output")
