-- MediBench PostgreSQL Database Schema
-- Version 1.0

CREATE TABLE IF NOT EXISTS patient_encounters (
    encounter_id INTEGER PRIMARY KEY,
    patient_nbr INTEGER NOT NULL,
    race VARCHAR(50),
    gender VARCHAR(20),
    age VARCHAR(20),
    weight VARCHAR(50),
    admission_type_id INTEGER,
    discharge_disposition_id INTEGER,
    admission_source_id INTEGER,
    time_in_hospital INTEGER NOT NULL,
    payer_code VARCHAR(20),
    medical_specialty VARCHAR(100),
    num_lab_procedures INTEGER NOT NULL,
    num_procedures INTEGER NOT NULL,
    num_medications INTEGER NOT NULL,
    number_outpatient INTEGER NOT NULL,
    number_emergency INTEGER NOT NULL,
    number_inpatient INTEGER NOT NULL,
    diag_1 VARCHAR(50),
    diag_2 VARCHAR(50),
    diag_3 VARCHAR(50),
    number_diagnoses INTEGER NOT NULL,
    max_glu_serum VARCHAR(20),
    a1c_result VARCHAR(20),
    metformin VARCHAR(20),
    repaglinide VARCHAR(20),
    nateglinide VARCHAR(20),
    chlorpropamide VARCHAR(20),
    glimepiride VARCHAR(20),
    acetohexamide VARCHAR(20),
    glipizide VARCHAR(20),
    glyburide VARCHAR(20),
    tolbutamide VARCHAR(20),
    pioglitazone VARCHAR(20),
    rosiglitazone VARCHAR(20),
    acarbose VARCHAR(20),
    miglitol VARCHAR(20),
    troglitazone VARCHAR(20),
    tolazamide VARCHAR(20),
    examide VARCHAR(20),
    citoglipton VARCHAR(20),
    insulin VARCHAR(20),
    glyburide_metformin VARCHAR(20),
    glipizide_metformin VARCHAR(20),
    glimepiride_pioglitazone VARCHAR(20),
    metformin_rosiglitazone VARCHAR(20),
    metformin_pioglitazone VARCHAR(20),
    change VARCHAR(10),
    diabetes_med VARCHAR(10),
    readmitted VARCHAR(20) NOT NULL,
    readmitted_30d BOOLEAN NOT NULL DEFAULT FALSE,
    readmitted_any BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS ix_encounter_patient ON patient_encounters (patient_nbr);
CREATE INDEX IF NOT EXISTS ix_encounter_readmitted ON patient_encounters (readmitted);
CREATE INDEX IF NOT EXISTS ix_encounter_readmitted_30d ON patient_encounters (readmitted_30d);
CREATE INDEX IF NOT EXISTS ix_encounter_age ON patient_encounters (age);
CREATE INDEX IF NOT EXISTS ix_encounter_gender ON patient_encounters (gender);

CREATE TABLE IF NOT EXISTS data_quality_results (
    id SERIAL PRIMARY KEY,
    check_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    record_count INTEGER NOT NULL,
    affected_count INTEGER NOT NULL,
    percentage FLOAT NOT NULL,
    details JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS benchmark_questions (
    id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    question TEXT NOT NULL,
    dataset_version VARCHAR(20) DEFAULT 'v1',
    reference_solution TEXT,
    evaluation_method VARCHAR(50) NOT NULL,
    tolerance FLOAT,
    freshness_category VARCHAR(50) DEFAULT 'static',
    status VARCHAR(50) DEFAULT 'pending_verification',
    metadata_info JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS benchmark_answers (
    id SERIAL PRIMARY KEY,
    question_id VARCHAR(50) REFERENCES benchmark_questions(id) ON DELETE CASCADE,
    expected_answer TEXT NOT NULL,
    answer_type VARCHAR(20) NOT NULL,
    computed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    verification_hash VARCHAR(64),
    verification_notes TEXT
);

CREATE INDEX IF NOT EXISTS ix_benchmark_answers_question_id ON benchmark_answers (question_id);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    id VARCHAR(50) PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    started_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    status VARCHAR(20) DEFAULT 'running',
    total_questions INTEGER DEFAULT 0,
    passed_questions INTEGER DEFAULT 0,
    overall_score FLOAT DEFAULT 0.0,
    config JSONB
);

CREATE TABLE IF NOT EXISTS evaluation_results (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(50) REFERENCES evaluation_runs(id) ON DELETE CASCADE,
    benchmark_id VARCHAR(50) REFERENCES benchmark_questions(id) ON DELETE CASCADE,
    model VARCHAR(100) NOT NULL,
    expected_answer TEXT,
    predicted_answer TEXT,
    score FLOAT NOT NULL,
    latency_ms FLOAT,
    tokens_used INTEGER,
    status VARCHAR(20) NOT NULL,
    evaluation_details JSONB,
    error_message TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_evaluation_results_run_id ON evaluation_results (run_id);
CREATE INDEX IF NOT EXISTS ix_evaluation_results_benchmark_id ON evaluation_results (benchmark_id);
