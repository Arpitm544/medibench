from typing import Any

import pandas as pd
from sqlalchemy.orm import Session

from medibench.database import DataQualityResult


def run_data_quality_checks(df: pd.DataFrame, db: Session = None) -> list[dict[str, Any]]:
    total = len(df)
    results = []

    # Check 1: Record count == 101,766
    status = "PASSED" if total == 101766 else "WARNING"
    results.append({
        "check_name": "total_record_count",
        "category": "completeness",
        "status": status,
        "record_count": total,
        "affected_count": abs(total - 101766),
        "percentage": 100.0 if total == 101766 else round((total / 101766) * 100, 2),
        "details": {"expected": 101766, "actual": total},
    })

    # Check 2: Encounter uniqueness
    dup_enc = int(df["encounter_id"].duplicated().sum())
    results.append({
        "check_name": "encounter_id_uniqueness",
        "category": "integrity",
        "status": "PASSED" if dup_enc == 0 else "FAILED",
        "record_count": total,
        "affected_count": dup_enc,
        "percentage": round((dup_enc / total) * 100, 4),
        "details": {"duplicate_count": dup_enc},
    })

    # Check 3: Missing weight percentage
    weight_missing = int(((df["weight"] == "?") | df["weight"].isna()).sum())
    weight_pct = round((weight_missing / total) * 100, 2)
    results.append({
        "check_name": "weight_sparsity_check",
        "category": "sparsity",
        "status": "WARNING" if weight_pct > 90.0 else "PASSED",
        "record_count": total,
        "affected_count": weight_missing,
        "percentage": weight_pct,
        "details": {"notes": "Weight is missing in >95% encounters; recommended to exclude from primary models"},
    })

    # Check 4: Missing medical_specialty percentage
    spec_missing = int(((df["medical_specialty"] == "?") | df["medical_specialty"].isna()).sum())
    spec_pct = round((spec_missing / total) * 100, 2)
    results.append({
        "check_name": "medical_specialty_sparsity",
        "category": "sparsity",
        "status": "WARNING" if spec_pct > 40.0 else "PASSED",
        "record_count": total,
        "affected_count": spec_missing,
        "percentage": spec_pct,
        "details": {"missing_count": spec_missing, "sparsity_pct": spec_pct},
    })

    # Check 5: Invalid gender entries
    invalid_gender = int(df["gender"].isin(["Unknown/Invalid"]).sum())
    results.append({
        "check_name": "gender_validity",
        "category": "validity",
        "status": "PASSED" if invalid_gender < 10 else "WARNING",
        "record_count": total,
        "affected_count": invalid_gender,
        "percentage": round((invalid_gender / total) * 100, 4),
        "details": {"invalid_records": invalid_gender},
    })

    # Check 6: Time in hospital range [1, 14]
    invalid_stay = int(((df["time_in_hospital"] < 1) | (df["time_in_hospital"] > 14)).sum())
    results.append({
        "check_name": "time_in_hospital_range",
        "category": "range",
        "status": "PASSED" if invalid_stay == 0 else "FAILED",
        "record_count": total,
        "affected_count": invalid_stay,
        "percentage": round((invalid_stay / total) * 100, 4),
        "details": {"min": int(df["time_in_hospital"].min()), "max": int(df["time_in_hospital"].max())},
    })

    # Check 7: Readmitted domain validity
    valid_readmit = {"<30", ">30", "NO"}
    invalid_readmit = int((~df["readmitted"].isin(valid_readmit)).sum())
    results.append({
        "check_name": "readmitted_values_validity",
        "category": "validity",
        "status": "PASSED" if invalid_readmit == 0 else "FAILED",
        "record_count": total,
        "affected_count": invalid_readmit,
        "percentage": round((invalid_readmit / total) * 100, 4),
        "details": {"valid_domain": list(valid_readmit)},
    })

    # Persist to DB if session provided
    if db:
        # Clear existing quality results to allow idempotent runs
        db.query(DataQualityResult).delete()
        for r in results:
            dqr = DataQualityResult(**r)
            db.add(dqr)
        db.commit()

    return results
