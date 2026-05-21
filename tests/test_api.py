from fastapi.testclient import TestClient

from medibench.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_analytics_overview_endpoint():
    response = client.get("/api/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["encounter_summary"]["total_encounters"] == 101766


def test_analytics_readmissions_endpoint():
    response = client.get("/api/analytics/readmissions")
    assert response.status_code == 200
    data = response.json()
    assert "by_stay_duration" in data
    assert "by_medication_change" in data


def test_benchmarks_list_endpoint():
    response = client.get("/api/benchmarks")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 60


def test_benchmark_detail_endpoint():
    response = client.get("/api/benchmarks/MED-001")
    assert response.status_code == 200
    data = response.json()
    assert data["benchmark"]["id"] == "MED-001"
    assert data["benchmark"]["verified_answer"]["expected_answer"] is not None


def test_benchmark_retired_endpoint():
    response = client.get("/api/benchmarks/retired")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] >= 3


def test_reports_summary_endpoint():
    response = client.get("/api/reports/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["dataset"]["total_encounters"] == 101766
    assert data["benchmarks"]["total_questions"] == 60


def test_evaluations_list_endpoint():
    response = client.get("/api/evaluations")
    assert response.status_code == 200
    data = response.json()
    assert data["total_runs"] >= 2
