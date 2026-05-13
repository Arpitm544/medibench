from typing import Any

import pandas as pd


class DataProfiler:
    def __init__(self, df: pd.DataFrame):
        self.raw_df = df

    def run_profiling(self) -> dict[str, Any]:
        df = self.raw_df
        total_records = len(df)

        # 1. Missing / Unknown values ('?' or None)
        missing_counts = {}
        for col in df.columns:
            count = int(((df[col] == "?") | df[col].isna()).sum())
            if count > 0:
                missing_counts[col] = {
                    "count": count,
                    "percentage": round((count / total_records) * 100, 2),
                }

        # 2. Duplicate Encounter IDs
        dup_encounters = int(df["encounter_id"].duplicated().sum())

        # 3. Patient Counts
        unique_patients = int(df["patient_nbr"].nunique())
        encounters_per_patient = round(total_records / unique_patients, 2)

        # 4. Gender distribution
        gender_dist = df["gender"].value_counts().to_dict()
        invalid_gender_count = int(df["gender"].isin(["Unknown/Invalid"]).sum())

        # 5. Readmission distribution
        readmission_dist = df["readmitted"].value_counts().to_dict()

        # 6. Age distribution
        age_dist = df["age"].value_counts().to_dict()

        # 7. Numerical ranges
        num_summary = {
            "time_in_hospital": {
                "min": int(df["time_in_hospital"].min()),
                "max": int(df["time_in_hospital"].max()),
                "mean": round(float(df["time_in_hospital"].mean()), 2),
                "median": float(df["time_in_hospital"].median()),
            },
            "num_lab_procedures": {
                "min": int(df["num_lab_procedures"].min()),
                "max": int(df["num_lab_procedures"].max()),
                "mean": round(float(df["num_lab_procedures"].mean()), 2),
            },
            "num_medications": {
                "min": int(df["num_medications"].min()),
                "max": int(df["num_medications"].max()),
                "mean": round(float(df["num_medications"].mean()), 2),
            },
            "number_diagnoses": {
                "min": int(df["number_diagnoses"].min()),
                "max": int(df["number_diagnoses"].max()),
                "mean": round(float(df["number_diagnoses"].mean()), 2),
            },
        }

        return {
            "total_records": total_records,
            "unique_encounters": int(df["encounter_id"].nunique()),
            "duplicate_encounters": dup_encounters,
            "unique_patients": unique_patients,
            "encounters_per_patient": encounters_per_patient,
            "missing_fields": missing_counts,
            "gender_distribution": gender_dist,
            "invalid_gender_records": invalid_gender_count,
            "readmission_distribution": readmission_dist,
            "age_distribution": age_dist,
            "numerical_summary": num_summary,
        }
