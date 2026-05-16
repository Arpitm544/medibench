-- Query 02: Readmission rate by age group with encounter volume and ranking
WITH age_summary AS (
    SELECT 
        age,
        COUNT(*) AS total_encounters,
        SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
        ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
    FROM patient_encounters
    GROUP BY age
)
SELECT 
    age,
    total_encounters,
    readmitted_30d,
    readmission_rate_pct,
    DENSE_RANK() OVER (ORDER BY readmission_rate_pct DESC) AS risk_rank
FROM age_summary
ORDER BY risk_rank ASC;
