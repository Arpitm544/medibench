-- Query 09: 30-day readmission rate by medication change status
SELECT 
    CASE WHEN change = 'Ch' THEN 'Medication Changed' ELSE 'No Medication Change' END AS medication_change_status,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM patient_encounters
GROUP BY CASE WHEN change = 'Ch' THEN 'Medication Changed' ELSE 'No Medication Change' END
ORDER BY total_encounters DESC;
