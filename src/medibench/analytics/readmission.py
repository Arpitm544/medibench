from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class ReadmissionAnalytics:
    def __init__(self, db: Session):
        self.db = db

    def get_overall_metrics(self) -> dict[str, Any]:
        sql = """
        SELECT
            COUNT(*) AS total_encounters,
            COUNT(DISTINCT patient_nbr) AS unique_patients,
            SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
            ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_30d_rate_pct,
            SUM(CASE WHEN readmitted IN ('<30', '>30') THEN 1 ELSE 0 END) AS readmitted_any,
            ROUND(CAST(SUM(CASE WHEN readmitted IN ('<30', '>30') THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_any_rate_pct,
            ROUND(AVG(time_in_hospital), 2) AS avg_time_in_hospital
        FROM patient_encounters;
        """
        row = dict(self.db.execute(text(sql)).mappings().first())
        return row

    def get_readmission_by_stay(self) -> dict[str, Any]:
        sql = """
        SELECT
            time_in_hospital,
            COUNT(*) AS encounters,
            SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
            ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
        FROM patient_encounters
        GROUP BY time_in_hospital
        ORDER BY time_in_hospital ASC;
        """
        result = self.db.execute(text(sql)).mappings().all()
        return {"data": [dict(r) for r in result]}

    def get_readmission_by_medication_change(self) -> dict[str, Any]:
        sql = """
        SELECT
            change,
            COUNT(*) AS total_encounters,
            SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
            ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
        FROM patient_encounters
        GROUP BY change;
        """
        result = self.db.execute(text(sql)).mappings().all()
        return {"data": [dict(r) for r in result]}

    def get_readmission_by_diagnosis_category(self) -> dict[str, Any]:
        sql = """
        WITH categorized_encounters AS (
            SELECT
                encounter_id,
                readmitted,
                CASE
                    WHEN diag_1 LIKE '250%' THEN 'Diabetes'
                    WHEN (CAST(SUBSTR(diag_1, 1, 3) AS INTEGER) BETWEEN 390 AND 459) OR diag_1 = '785' THEN 'Circulatory'
                    WHEN (CAST(SUBSTR(diag_1, 1, 3) AS INTEGER) BETWEEN 460 AND 519) OR diag_1 = '786' THEN 'Respiratory'
                    WHEN (CAST(SUBSTR(diag_1, 1, 3) AS INTEGER) BETWEEN 520 AND 579) OR diag_1 = '787' THEN 'Digestive'
                    WHEN (CAST(SUBSTR(diag_1, 1, 3) AS INTEGER) BETWEEN 580 AND 629) OR diag_1 = '788' THEN 'Genitourinary'
                    WHEN (CAST(SUBSTR(diag_1, 1, 3) AS INTEGER) BETWEEN 140 AND 239) THEN 'Neoplasms'
                    WHEN (CAST(SUBSTR(diag_1, 1, 3) AS INTEGER) BETWEEN 710 AND 739) THEN 'Musculoskeletal'
                    WHEN (CAST(SUBSTR(diag_1, 1, 3) AS INTEGER) BETWEEN 800 AND 999) THEN 'Injury'
                    ELSE 'Other'
                END AS primary_diagnosis_category
            FROM patient_encounters
            WHERE diag_1 IS NOT NULL AND diag_1 NOT LIKE 'V%' AND diag_1 NOT LIKE 'E%'
        )
        SELECT
            primary_diagnosis_category,
            COUNT(*) AS total_encounters,
            SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
            ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
        FROM categorized_encounters
        GROUP BY primary_diagnosis_category
        ORDER BY total_encounters DESC;
        """
        result = self.db.execute(text(sql)).mappings().all()
        return {"data": [dict(r) for r in result]}
