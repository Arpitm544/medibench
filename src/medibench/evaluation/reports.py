import json
import logging
from pathlib import Path

from sqlalchemy.orm import Session

from medibench.database import EvaluationResult, EvaluationRun

logger = logging.getLogger(__name__)


def generate_evaluation_artifacts(db: Session, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    runs = db.query(EvaluationRun).all()

    # 1. Export evaluation_results.json
    all_runs_data = []
    for r in runs:
        results = db.query(EvaluationResult).filter(EvaluationResult.run_id == r.id).all()
        run_data = {
            "run_id": r.id,
            "model_name": r.model_name,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "total_questions": r.total_questions,
            "passed_questions": r.passed_questions,
            "overall_score_pct": r.overall_score,
            "results": [
                {
                    "benchmark_id": res.benchmark_id,
                    "model": res.model,
                    "score": res.score,
                    "status": res.status,
                    "latency_ms": res.latency_ms,
                    "tokens_used": res.tokens_used,
                    "error_message": res.error_message,
                }
                for res in results
            ],
        }
        all_runs_data.append(run_data)

    json_path = output_dir / "evaluation_results.json"
    with open(json_path, "w") as f:
        json.dump(all_runs_data, f, indent=2)
    logger.info(f"Evaluation JSON saved to {json_path}")

    # 2. Export reports/model_comparison.md
    md_lines = [
        "# MediBench: AI Model Evaluation & Comparison Report",
        "",
        "## Executive Summary",
        "This report evaluates AI model capabilities across 60 rigorous healthcare analytics benchmark questions grounded in 101,766 hospital encounters.",
        "",
        "| Run ID | Model Name | Evaluated Questions | Passed | Overall Score (%) | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for r in runs:
        md_lines.append(f"| `{r.id}` | **{r.model_name}** | {r.total_questions} | {r.passed_questions} | **{r.overall_score}%** | `{r.status}` |")

    md_lines.extend([
        "",
        "---",
        "",
        "## Performance by Category Breakdown",
        "",
    ])

    for r in runs:
        results = db.query(EvaluationResult).filter(EvaluationResult.run_id == r.id).all()
        cat_scores = {}
        cat_totals = {}
        for res in results:
            res.benchmark_id[:3]  # category grouping
            cat_totals[res.benchmark_id] = cat_totals.get(res.benchmark_id, 0) + 1
            cat_scores[res.status] = cat_scores.get(res.status, 0) + 1

        avg_lat = round(sum((res.latency_ms or 0) for res in results) / max(len(results), 1), 1)
        tot_tokens = sum((res.tokens_used or 0) for res in results)

        md_lines.extend([
            f"### Model: {r.model_name} (`{r.id}`)",
            f"- **Average Question Latency**: {avg_lat} ms",
            f"- **Total Tokens Utilized**: {tot_tokens:,}",
            f"- **Passed**: {cat_scores.get('passed', 0)} / {len(results)} ({r.overall_score}%)",
            f"- **Failed / Deviations**: {cat_scores.get('failed', 0)}",
            "",
        ])

    md_lines.extend([
        "---",
        "*Report generated deterministically by MediBench Evaluation Suite.*",
    ])

    md_path = output_dir / "model_comparison.md"
    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))
    logger.info(f"Model comparison report saved to {md_path}")
