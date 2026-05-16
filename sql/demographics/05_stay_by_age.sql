-- Query 05: Average and maximum length of stay by age group
SELECT 
    age,
    COUNT(*) AS encounters,
    ROUND(AVG(time_in_hospital), 2) AS avg_time_in_hospital,
    MIN(time_in_hospital) AS min_stay,
    MAX(time_in_hospital) AS max_stay,
    ROUND(AVG(num_lab_procedures), 1) AS avg_lab_procedures
FROM patient_encounters
GROUP BY age
ORDER BY age ASC;
