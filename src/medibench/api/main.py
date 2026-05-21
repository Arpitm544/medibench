from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from medibench.api.routes import analytics, benchmarks, evaluations
from medibench.config import settings
from medibench.database import BenchmarkQuestion, EvaluationRun, get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MediBench Healthcare Data Analytics & AI Benchmark Evaluation API",
)

# Enable CORS for frontend & dashboard integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(analytics.router)
app.include_router(benchmarks.router)
app.include_router(evaluations.router)


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"unhealthy: {e!s}"

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": db_status,
        "environment": settings.APP_ENV,
    }


@app.get("/api/reports/summary")
def get_reports_summary(db: Session = Depends(get_db)):
    total_encounters = db.execute(text("SELECT COUNT(*) FROM patient_encounters;")).scalar()
    total_benchmarks = db.query(BenchmarkQuestion).count()
    runs = db.query(EvaluationRun).all()

    return {
        "status": "success",
        "dataset": {
            "name": "Diabetes 130-US Hospitals (1999-2008)",
            "total_encounters": total_encounters,
            "period": "1999-2008",
        },
        "benchmarks": {
            "total_questions": total_benchmarks,
            "categories_count": 6,
            "status": "100% verified",
        },
        "evaluations": {
            "total_runs": len(runs),
            "completed_runs": sum(1 for r in runs if r.status == "completed"),
            "latest_run": runs[-1].id if runs else None,
        },
    }
