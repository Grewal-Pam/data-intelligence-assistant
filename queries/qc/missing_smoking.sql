

-- ==============================
-- Missing smoking values
-- ==============================
SELECT
    COUNT(*) AS total_rows,
    SUM(smoking IS NULL) AS missing_smoking
FROM survey_measurements;
