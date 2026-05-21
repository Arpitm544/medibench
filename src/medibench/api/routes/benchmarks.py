from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from medibench.benchmarks.ground_truth import RETIRED_QUESTIONS_REGISTRY
from medibench.database import BenchmarkQuestion, get_db

router = APIRouter(prefix="/api/benchmarks", tags=["benchmarks"])


@router.get("")
def list_benchmarks(
    category: str | None = Query(None, description="Filter by category"),
    difficulty: str | None = Query(None, description="Filter by difficulty"),
    db: Session = Depends(get_db),
):
    query = db.query(BenchmarkQuestion)
    if category:
        query = query.filter(BenchmarkQuestion.category == category)
    if difficulty:
        query = query.filter(BenchmarkQuestion.difficulty == difficulty)

    questions = query.all()
    return {
        "status": "success",
        "total_count": len(questions),
        "benchmarks": [
            {
                "id": q.id,
                "category": q.category,
                "difficulty": q.difficulty,
                "question": q.question,
                "evaluation_method": q.evaluation_method,
                "tolerance": q.tolerance,
                "freshness_category": q.freshness_category,
                "status": q.status,
                "has_ground_truth": len(q.answers) > 0,
            }
            for q in questions
        ],
    }


@router.get("/retired")
def list_retired_benchmarks():
    return {
        "status": "success",
        "total_count": len(RETIRED_QUESTIONS_REGISTRY),
        "retired_questions": [r.dict() for r in RETIRED_QUESTIONS_REGISTRY],
    }


@router.get("/{benchmark_id}")
def get_benchmark(benchmark_id: str, db: Session = Depends(get_db)):
    q = db.query(BenchmarkQuestion).filter(BenchmarkQuestion.id == benchmark_id).first()
    if not q:
        raise HTTPException(status_code=404, detail=f"Benchmark '{benchmark_id}' not found")

    ans = q.answers[0] if q.answers else None
    return {
        "status": "success",
        "benchmark": {
            "id": q.id,
            "category": q.category,
            "difficulty": q.difficulty,
            "question": q.question,
            "dataset_version": q.dataset_version,
            "reference_solution": q.reference_solution,
            "evaluation_method": q.evaluation_method,
            "tolerance": q.tolerance,
            "freshness_category": q.freshness_category,
            "status": q.status,
            "metadata_info": q.metadata_info,
            "verified_answer": {
                "expected_answer": ans.expected_answer if ans else None,
                "answer_type": ans.answer_type if ans else None,
                "verification_hash": ans.verification_hash if ans else None,
                "verification_notes": ans.verification_notes if ans else None,
            }
            if ans
            else None,
        },
    }
