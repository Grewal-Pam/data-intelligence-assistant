-- ==============================
-- Row counts
-- ==============================
SELECT 'participants' AS table_name, COUNT(*) AS row_count FROM participants
UNION ALL
SELECT 'visits', COUNT(*) FROM visits
UNION ALL
SELECT 'survey_measurements', COUNT(*) FROM survey_measurements
UNION ALL
SELECT 'vital_measurements', COUNT(*) FROM vital_measurements;

-- ==============================
-- Visits per participant
-- ==============================
SELECT
    participant_id,
    COUNT(*) AS visit_count
FROM visits
GROUP BY participant_id;

-- ==============================
-- Missing smoking values
-- ==============================
SELECT
    COUNT(*) AS total_rows,
    SUM(smoking IS NULL) AS missing_smoking
FROM survey_measurements;
