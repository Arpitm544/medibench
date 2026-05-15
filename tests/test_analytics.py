import pytest

from medibench.analytics.demographics import DemographicsAnalytics
from medibench.analytics.readmission import ReadmissionAnalytics
from medibench.analytics.statistics import StatisticalAnalytics
from medibench.analytics.treatment import TreatmentAnalytics
from medibench.database import SessionLocal


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()


def test_demographics_analytics(db_session):
    demo = DemographicsAnalytics(db_session)
    age_dist = demo.get_age_distribution()
    assert len(age_dist["data"]) == 10
    total_pct = sum(r["percentage"] for r in age_dist["data"])
    assert 99.0 <= total_pct <= 101.0

    gender_dist = demo.get_gender_distribution()
    assert len(gender_dist["data"]) == 2  # Female, Male


def test_readmission_analytics(db_session):
    readm = ReadmissionAnalytics(db_session)
    metrics = readm.get_overall_metrics()
    assert metrics["total_encounters"] == 101766
    assert metrics["unique_patients"] == 71518
    assert metrics["readmitted_30d"] == 11357
    assert round(metrics["readmission_30d_rate_pct"], 1) == 11.2


def test_treatment_analytics(db_session):
    treat = TreatmentAnalytics(db_session)
    patterns = treat.get_medication_patterns()
    assert len(patterns["data"]) == 5
    insulin_stat = next(d for d in patterns["data"] if d["drug"] == "insulin")
    assert insulin_stat["count"] > 50000

    lab_stats = treat.get_procedure_and_lab_stats()
    assert lab_stats["min_lab_procedures"] == 1
    assert lab_stats["max_lab_procedures"] == 132


def test_statistical_analytics(db_session):
    stat = StatisticalAnalytics(db_session)

    # 1. Confidence interval
    ci = stat.calculate_confidence_interval(11357, 101766)
    assert 11.0 <= ci["point_estimate"] <= 11.5
    assert ci["lower_bound"] < ci["point_estimate"] < ci["upper_bound"]

    # 2. Chi-square
    chi2 = stat.chi_square_test("change", "readmitted_30d")
    assert chi2["statistically_significant"] is True
    assert chi2["p_value"] < 0.001

    # 3. Stay comparison
    comp = stat.group_comparison_stay()
    assert comp["readmitted_mean_stay"] > comp["non_readmitted_mean_stay"]
    assert comp["difference_significant"] is True

    # 4. Correlation
    corr = stat.correlation_matrix()
    assert "time_in_hospital" in corr["pearson"]
