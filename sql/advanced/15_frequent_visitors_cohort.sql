-- Query 15: Frequent hospital visitors: Patients with >= 3 encounters
WITH patient_encounter_counts AS (
    SELECT 
        patient_nbr,
        COUNT(*) AS total_visits,
        SUM(time_in_hospital) AS total_days_hospitalized,
        SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS total_30d_readmissions
    FROM patient_encounters
    GROUP BY patient_nbr
)
SELECT 
    CASE WHEN total_visits >= 3 THEN 'High-Frequency (>=3 visits)' ELSE 'Standard (<3 visits)' END AS patient_cohort,
    COUNT(*) AS unique_patients,
    SUM(total_visits) AS total_encounters,
    ROUND(AVG(total_days_hospitalized), 2) AS avg_hospital_days_per_patient,
    ROUND(CAST(SUM(total_30d_readmissions) AS FLOAT) * 100.0 / SUM(total_visits), 2) AS readmission_30d_pct
FROM patient_encounter_counts
GROUP BY CASE WHEN total_visits >= 3 THEN 'High-Frequency (>=3 visits)' ELSE 'Standard (<3 visits)' END;
