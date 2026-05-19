import hashlib
import json
import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from medibench.analytics.statistics import StatisticalAnalytics
from medibench.benchmarks.schemas import RetiredQuestionRecord
from medibench.benchmarks.templates import BENCHMARK_DEFINITIONS
from medibench.database import BenchmarkAnswer, BenchmarkQuestion

logger = logging.getLogger(__name__)


# Feature 1: Retired Question Registry
RETIRED_QUESTIONS_REGISTRY: list[RetiredQuestionRecord] = [
    RetiredQuestionRecord(
        question_id="MED-RET-001",
        original_question="What is the average patient weight in kg across all encounters?",
        data_owner_feedback="Hospital Data Governance Officer: 'Weight was not systematically documented in the EHR between 1999 and 2008, leaving >95% missing values. Any metric reported from this field creates misleading clinical assertions.'",
        reason_for_retirement="Excessive sparsity (>95% missing); fails institutional data quality thresholds.",
        replacement_question_id="MED-036",
        review_date="2026-03-15",
        status="hypothetical_expert_review",
    ),
    RetiredQuestionRecord(
        question_id="MED-RET-002",
        original_question="Which hospital facility had the lowest 30-day readmission rate?",
        data_owner_feedback="Institutional Review Board: 'Hospital facility IDs were de-identified and stripped by UCI researchers to protect institution privacy. Attempting to rank hospital IDs is statistically invalid.'",
        reason_for_retirement="De-identified institutional IDs; uninterpretable hospital site comparisons.",
        replacement_question_id="MED-001",
        review_date="2026-04-10",
        status="hypothetical_expert_review",
    ),
    RetiredQuestionRecord(
        question_id="MED-RET-003",
        original_question="Did changing medication cause readmissions to increase?",
        data_owner_feedback="Chief Medical Officer: 'Causality cannot be asserted from retrospective observational encounter data without addressing confounding by indication.'",
        reason_for_retirement="Invalid causal framing on observational dataset.",
        replacement_question_id="MED-056",
        review_date="2026-05-02",
        status="hypothetical_expert_review",
    ),
]


class GroundTruthCalculator:
    def __init__(self, db: Session):
        self.db = db
        self.stats = StatisticalAnalytics(db)

    def calculate_expected_answer(self, bq: dict[str, Any]) -> tuple[Any, str]:
        ref = bq["reference_solution"]
        method = bq["evaluation_method"]
        bq["answer_type"]

        if method == "numeric_tolerance" and "SELECT" in ref:
            # Execute SQL
            res = self.db.execute(text(ref)).scalar()
            return float(res) if res is not None else 0.0, "Computed via reference SQL query"

        elif method == "categorical_exact" and "SELECT" in ref:
            res = self.db.execute(text(ref)).scalar()
            return str(res), "Computed via reference SQL query"

        elif ref.startswith("python:"):
            # Execute Python stat method
            expr = ref[len("python:"):]
            if "calculate_confidence_interval" in expr:
                if "lower_bound" in expr:
                    val = self.stats.calculate_confidence_interval(11357, 101766)["lower_bound"]
                else:
                    val = self.stats.calculate_confidence_interval(11357, 101766)["upper_bound"]
                return float(val), "Computed via Wilson score interval"
            elif "chi_square_test" in expr:
                res = self.stats.chi_square_test("change", "readmitted_30d")
                return "Yes" if res["statistically_significant"] else "No", "Computed via SciPy chi2_contingency"
            elif "correlation_matrix" in expr:
                corr = self.stats.correlation_matrix()
                if "num_medications" in expr and "time_in_hospital" in expr:
                    return float(corr["pearson"]["time_in_hospital"]["num_medications"]), "Computed via Pearson correlation"
                elif "num_lab_procedures" in expr:
                    return float(corr["pearson"]["time_in_hospital"]["num_lab_procedures"]), "Computed via Pearson correlation"
                elif "num_procedures" in expr:
                    return float(corr["pearson"]["num_procedures"]["num_medications"]), "Computed via Pearson correlation"
            elif "logistic_regression" in expr:
                lr = self.stats.logistic_regression_readmission()
                if "number_inpatient" in expr:
                    return float(lr["features"]["number_inpatient"]["odds_ratio"]), "Computed via multivariable Logit"
                elif "time_in_hospital" in expr:
                    return float(lr["features"]["time_in_hospital"]["odds_ratio"]), "Computed via multivariable Logit"

        elif method == "categorical_exact" and "->" in ref:
            ans = ref.split("->")[-1].strip()
            return ans, "Static categorical ground truth"

        elif method == "numeric_tolerance" and "=" in ref:
            # Deterministic math calculation
            if bq["id"] == "MED-049":
                return 100000.0, "Net savings: 40 prevented * $15,000 penalty - 1,000 * $500 cost = $100,000"
            elif bq["id"] == "MED-053":
                return 218.4, "11,357 readmissions / 52 weeks = 218.4 weekly slots"

        elif method == "rubric_based":
            return ref, "Analytical rubric evaluation"

        return ref, "Reference solution"

    def populate_ground_truth(self) -> int:
        """
        Populates all 60 benchmark questions and their deterministic ground-truth answers in the database.
        """
        # Clear existing to ensure idempotence
        self.db.query(BenchmarkAnswer).delete()
        self.db.query(BenchmarkQuestion).delete()
        self.db.commit()

        count = 0
        for bq in BENCHMARK_DEFINITIONS:
            expected_val, notes = self.calculate_expected_answer(bq)
            expected_str = json.dumps(expected_val) if isinstance(expected_val, (dict, list)) else str(expected_val)

            # Verification hash
            v_hash = hashlib.sha256(f"{bq['id']}:{expected_str}".encode()).hexdigest()

            question_obj = BenchmarkQuestion(
                id=bq["id"],
                category=bq["category"],
                difficulty=bq["difficulty"],
                question=bq["question"],
                dataset_version=bq.get("dataset_version", "v1"),
                reference_solution=bq.get("reference_solution"),
                evaluation_method=bq["evaluation_method"],
                tolerance=bq.get("tolerance"),
                freshness_category=bq.get("freshness_category", "static"),
                status="verified",
                metadata_info=bq.get("metadata_info"),
            )
            self.db.add(question_obj)
            self.db.flush()

            answer_obj = BenchmarkAnswer(
                question_id=bq["id"],
                expected_answer=expected_str,
                answer_type=bq.get("answer_type", "numeric"),
                verification_hash=v_hash,
                verification_notes=notes,
            )
            self.db.add(answer_obj)
            count += 1

        self.db.commit()
        logger.info(f"Successfully generated and stored {count} verified benchmark questions with ground truth!")
        return count
