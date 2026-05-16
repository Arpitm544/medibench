-- Query 06: Readmission rate by admission type
SELECT 
    admission_type_id,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM patient_encounters
GROUP BY admission_type_id
ORDER BY total_encounters DESC;
