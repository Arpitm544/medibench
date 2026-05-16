-- Query 20: Complex cohort comparison: Insulin treatment vs oral-only/no medication
WITH cohort_classification AS (
    SELECT 
        encounter_id,
        readmitted,
        time_in_hospital,
        num_medications,
        CASE 
            WHEN insulin != 'No' THEN 'Insulin-Treated'
            WHEN diabetes_med = 'Yes' AND insulin = 'No' THEN 'Oral Agents Only'
            ELSE 'No Diabetes Medications'
        END AS treatment_modality
    FROM patient_encounters
)
SELECT 
    treatment_modality,
    COUNT(*) AS total_encounters,
    ROUND(AVG(time_in_hospital), 2) AS avg_stay_days,
    ROUND(AVG(num_medications), 1) AS avg_meds_count,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_30d_pct
FROM cohort_classification
GROUP BY treatment_modality
ORDER BY total_encounters DESC;
