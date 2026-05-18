from enum import Enum
from typing import Any

from pydantic import BaseModel


class BenchmarkCategory(str, Enum):
    SQL_ANALYTICS = "sql_analytics"
    STATISTICAL_REASONING = "statistical_reasoning"
    DATA_INTERPRETATION = "data_interpretation"
    DATA_QUALITY = "data_quality"
    BUSINESS_DECISION_MAKING = "business_decision_making"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class FreshnessCategory(str, Enum):
    STATIC = "static"
    SLOWLY_CHANGING = "slowly_changing"
    FREQUENTLY_CHANGING = "frequently_changing"
    LIVE_DEPENDENT = "live_dependent"


class EvaluationMethod(str, Enum):
    NUMERIC_TOLERANCE = "numeric_tolerance"
    SQL_EXECUTION = "sql_execution"
    RUBRIC_BASED = "rubric_based"
    CATEGORICAL_EXACT = "categorical_exact"


class BenchmarkQuestionSchema(BaseModel):
    id: str
    category: BenchmarkCategory
    difficulty: DifficultyLevel
    question: str
    dataset_version: str = "v1"
    reference_solution: str | None = None
    evaluation_method: EvaluationMethod
    tolerance: float | None = 0.01
    freshness_category: FreshnessCategory = FreshnessCategory.STATIC
    status: str = "verified"
    metadata_info: dict[str, Any] | None = None


class BenchmarkAnswerSchema(BaseModel):
    question_id: str
    expected_answer: float | int | str | dict
    answer_type: str
    verification_hash: str | None = None
    verification_notes: str | None = None


class RetiredQuestionRecord(BaseModel):
    question_id: str
    original_question: str
    data_owner_feedback: str
    reason_for_retirement: str
    replacement_question_id: str | None = None
    review_date: str
    status: str = "retired"  # 'hypothetical_expert_review' or 'verified_data_owner'
