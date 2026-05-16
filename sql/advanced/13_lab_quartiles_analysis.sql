-- Query 13: Lab procedure quartiles and relationship with length of stay
WITH ranked_labs AS (
    SELECT 
        encounter_id,
        num_lab_procedures,
        time_in_hospital,
        readmitted_30d,
        NTILE(4) OVER (ORDER BY num_lab_procedures ASC) AS lab_quartile
    FROM patient_encounters
)
SELECT 
    lab_quartile,
    COUNT(*) AS encounters,
    MIN(num_lab_procedures) AS min_labs,
    MAX(num_lab_procedures) AS max_labs,
    ROUND(AVG(num_lab_procedures), 1) AS avg_labs,
    ROUND(AVG(time_in_hospital), 2) AS avg_stay_days,
    ROUND(CAST(SUM(CASE WHEN readmitted_30d = 1 THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_30d_pct
FROM ranked_labs
GROUP BY lab_quartile
ORDER BY lab_quartile ASC;
