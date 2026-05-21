from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from medibench.database import EvaluationResult, EvaluationRun, SessionLocal, get_db
from medibench.evaluation.model_client import ModelClient
from medibench.evaluation.runner import EvaluationRunner

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])


class EvaluationRequest(BaseModel):
    model_name: str = "gpt-4o-mini"
    category: str | None = None
    mock_mode: bool = True
    mock_accuracy: float = 0.85


def run_evaluation_background(run_id: str, model_name: str, category: str | None, mock_mode: bool, mock_accuracy: float):
    db = SessionLocal()
    try:
        client = ModelClient(model_name=model_name, mock_mode=mock_mode, mock_accuracy=mock_accuracy)
        runner = EvaluationRunner(db=db, client=client)
        runner.run_evaluation(run_id=run_id, model_name=model_name, category=category)
    finally:
        db.close()


@router.post("")
def start_evaluation(
    request: EvaluationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    run_id = f"RUN-{timestamp}"

    # Initialize record
    run_obj = EvaluationRun(
        id=run_id,
        model_name=request.model_name,
        started_at=datetime.utcnow(),
        status="queued",
        config=request.dict(),
    )
    db.add(run_obj)
    db.commit()

    # Enqueue background worker
    background_tasks.add_task(
        run_evaluation_background,
        run_id=run_id,
        model_name=request.model_name,
        category=request.category,
        mock_mode=request.mock_mode,
        mock_accuracy=request.mock_accuracy,
    )

    return {
        "status": "success",
        "message": f"Evaluation '{run_id}' has been queued.",
        "run_id": run_id,
        "model_name": request.model_name,
    }


@router.get("")
def list_evaluations(db: Session = Depends(get_db)):
    runs = db.query(EvaluationRun).order_by(EvaluationRun.started_at.desc()).all()
    return {
        "status": "success",
        "total_runs": len(runs),
        "runs": [
            {
                "run_id": r.id,
                "model_name": r.model_name,
                "status": r.status,
                "total_questions": r.total_questions,
                "passed_questions": r.passed_questions,
                "overall_score": r.overall_score,
                "started_at": r.started_at,
                "completed_at": r.completed_at,
            }
            for r in runs
        ],
    }


@router.get("/{run_id}")
def get_evaluation_status(run_id: str, db: Session = Depends(get_db)):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail=f"Evaluation run '{run_id}' not found")

    return {
        "status": "success",
        "run_id": run.id,
        "model_name": run.model_name,
        "execution_status": run.status,
        "total_questions": run.total_questions,
        "passed_questions": run.passed_questions,
        "overall_score": run.overall_score,
        "started_at": run.started_at,
        "completed_at": run.completed_at,
    }


@router.get("/{run_id}/results")
def get_evaluation_results(run_id: str, db: Session = Depends(get_db)):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail=f"Evaluation run '{run_id}' not found")

    results = db.query(EvaluationResult).filter(EvaluationResult.run_id == run_id).all()
    return {
        "status": "success",
        "run_id": run_id,
        "model_name": run.model_name,
        "overall_score": run.overall_score,
        "total_results": len(results),
        "results": [
            {
                "benchmark_id": res.benchmark_id,
                "score": res.score,
                "status": res.status,
                "latency_ms": res.latency_ms,
                "tokens_used": res.tokens_used,
                "predicted_answer": res.predicted_answer,
                "expected_answer": res.expected_answer,
                "error_message": res.error_message,
            }
            for res in results
        ],
    }
