import pytest

from medibench.benchmarks.ground_truth import RETIRED_QUESTIONS_REGISTRY
from medibench.database import BenchmarkQuestion, SessionLocal


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()


def test_total_benchmark_questions_count(db_session):
    total = db_session.query(BenchmarkQuestion).count()
    assert total == 60


def test_benchmark_categories_distribution(db_session):
    questions = db_session.query(BenchmarkQuestion).all()
    cat_counts = {}
    for q in questions:
        cat_counts[q.category] = cat_counts.get(q.category, 0) + 1

    assert cat_counts["sql_analytics"] == 15
    assert cat_counts["statistical_reasoning"] == 10
    assert cat_counts["data_interpretation"] == 10
    assert cat_counts["data_quality"] == 10
    assert cat_counts["business_decision_making"] == 10
    assert cat_counts["contradictory_evidence"] == 5


def test_all_questions_have_verified_answers(db_session):
    questions = db_session.query(BenchmarkQuestion).all()
    for q in questions:
        assert len(q.answers) == 1
        ans = q.answers[0]
        assert ans.expected_answer is not None
        assert ans.verification_hash is not None
        assert len(ans.verification_hash) == 64


def test_retired_question_registry():
    assert len(RETIRED_QUESTIONS_REGISTRY) >= 3
    ret_ids = {r.question_id for r in RETIRED_QUESTIONS_REGISTRY}
    assert "MED-RET-001" in ret_ids
    assert "MED-RET-002" in ret_ids
    assert "MED-RET-003" in ret_ids
