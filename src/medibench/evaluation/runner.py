import logging
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from medibench.database import (
    BenchmarkQuestion,
    EvaluationResult,
    EvaluationRun,
)
from medibench.evaluation.model_client import ModelClient
from medibench.evaluation.scoring import ScoringEngine

logger = logging.getLogger(__name__)


class EvaluationRunner:
    def __init__(self, db: Session, client: ModelClient | None = None):
        self.db = db
        self.client = client or ModelClient(mock_mode=True, mock_accuracy=0.88)

    def run_evaluation(
        self,
        run_id: str | None = None,
        model_name: str | None = None,
        category: str | None = None,
    ) -> dict[str, Any]:
        """
        Executes an evaluation run across all or filtered benchmark questions.
        """
        model_name = model_name or self.client.model_name
        if not run_id:
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            run_id = f"RUN-{timestamp}"

        # Fetch benchmark questions
        query = self.db.query(BenchmarkQuestion)
        if category:
            query = query.filter(BenchmarkQuestion.category == category)
        questions = query.all()

        if not questions:
            raise ValueError("No benchmark questions found to evaluate!")

        logger.info(f"Starting evaluation run {run_id} for model '{model_name}' on {len(questions)} questions...")

        run_obj = EvaluationRun(
            id=run_id,
            model_name=model_name,
            started_at=datetime.utcnow(),
            status="running",
            total_questions=len(questions),
            config={"mock_mode": self.client.mock_mode, "category_filter": category},
        )
        self.db.add(run_obj)
        self.db.commit()

        total_score = 0.0
        passed_count = 0
        results_list = []

        for q in questions:
            expected_answer_str = q.answers[0].expected_answer if q.answers else None

            # Prompt model without leaking answer
            model_out = self.client.query(
                question_text=q.question,
                expected_ground_truth=expected_answer_str,
            )

            # Evaluate with ScoringEngine
            eval_score = ScoringEngine.evaluate(
                evaluation_method=q.evaluation_method,
                predicted_answer=model_out["response"],
                expected_answer_str=expected_answer_str or "",
                tolerance=q.tolerance,
                metadata=q.metadata_info,
            )

            score = eval_score["score"]
            status = eval_score["status"]

            total_score += score
            if status == "passed":
                passed_count += 1

            result_entry = EvaluationResult(
                run_id=run_id,
                benchmark_id=q.id,
                model=model_name,
                expected_answer=expected_answer_str,
                predicted_answer=model_out["response"],
                score=score,
                latency_ms=model_out["latency_ms"],
                tokens_used=model_out["tokens_used"],
                status=status,
                evaluation_details=eval_score,
                error_message=eval_score.get("error_message"),
            )
            self.db.add(result_entry)
            results_list.append(result_entry)

        # Update run summary
        run_obj.completed_at = datetime.utcnow()
        run_obj.status = "completed"
        run_obj.passed_questions = passed_count
        run_obj.overall_score = round((total_score / len(questions)) * 100.0, 2)
        self.db.commit()

        logger.info(f"Evaluation run {run_id} completed: score = {run_obj.overall_score}%, passed = {passed_count}/{len(questions)}")

        return {
            "run_id": run_id,
            "model_name": model_name,
            "total_questions": len(questions),
            "passed_questions": passed_count,
            "overall_score_pct": run_obj.overall_score,
            "status": run_obj.status,
        }
