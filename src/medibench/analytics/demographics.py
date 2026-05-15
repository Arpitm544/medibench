from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class DemographicsAnalytics:
    def __init__(self, db: Session):
        self.db = db

    def get_age_distribution(self) -> dict[str, Any]:
        sql = """
        SELECT
            age,
            COUNT(*) AS encounter_count,
            ROUND(CAST(COUNT(*) AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM patient_encounters), 2) AS percentage,
            SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
            ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct,
            ROUND(AVG(time_in_hospital), 2) AS avg_stay_days
        FROM patient_encounters
        GROUP BY age
        ORDER BY age ASC;
        """
        result = self.db.execute(text(sql)).mappings().all()
        return {"data": [dict(r) for r in result]}

    def get_gender_distribution(self) -> dict[str, Any]:
        sql = """
        SELECT
            gender,
            COUNT(*) AS encounter_count,
            ROUND(CAST(COUNT(*) AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM patient_encounters), 2) AS percentage,
            SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
            ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
        FROM patient_encounters
        WHERE gender IN ('Female', 'Male')
        GROUP BY gender
        ORDER BY encounter_count DESC;
        """
        result = self.db.execute(text(sql)).mappings().all()
        return {"data": [dict(r) for r in result]}

    def get_race_distribution(self) -> dict[str, Any]:
        sql = """
        SELECT
            COALESCE(race, 'Missing/Unspecified') AS race,
            COUNT(*) AS encounter_count,
            ROUND(CAST(COUNT(*) AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM patient_encounters), 2) AS percentage,
            SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
            ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
        FROM patient_encounters
        GROUP BY COALESCE(race, 'Missing/Unspecified')
        ORDER BY encounter_count DESC;
        """
        result = self.db.execute(text(sql)).mappings().all()
        return {"data": [dict(r) for r in result]}
