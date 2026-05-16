-- Query 10: Readmission rate by diabetes medication prescription status
SELECT 
    CASE WHEN diabetes_med = 'Yes' THEN 'Prescribed Diabetes Med' ELSE 'No Diabetes Med Prescribed' END AS diabetes_med_status,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM patient_encounters
GROUP BY CASE WHEN diabetes_med = 'Yes' THEN 'Prescribed Diabetes Med' ELSE 'No Diabetes Med Prescribed' END
ORDER BY total_encounters DESC;
