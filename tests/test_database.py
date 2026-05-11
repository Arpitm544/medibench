from sqlalchemy import text

from medibench.database import Base, engine


def test_database_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1


def test_tables_created():
    tables = Base.metadata.tables.keys()
    assert "patient_encounters" in tables
    assert "data_quality_results" in tables
    assert "benchmark_questions" in tables
    assert "benchmark_answers" in tables
    assert "evaluation_runs" in tables
    assert "evaluation_results" in tables
