import pandas as pd

from medibench.config import settings
from medibench.ingestion.loader import clean_dataframe


def test_raw_data_file_exists():
    raw_csv = settings.RAW_DATA_DIR / "diabetic_data.csv"
    assert raw_csv.exists()


def test_clean_dataframe_transformation():
    sample_data = {
        "encounter_id": [1, 2],
        "patient_nbr": [100, 101],
        "race": ["Caucasian", "?"],
        "gender": ["Female", "Male"],
        "age": ["[0-10)", "[50-60)"],
        "weight": ["?", "?"],
        "admission_type_id": [1, 2],
        "discharge_disposition_id": [1, 1],
        "admission_source_id": [7, 7],
        "time_in_hospital": [3, 4],
        "payer_code": ["?", "MC"],
        "medical_specialty": ["?", "?"],
        "num_lab_procedures": [40, 50],
        "num_procedures": [0, 1],
        "num_medications": [5, 10],
        "number_outpatient": [0, 0],
        "number_emergency": [0, 0],
        "number_inpatient": [0, 1],
        "diag_1": ["250.0", "428"],
        "diag_2": ["?", "?"],
        "diag_3": ["?", "?"],
        "number_diagnoses": [5, 6],
        "max_glu_serum": ["None", "None"],
        "A1Cresult": ["None", ">8"],
        "metformin": ["No", "No"],
        "repaglinide": ["No", "No"],
        "nateglinide": ["No", "No"],
        "chlorpropamide": ["No", "No"],
        "glimepiride": ["No", "No"],
        "acetohexamide": ["No", "No"],
        "glipizide": ["No", "No"],
        "glyburide": ["No", "No"],
        "tolbutamide": ["No", "No"],
        "pioglitazone": ["No", "No"],
        "rosiglitazone": ["No", "No"],
        "acarbose": ["No", "No"],
        "miglitol": ["No", "No"],
        "troglitazone": ["No", "No"],
        "tolazamide": ["No", "No"],
        "examide": ["No", "No"],
        "citoglipton": ["No", "No"],
        "insulin": ["No", "Steady"],
        "glyburide-metformin": ["No", "No"],
        "glipizide-metformin": ["No", "No"],
        "glimepiride-pioglitazone": ["No", "No"],
        "metformin-rosiglitazone": ["No", "No"],
        "metformin-pioglitazone": ["No", "No"],
        "change": ["No", "Ch"],
        "diabetesMed": ["No", "Yes"],
        "readmitted": ["<30", "NO"],
    }
    df = pd.DataFrame(sample_data)
    clean_df = clean_dataframe(df)

    assert "a1c_result" in clean_df.columns
    assert "glyburide_metformin" in clean_df.columns
    assert "readmitted_30d" in clean_df.columns
    assert clean_df.loc[0, "readmitted_30d"]
    assert not clean_df.loc[1, "readmitted_30d"]
    assert clean_df.loc[0, "race"] == "Caucasian"
    assert pd.isna(clean_df.loc[1, "race"])  # '?' was cleaned to NA/None
