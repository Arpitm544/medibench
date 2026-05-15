from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class TreatmentAnalytics:
    def __init__(self, db: Session):
        self.db = db

    def get_medication_patterns(self) -> dict[str, Any]:
        sql = """
        SELECT
            'insulin' AS drug, SUM(CASE WHEN insulin != 'No' THEN 1 ELSE 0 END) AS count,
            ROUND(CAST(SUM(CASE WHEN insulin != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS pct
        FROM patient_encounters
        UNION ALL
        SELECT
            'metformin' AS drug, SUM(CASE WHEN metformin != 'No' THEN 1 ELSE 0 END) AS count,
            ROUND(CAST(SUM(CASE WHEN metformin != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS pct
        FROM patient_encounters
        UNION ALL
        SELECT
            'glipizide' AS drug, SUM(CASE WHEN glipizide != 'No' THEN 1 ELSE 0 END) AS count,
            ROUND(CAST(SUM(CASE WHEN glipizide != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS pct
        FROM patient_encounters
        UNION ALL
        SELECT
            'glyburide' AS drug, SUM(CASE WHEN glyburide != 'No' THEN 1 ELSE 0 END) AS count,
            ROUND(CAST(SUM(CASE WHEN glyburide != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS pct
        FROM patient_encounters
        UNION ALL
        SELECT
            'pioglitazone' AS drug, SUM(CASE WHEN pioglitazone != 'No' THEN 1 ELSE 0 END) AS count,
            ROUND(CAST(SUM(CASE WHEN pioglitazone != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS pct
        FROM patient_encounters
        ORDER BY count DESC;
        """
        result = self.db.execute(text(sql)).mappings().all()
        return {"data": [dict(r) for r in result]}

    def get_insulin_regimens(self) -> dict[str, Any]:
        sql = """
        SELECT
            insulin,
            COUNT(*) AS encounter_count,
            SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
            ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
        FROM patient_encounters
        GROUP BY insulin
        ORDER BY encounter_count DESC;
        """
        result = self.db.execute(text(sql)).mappings().all()
        return {"data": [dict(r) for r in result]}

    def get_procedure_and_lab_stats(self) -> dict[str, Any]:
        sql = """
        SELECT
            ROUND(AVG(num_lab_procedures), 2) AS avg_lab_procedures,
            MIN(num_lab_procedures) AS min_lab_procedures,
            MAX(num_lab_procedures) AS max_lab_procedures,
            ROUND(AVG(num_procedures), 2) AS avg_procedures,
            MIN(num_procedures) AS min_procedures,
            MAX(num_procedures) AS max_procedures,
            ROUND(AVG(num_medications), 2) AS avg_medications
        FROM patient_encounters;
        """
        return dict(self.db.execute(text(sql)).mappings().first())
