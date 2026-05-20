import logging

from medibench.config import settings
from medibench.database import SessionLocal
from medibench.evaluation.model_client import ModelClient
from medibench.evaluation.reports import generate_evaluation_artifacts
from medibench.evaluation.runner import EvaluationRunner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()
    try:
        # Run 1: High-Performance Healthcare LLM
        client_expert = ModelClient(model_name="MediBench-Clinical-LLM", mock_mode=True, mock_accuracy=0.92)
        runner_expert = EvaluationRunner(db=db, client=client_expert)
        res1 = runner_expert.run_evaluation(run_id="RUN-001", model_name="MediBench-Clinical-LLM")
        logger.info(f"Run 1 completed: {res1}")

        # Run 2: General Baseline LLM
        client_baseline = ModelClient(model_name="General-Baseline-LLM", mock_mode=True, mock_accuracy=0.72)
        runner_baseline = EvaluationRunner(db=db, client=client_baseline)
        res2 = runner_baseline.run_evaluation(run_id="RUN-002", model_name="General-Baseline-LLM")
        logger.info(f"Run 2 completed: {res2}")

        # Generate evaluation artifacts
        generate_evaluation_artifacts(db, settings.REPORTS_DIR)
        logger.info("Evaluation artifacts generated in reports/")

    finally:
        db.close()


if __name__ == "__main__":
    main()
