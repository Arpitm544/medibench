-- Query 18: Glycated hemoglobin (HbA1c) testing results and readmission
SELECT 
    COALESCE(a1c_result, 'None Tested') AS a1c_test_result,
    COUNT(*) AS total_encounters,
    ROUND(CAST(COUNT(*) AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM patient_encounters), 2) AS testing_pct,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM patient_encounters
GROUP BY COALESCE(a1c_result, 'None Tested')
ORDER BY total_encounters DESC;
