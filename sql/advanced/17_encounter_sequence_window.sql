-- Query 17: Window function: Encounter sequence per patient and readmission risk
WITH sequenced_encounters AS (
    SELECT 
        encounter_id,
        patient_nbr,
        readmitted,
        ROW_NUMBER() OVER (PARTITION BY patient_nbr ORDER BY encounter_id ASC) AS encounter_seq
    FROM patient_encounters
)
SELECT 
    CASE WHEN encounter_seq = 1 THEN 'Index (First) Encounter' ELSE 'Subsequent Encounter' END AS encounter_stage,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM sequenced_encounters
GROUP BY CASE WHEN encounter_seq = 1 THEN 'Index (First) Encounter' ELSE 'Subsequent Encounter' END;
