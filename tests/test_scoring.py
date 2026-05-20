from medibench.database import SessionLocal
from medibench.evaluation.model_client import ModelClient
from medibench.evaluation.runner import EvaluationRunner
from medibench.evaluation.scoring import ScoringEngine


def test_scoring_numeric():
    # Exact match
    score, status, err = ScoringEngine.score_numeric("The rate is 11.16%", 11.16, tolerance=0.01)
    assert score == 1.0
    assert status == "passed"
    assert err is None

    # Within tolerance
    score, status, err = ScoringEngine.score_numeric("Answer: 11.2", 11.16, tolerance=0.05)
    assert score == 1.0
    assert status == "passed"

    # Outside tolerance
    score, status, err = ScoringEngine.score_numeric("Answer: 15.0", 11.16, tolerance=0.05)
    assert score == 0.0
    assert status == "failed"
    assert "NUMERICAL_DEVIATION" in err

    # Parse error
    score, status, err = ScoringEngine.score_numeric("There is no number here", 11.16)
    assert score == 0.0
    assert "PARSE_ERROR" in err


def test_scoring_categorical():
    score, status, err = ScoringEngine.score_categorical("The cohort is Caucasian", "Caucasian")
    assert score == 1.0
    assert status == "passed"

    score, status, err = ScoringEngine.score_categorical("The cohort is Asian", "Caucasian")
    assert score == 0.0
    assert status == "failed"


def test_scoring_rubric():
    meta = {"required_concepts": ["confounding", "indication", "severity"]}
    response = "This pattern represents confounding by indication because baseline patient severity is higher."
    score, status, err = ScoringEngine.score_rubric(response, "reference", meta)
    assert score == 1.0
    assert status == "passed"

    fail_response = "The hospital has poor doctors."
    score, status, err = ScoringEngine.score_rubric(fail_response, "reference", meta)
    assert score == 0.0
    assert status == "failed"


def test_evaluation_runner_mock():
    db = SessionLocal()
    try:
        client = ModelClient(model_name="Test-Bench-Model", mock_mode=True, mock_accuracy=1.0)
        runner = EvaluationRunner(db=db, client=client)
        # Evaluate subset: category "statistical_reasoning"
        res = runner.run_evaluation(model_name="Test-Bench-Model", category="statistical_reasoning")
        assert res["total_questions"] == 10
        assert res["overall_score_pct"] == 100.0
        assert res["status"] == "completed"
    finally:
        db.close()
