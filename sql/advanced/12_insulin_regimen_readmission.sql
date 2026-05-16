-- Query 12: Insulin dosage regimen breakdown and 30-day readmission
SELECT 
    insulin AS insulin_regimen,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct,
    ROUND(AVG(time_in_hospital), 2) AS avg_stay_days
FROM patient_encounters
GROUP BY insulin
ORDER BY total_encounters DESC;
