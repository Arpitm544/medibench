-- Query 14: Prior healthcare utilization tiers (Inpatient visits) vs Readmission
SELECT 
    CASE 
        WHEN number_inpatient = 0 THEN '0 Prior Inpatient'
        WHEN number_inpatient = 1 THEN '1 Prior Inpatient'
        WHEN number_inpatient BETWEEN 2 AND 4 THEN '2-4 Prior Inpatient'
        ELSE '5+ Prior Inpatient'
    END AS prior_inpatient_tier,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM patient_encounters
GROUP BY CASE 
        WHEN number_inpatient = 0 THEN '0 Prior Inpatient'
        WHEN number_inpatient = 1 THEN '1 Prior Inpatient'
        WHEN number_inpatient BETWEEN 2 AND 4 THEN '2-4 Prior Inpatient'
        ELSE '5+ Prior Inpatient'
    END
ORDER BY total_encounters DESC;
