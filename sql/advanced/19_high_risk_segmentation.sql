-- Query 19: High-risk operational cohort segmentation
WITH risk_segmented AS (
    SELECT 
        encounter_id,
        readmitted,
        time_in_hospital,
        num_medications,
        number_inpatient,
        CASE 
            WHEN time_in_hospital >= 5 AND number_diagnoses >= 7 AND (number_emergency > 0 OR number_inpatient > 0) THEN 'High Risk'
            WHEN time_in_hospital >= 3 OR number_diagnoses >= 5 THEN 'Moderate Risk'
            ELSE 'Low Risk'
        END AS clinical_risk_tier
    FROM patient_encounters
)
SELECT 
    clinical_risk_tier,
    COUNT(*) AS encounter_count,
    ROUND(CAST(COUNT(*) AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM patient_encounters), 2) AS tier_share_pct,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM risk_segmented
GROUP BY clinical_risk_tier
ORDER BY readmission_rate_pct DESC;
