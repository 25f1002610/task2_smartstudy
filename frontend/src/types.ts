export interface StudyPlanRequest {
  subject: string;
  exam_in_days: number;
  current_level: 'Beginner' | 'Intermediate' | 'Advanced';
  topics: string[];
  hours_per_day: number;
  preferences?: string;
  constraints?: string;
}

export interface DayPlan {
  day: number;
  primary_focus: string;
  tasks: string[];
  learning_objectives: string[];
  practice_tasks: string[];
  problem_count: number;
  revision_tasks: string;
  study_hours: number;
  practice_hours: number;
  total_hours: number;
  is_final_prep: boolean;
}

export interface TopicItem {
  topic_name: string;
  priority: 'High' | 'Medium' | 'Low';
  difficulty: 'Easy' | 'Medium' | 'Hard';
  learning_focus: string;
  recommended_study_duration_hours?: number;
}

export interface PracticeItem {
  topic_name: string;
  recommended_problem_count: number;
  practice_type: string;
  expected_duration_hours?: number;
  rationale: string;
}

export interface CriteriaChecks {
  all_topics_covered: boolean;
  time_constraints_respected: boolean;
  sufficient_practice_included: boolean;
  revision_included: boolean;
  final_day_appropriate: boolean;
}

export interface ReviewFeedback {
  approved: boolean;
  criteria_checks?: CriteriaChecks;
  issues?: string[];
  required_changes?: string[];
  iteration?: number;
  evaluation_notes?: string;
}

export interface StructuredData {
  draft_plan?: {
    subject?: string;
    exam_in_days?: number;
    current_level?: string;
    hours_per_day?: number;
    covered_topics?: string[];
    plan_overview?: string;
    day_by_day_plan?: DayPlan[];
    total_practice_problems?: number;
    total_study_hours?: number;
    iteration?: number;
  };
  review_feedback?: ReviewFeedback;
  topic_analysis?: {
    subject?: string;
    topics?: TopicItem[];
    summary?: string;
  };
  practice_plan?: {
    subject?: string;
    topic_practice?: PracticeItem[];
    total_practice_problems?: number;
    total_practice_hours?: number;
    mock_test_recommended?: boolean;
  };
  schedule_plan?: {
    subject?: string;
    total_days?: number;
    max_daily_hours_allowed?: number;
    daily_schedule?: any[];
  };
}

export interface SummaryMetrics {
  subject: string;
  exam_in_days: number;
  current_level: string;
  hours_per_day: number;
  total_study_hours: number;
  topics_count: number;
  review_status: string;
}

export interface StudyPlanResponse {
  success: boolean;
  session_id: string;
  phases_executed: string[];
  final_markdown: string;
  structured_data: StructuredData;
  summary_metrics: SummaryMetrics;
}
