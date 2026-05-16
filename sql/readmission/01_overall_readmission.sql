-- Query 01: Overall 30-day readmission rate
-- Returns total encounters, readmitted <30 encounters, and readmission percentage
SELECT 
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d_encounters,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_30d_rate_pct
FROM patient_encounters;
