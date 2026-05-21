from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from medibench.analytics.demographics import DemographicsAnalytics
from medibench.analytics.readmission import ReadmissionAnalytics
from medibench.analytics.treatment import TreatmentAnalytics
from medibench.database import get_db

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    readm = ReadmissionAnalytics(db)
    demo = DemographicsAnalytics(db)
    treat = TreatmentAnalytics(db)

    metrics = readm.get_overall_metrics()
    gender = demo.get_gender_distribution()
    labs = treat.get_procedure_and_lab_stats()

    return {
        "status": "success",
        "encounter_summary": metrics,
        "gender_distribution": gender["data"],
        "clinical_procedure_stats": labs,
    }


@router.get("/readmissions")
def get_readmission_analysis(db: Session = Depends(get_db)):
    readm = ReadmissionAnalytics(db)

    return {
        "status": "success",
        "overall": readm.get_overall_metrics(),
        "by_stay_duration": readm.get_readmission_by_stay()["data"],
        "by_medication_change": readm.get_readmission_by_medication_change()["data"],
        "by_diagnosis_category": readm.get_readmission_by_diagnosis_category()["data"],
    }


@router.get("/demographics")
def get_demographics_analysis(db: Session = Depends(get_db)):
    demo = DemographicsAnalytics(db)

    return {
        "status": "success",
        "age_distribution": demo.get_age_distribution()["data"],
        "gender_distribution": demo.get_gender_distribution()["data"],
        "race_distribution": demo.get_race_distribution()["data"],
    }
