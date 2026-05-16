-- Query 03: Readmission rate by gender (excluding invalid records)
SELECT 
    gender,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM patient_encounters
WHERE gender IN ('Female', 'Male')
GROUP BY gender
ORDER BY total_encounters DESC;
