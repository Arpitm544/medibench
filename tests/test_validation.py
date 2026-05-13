import pandas as pd

from medibench.validation.checks import run_data_quality_checks
from medibench.validation.quality import DataProfiler


def test_profiler_and_checks():
    df = pd.DataFrame({
        "encounter_id": [1, 2, 3],
        "patient_nbr": [10, 20, 10],  # 1 repeated patient
        "race": ["Caucasian", "AfricanAmerican", "?"],
        "gender": ["Female", "Male", "Unknown/Invalid"],
        "age": ["[50-60)", "[60-70)", "[70-80)"],
        "weight": ["?", "?", "?"],
        "time_in_hospital": [2, 5, 8],
        "medical_specialty": ["InternalMedicine", "?", "?"],
        "num_lab_procedures": [20, 30, 40],
        "num_procedures": [0, 1, 2],
        "num_medications": [5, 12, 18],
        "number_diagnoses": [4, 6, 9],
        "readmitted": ["<30", ">30", "NO"],
    })

    profiler = DataProfiler(df)
    profile = profiler.run_profiling()

    assert profile["total_records"] == 3
    assert profile["unique_patients"] == 2
    assert profile["duplicate_encounters"] == 0
    assert profile["invalid_gender_records"] == 1
    assert "weight" in profile["missing_fields"]
    assert profile["missing_fields"]["weight"]["count"] == 3

    checks = run_data_quality_checks(df)
    check_names = {c["check_name"] for c in checks}
    assert "total_record_count" in check_names
    assert "encounter_id_uniqueness" in check_names
    assert "weight_sparsity_check" in check_names
    assert "readmitted_values_validity" in check_names
