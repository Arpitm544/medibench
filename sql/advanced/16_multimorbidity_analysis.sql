-- Query 16: Multi-morbidity analysis: number of diagnoses vs medication count and readmission
SELECT 
    CASE 
        WHEN number_diagnoses BETWEEN 1 AND 4 THEN '1-4 Diagnoses'
        WHEN number_diagnoses BETWEEN 5 AND 8 THEN '5-8 Diagnoses'
        ELSE '9+ Diagnoses'
    END AS diagnosis_burden_group,
    COUNT(*) AS total_encounters,
    ROUND(AVG(num_medications), 1) AS avg_medications,
    ROUND(AVG(time_in_hospital), 2) AS avg_length_of_stay,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
    ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_30d_pct
FROM patient_encounters
GROUP BY CASE 
        WHEN number_diagnoses BETWEEN 1 AND 4 THEN '1-4 Diagnoses'
        WHEN number_diagnoses BETWEEN 5 AND 8 THEN '5-8 Diagnoses'
        ELSE '9+ Diagnoses'
    END
ORDER BY total_encounters DESC;
