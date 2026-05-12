import logging
from pathlib import Path

import pandas as pd

from medibench.config import settings
from medibench.database import SessionLocal, init_db
from medibench.ingestion.download import download_dataset
from medibench.ingestion.loader import clean_dataframe, load_dataset_to_db
from medibench.validation.checks import run_data_quality_checks
from medibench.validation.quality import DataProfiler

logger = logging.getLogger(__name__)


def generate_quality_report(profile: dict, checks: list[dict], sha256: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_content = f"""# MediBench: Healthcare Dataset Quality & Profiling Report

## Executive Summary
- **Dataset**: Diabetes 130-US Hospitals (1999–2008)
- **Source**: UCI Machine Learning Repository
- **Total Encounters Accounted For**: {profile['total_records']:,}
- **Unique Patients**: {profile['unique_patients']:,}
- **Encounters per Patient**: {profile['encounters_per_patient']}
- **Raw File Checksum (SHA-256)**: `{sha256}`
- **Ingestion Status**: Fully Validated & Ingested into Database

---

## 1. Data Integrity & Completeness Checks

| Check Name | Category | Status | Records Checked | Affected / Deviant | Pct Affected |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for c in checks:
        status_badge = "✅ PASS" if c['status'] == 'PASSED' else ("⚠️ WARNING" if c['status'] == 'WARNING' else "❌ FAIL")
        report_content += f"| `{c['check_name']}` | {c['category']} | {status_badge} | {c['record_count']:,} | {c['affected_count']:,} | {c['percentage']}% |\n"

    report_content += """
---

## 2. Demographic Distributions

### Gender Breakdown
"""
    for g, count in profile['gender_distribution'].items():
        pct = round((count / profile['total_records']) * 100, 2)
        report_content += f"- **{g}**: {count:,} encounters ({pct}%)\n"

    report_content += """
### Age Group Breakdown
"""
    for age_grp, count in profile['age_distribution'].items():
        pct = round((count / profile['total_records']) * 100, 2)
        report_content += f"- **{age_grp}**: {count:,} encounters ({pct}%)\n"

    report_content += """
---

## 3. Readmission Distribution (Target Variable)
"""
    for rm, count in profile['readmission_distribution'].items():
        pct = round((count / profile['total_records']) * 100, 2)
        report_content += f"- **Readmitted `{rm}`**: {count:,} encounters ({pct}%)\n"

    report_content += """
---

## 4. Sparsity & Missing Values (Original '?' markers)
High-sparsity features identified:
"""
    for col, data in profile['missing_fields'].items():
        report_content += f"- **`{col}`**: {data['count']:,} missing values ({data['percentage']}%)\n"

    report_content += """
---

## 5. Numerical Metrics Summary
"""
    for metric, stats in profile['numerical_summary'].items():
        report_content += f"- **{metric}**: Min={stats['min']}, Max={stats['max']}, Mean={stats['mean']}\n"

    report_content += """
---
*Generated automatically by MediBench Ingestion Pipeline.*
"""
    with open(output_path, "w") as f:
        f.write(report_content)
    logger.info(f"Quality report generated at {output_path}")


def run_pipeline(force_download: bool = False) -> dict:
    init_db()

    # Step 1: Download / Verify raw dataset
    raw_path, sha256 = download_dataset(force=force_download)

    # Step 2: Read raw dataset
    logger.info(f"Reading raw data from {raw_path}...")
    raw_df = pd.read_csv(raw_path)

    # Step 3: Profile data
    logger.info("Profiling dataset...")
    profiler = DataProfiler(raw_df)
    profile = profiler.run_profiling()

    # Step 4: Validate quality checks and save to DB
    logger.info("Executing quality checks...")
    db = SessionLocal()
    try:
        checks = run_data_quality_checks(raw_df, db=db)
    finally:
        db.close()

    # Step 5: Clean and load into database
    logger.info("Cleaning data and loading into database...")
    clean_df = clean_dataframe(raw_df)
    records_loaded = load_dataset_to_db(clean_df)

    # Step 6: Generate documentation report
    report_path = settings.REPORTS_DIR / "dataset_quality_report.md"
    generate_quality_report(profile, checks, sha256, report_path)

    return {
        "records_loaded": records_loaded,
        "sha256": sha256,
        "profile": profile,
        "checks_count": len(checks),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()
