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

