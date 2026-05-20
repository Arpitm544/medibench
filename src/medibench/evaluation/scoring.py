import re
from typing import Any


class ScoringEngine:
    """
    Evaluates AI model responses against deterministic ground-truth answers using
    numeric tolerance, categorical matching, SQL result equivalence, or structured rubrics.
    """

    @staticmethod
    def extract_first_number(text_str: str) -> float | None:
        if text_str is None:
            return None
        # Clean currency and percentage signs
        clean = text_str.replace(",", "").replace("$", "").replace("%", " ")
        # Match floats, integers, or negatives
        match = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", clean)
        if match:
            try:
                return float(match.group(0))
            except ValueError:
                return None
        return None

    @classmethod
    def score_numeric(
        cls, predicted_text: str, expected_val: float, tolerance: float | None = 0.05
    ) -> tuple[float, str, str | None]:
        predicted_num = cls.extract_first_number(predicted_text)
        if predicted_num is None:
            return 0.0, "failed", "PARSE_ERROR: No numerical value could be extracted from response."

        tol = tolerance if tolerance is not None else 0.05
        # Absolute or relative tolerance check
        abs_diff = abs(predicted_num - expected_val)
        allowed_delta = max(tol, tol * abs(expected_val))

        if abs_diff <= allowed_delta:
            return 1.0, "passed", None
        else:
            return 0.0, "failed", f"NUMERICAL_DEVIATION: Expected {expected_val}, extracted {predicted_num} (diff: {round(abs_diff, 4)} > tol {allowed_delta})"

    @classmethod
    def score_categorical(cls, predicted_text: str, expected_val: str) -> tuple[float, str, str | None]:
        if not predicted_text:
            return 0.0, "failed", "EMPTY_RESPONSE"

        norm_pred = predicted_text.strip().lower()
        norm_exp = expected_val.strip().lower()

        # Check exact or contained match
        if norm_exp in norm_pred:
            return 1.0, "passed", None
        return 0.0, "failed", f"CATEGORICAL_MISMATCH: Expected '{expected_val}', got '{predicted_text[:100]}'"

    @classmethod
    def score_rubric(
        cls, predicted_text: str, expected_ref: str, metadata: dict[str, Any] | None = None
    ) -> tuple[float, str, str | None]:
        if not predicted_text or len(predicted_text.strip()) < 5:
            return 0.0, "failed", "INSUFFICIENT_RESPONSE"

        norm_pred = predicted_text.lower()
        required_concepts = metadata.get("required_concepts", []) if metadata else []

        if not required_concepts:
            # Fallback to key terms from reference
            ref_words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{4,}\b", expected_ref)]
            matches = sum(1 for w in set(ref_words) if w in norm_pred)
            ratio = matches / max(len(set(ref_words)), 1)
            score = 1.0 if ratio >= 0.3 else 0.5 if ratio >= 0.15 else 0.0
            status = "passed" if score >= 0.7 else "partial" if score > 0 else "failed"
            return score, status, None

        matched_concepts = [c for c in required_concepts if c.lower() in norm_pred]
        match_ratio = len(matched_concepts) / len(required_concepts)

        if match_ratio >= 0.6:
            return 1.0, "passed", None
        elif match_ratio >= 0.3:
            return 0.5, "passed", f"PARTIAL_CONCEPTS_MATCHED: {matched_concepts} of {required_concepts}"
        else:
            return 0.0, "failed", f"MISSING_REQUIRED_CONCEPTS: Missed {[c for c in required_concepts if c not in matched_concepts]}"

    @classmethod
    def evaluate(
        cls,
        evaluation_method: str,
        predicted_answer: str,
        expected_answer_str: str,
        tolerance: float | None = 0.05,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            if evaluation_method == "numeric_tolerance":
                expected_num = float(expected_answer_str)
                score, status, err = cls.score_numeric(predicted_answer, expected_num, tolerance)
            elif evaluation_method in ["categorical_exact", "sql_execution"]:
                score, status, err = cls.score_categorical(predicted_answer, expected_answer_str)
            elif evaluation_method == "rubric_based":
                score, status, err = cls.score_rubric(predicted_answer, expected_answer_str, metadata)
            else:
                score, status, err = cls.score_categorical(predicted_answer, expected_answer_str)

            return {
                "score": float(score),
                "status": status,
                "error_message": err,
            }
        except Exception as e:
            return {
                "score": 0.0,
                "status": "error",
                "error_message": f"SCORING_EXCEPTION: {e!s}",
            }
