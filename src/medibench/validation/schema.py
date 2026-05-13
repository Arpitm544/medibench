
from pydantic import BaseModel, Field

# Mapping of raw CSV column names to standardized snake_case column names
COLUMN_MAPPING = {
    "encounter_id": "encounter_id",
    "patient_nbr": "patient_nbr",
    "race": "race",
    "gender": "gender",
    "age": "age",
    "weight": "weight",
    "admission_type_id": "admission_type_id",
    "discharge_disposition_id": "discharge_disposition_id",
    "admission_source_id": "admission_source_id",
    "time_in_hospital": "time_in_hospital",
    "payer_code": "payer_code",
    "medical_specialty": "medical_specialty",
    "num_lab_procedures": "num_lab_procedures",
    "num_procedures": "num_procedures",
    "num_medications": "num_medications",
    "number_outpatient": "number_outpatient",
    "number_emergency": "number_emergency",
    "number_inpatient": "number_inpatient",
    "diag_1": "diag_1",
    "diag_2": "diag_2",
    "diag_3": "diag_3",
    "number_diagnoses": "number_diagnoses",
    "max_glu_serum": "max_glu_serum",
    "A1Cresult": "a1c_result",
    "metformin": "metformin",
    "repaglinide": "repaglinide",
    "nateglinide": "nateglinide",
    "chlorpropamide": "chlorpropamide",
    "glimepiride": "glimepiride",
    "acetohexamide": "acetohexamide",
    "glipizide": "glipizide",
    "glyburide": "glyburide",
    "tolbutamide": "tolbutamide",
    "pioglitazone": "pioglitazone",
    "rosiglitazone": "rosiglitazone",
    "acarbose": "acarbose",
    "miglitol": "miglitol",
    "troglitazone": "troglitazone",
    "tolazamide": "tolazamide",
    "examide": "examide",
    "citoglipton": "citoglipton",
    "insulin": "insulin",
    "glyburide-metformin": "glyburide_metformin",
    "glipizide-metformin": "glipizide_metformin",
    "glimepiride-pioglitazone": "glimepiride_pioglitazone",
    "metformin-rosiglitazone": "metformin_rosiglitazone",
    "metformin-pioglitazone": "metformin_pioglitazone",
    "change": "change",
    "diabetesMed": "diabetes_med",
    "readmitted": "readmitted",
}

MEDICATION_COLUMNS = [
    "metformin",
    "repaglinide",
    "nateglinide",
    "chlorpropamide",
    "glimepiride",
    "acetohexamide",
    "glipizide",
    "glyburide",
    "tolbutamide",
    "pioglitazone",
    "rosiglitazone",
    "acarbose",
    "miglitol",
    "troglitazone",
    "tolazamide",
    "examide",
    "citoglipton",
    "insulin",
    "glyburide_metformin",
    "glipizide_metformin",
    "glimepiride_pioglitazone",
    "metformin_rosiglitazone",
    "metformin_pioglitazone",
]


class EncounterSchema(BaseModel):
    encounter_id: int
    patient_nbr: int
    race: str | None = None
    gender: str | None = None
    age: str | None = None
    time_in_hospital: int = Field(ge=1, le=14)
    num_lab_procedures: int = Field(ge=0)
    num_procedures: int = Field(ge=0)
    num_medications: int = Field(ge=0)
    number_diagnoses: int = Field(ge=1)
    readmitted: str
    readmitted_30d: bool
    readmitted_any: bool
