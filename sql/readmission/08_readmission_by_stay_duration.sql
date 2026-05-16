-- Query 08: Readmission by hospital stay duration and cumulative distribution
WITH stay_metrics AS (
    SELECT 
        time_in_hospital,
        COUNT(*) AS encounters,
        SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
        ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
    FROM patient_encounters
    GROUP BY time_in_hospital
)
SELECT 
    time_in_hospital,
    encounters,
    ROUND(CAST(encounters AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM patient_encounters), 2) AS pct_of_total,
    readmitted_30d,
    readmission_rate_pct,
    ROUND(CAST(SUM(encounters) OVER (ORDER BY time_in_hospital ASC) AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM patient_encounters), 2) AS cumulative_pct
FROM stay_metrics
ORDER BY time_in_hospital ASC;
