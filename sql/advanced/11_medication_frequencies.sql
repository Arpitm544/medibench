-- Query 11: Utilization frequencies of primary diabetes medications
SELECT 
    'insulin' AS medication,
    SUM(CASE WHEN insulin != 'No' THEN 1 ELSE 0 END) AS active_prescriptions,
    ROUND(CAST(SUM(CASE WHEN insulin != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS prescription_pct
FROM patient_encounters
UNION ALL
SELECT 
    'metformin' AS medication,
    SUM(CASE WHEN metformin != 'No' THEN 1 ELSE 0 END) AS active_prescriptions,
    ROUND(CAST(SUM(CASE WHEN metformin != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS prescription_pct
FROM patient_encounters
UNION ALL
SELECT 
    'glipizide' AS medication,
    SUM(CASE WHEN glipizide != 'No' THEN 1 ELSE 0 END) AS active_prescriptions,
    ROUND(CAST(SUM(CASE WHEN glipizide != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS prescription_pct
FROM patient_encounters
UNION ALL
SELECT 
    'glyburide' AS medication,
    SUM(CASE WHEN glyburide != 'No' THEN 1 ELSE 0 END) AS active_prescriptions,
    ROUND(CAST(SUM(CASE WHEN glyburide != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS prescription_pct
FROM patient_encounters
UNION ALL
SELECT 
    'pioglitazone' AS medication,
    SUM(CASE WHEN pioglitazone != 'No' THEN 1 ELSE 0 END) AS active_prescriptions,
    ROUND(CAST(SUM(CASE WHEN pioglitazone != 'No' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS prescription_pct
FROM patient_encounters
ORDER BY active_prescriptions DESC;
