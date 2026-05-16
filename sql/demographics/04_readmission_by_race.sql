-- Query 04: Readmission rate by race with total encounter proportion
WITH race_stats AS (
    SELECT 
        COALESCE(race, 'Missing/Unspecified') AS race_category,
        COUNT(*) AS encounters,
        SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted_30d,
        ROUND(CAST(SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
    FROM patient_encounters
    GROUP BY COALESCE(race, 'Missing/Unspecified')
)
SELECT 
    race_category,
    encounters,
    ROUND(CAST(encounters AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM patient_encounters), 2) AS pct_of_all_encounters,
    readmitted_30d,
    readmission_rate_pct
FROM race_stats
ORDER BY encounters DESC;
