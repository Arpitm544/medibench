from collections.abc import Generator
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

from medibench.config import settings

# Engine configuration
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PatientEncounter(Base):
    __tablename__ = "patient_encounters"

    encounter_id = Column(Integer, primary_key=True, index=True)
    patient_nbr = Column(Integer, index=True, nullable=False)
    race = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)
    age = Column(String(20), nullable=True)
    weight = Column(String(50), nullable=True)
    admission_type_id = Column(Integer, nullable=True)
    discharge_disposition_id = Column(Integer, nullable=True)
    admission_source_id = Column(Integer, nullable=True)
    time_in_hospital = Column(Integer, nullable=False)
    payer_code = Column(String(20), nullable=True)
    medical_specialty = Column(String(100), nullable=True)
    num_lab_procedures = Column(Integer, nullable=False)
    num_procedures = Column(Integer, nullable=False)
    num_medications = Column(Integer, nullable=False)
    number_outpatient = Column(Integer, nullable=False)
    number_emergency = Column(Integer, nullable=False)
    number_inpatient = Column(Integer, nullable=False)
    diag_1 = Column(String(50), nullable=True)
    diag_2 = Column(String(50), nullable=True)
    diag_3 = Column(String(50), nullable=True)
    number_diagnoses = Column(Integer, nullable=False)
    max_glu_serum = Column(String(20), nullable=True)
    a1c_result = Column(String(20), nullable=True)

    # 23 Medications
    metformin = Column(String(20), nullable=True)
    repaglinide = Column(String(20), nullable=True)
    nateglinide = Column(String(20), nullable=True)
    chlorpropamide = Column(String(20), nullable=True)
    glimepiride = Column(String(20), nullable=True)
    acetohexamide = Column(String(20), nullable=True)
    glipizide = Column(String(20), nullable=True)
    glyburide = Column(String(20), nullable=True)
    tolbutamide = Column(String(20), nullable=True)
    pioglitazone = Column(String(20), nullable=True)
    rosiglitazone = Column(String(20), nullable=True)
    acarbose = Column(String(20), nullable=True)
    miglitol = Column(String(20), nullable=True)
    troglitazone = Column(String(20), nullable=True)
    tolazamide = Column(String(20), nullable=True)
    examide = Column(String(20), nullable=True)
    citoglipton = Column(String(20), nullable=True)
    insulin = Column(String(20), nullable=True)
    glyburide_metformin = Column(String(20), nullable=True)
    glipizide_metformin = Column(String(20), nullable=True)
    glimepiride_pioglitazone = Column(String(20), nullable=True)
    metformin_rosiglitazone = Column(String(20), nullable=True)
    metformin_pioglitazone = Column(String(20), nullable=True)

    change = Column(String(10), nullable=True)
    diabetes_med = Column(String(10), nullable=True)
    readmitted = Column(String(20), nullable=False)  # '<30', '>30', 'NO'
    readmitted_30d = Column(Boolean, nullable=False, default=False)
    readmitted_any = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        Index("ix_encounter_patient", "patient_nbr"),
        Index("ix_encounter_readmitted", "readmitted"),
        Index("ix_encounter_readmitted_30d", "readmitted_30d"),
        Index("ix_encounter_age", "age"),
        Index("ix_encounter_gender", "gender"),
    )


class DataQualityResult(Base):
    __tablename__ = "data_quality_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    check_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)  # 'PASSED', 'WARNING', 'FAILED'
    record_count = Column(Integer, nullable=False)
    affected_count = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class BenchmarkQuestion(Base):
    __tablename__ = "benchmark_questions"

    id = Column(String(50), primary_key=True)  # e.g. MED-001
    category = Column(String(50), nullable=False)  # sql_analytics, statistical_reasoning, etc.
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    question = Column(Text, nullable=False)
    dataset_version = Column(String(20), default="v1")
    reference_solution = Column(Text, nullable=True)  # path or inline solution
    evaluation_method = Column(String(50), nullable=False)  # numeric_tolerance, sql_execution, rubric
    tolerance = Column(Float, nullable=True)
    freshness_category = Column(String(50), default="static")
    status = Column(String(50), default="pending_verification")
    metadata_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship("BenchmarkAnswer", back_populates="question_rel", cascade="all, delete-orphan")


class BenchmarkAnswer(Base):
    __tablename__ = "benchmark_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(String(50), ForeignKey("benchmark_questions.id"), nullable=False, index=True)
    expected_answer = Column(Text, nullable=False)
    answer_type = Column(String(20), nullable=False)  # numeric, categorical, sql_result, rubric
    computed_at = Column(DateTime, default=datetime.utcnow)
    verification_hash = Column(String(64), nullable=True)
    verification_notes = Column(Text, nullable=True)

    question_rel = relationship("BenchmarkQuestion", back_populates="answers")


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String(50), primary_key=True)  # e.g. RUN-001
    model_name = Column(String(100), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="running")  # running, completed, failed
    total_questions = Column(Integer, default=0)
    passed_questions = Column(Integer, default=0)
    overall_score = Column(Float, default=0.0)
    config = Column(JSON, nullable=True)

    results = relationship("EvaluationResult", back_populates="run_rel", cascade="all, delete-orphan")


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), ForeignKey("evaluation_runs.id"), nullable=False, index=True)
    benchmark_id = Column(String(50), ForeignKey("benchmark_questions.id"), nullable=False, index=True)
    model = Column(String(100), nullable=False)
    expected_answer = Column(Text, nullable=True)
    predicted_answer = Column(Text, nullable=True)
    score = Column(Float, nullable=False)
    latency_ms = Column(Float, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    status = Column(String(20), nullable=False)  # passed, failed, error
    evaluation_details = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    run_rel = relationship("EvaluationRun", back_populates="results")


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
