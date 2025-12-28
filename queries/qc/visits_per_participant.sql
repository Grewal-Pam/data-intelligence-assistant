

-- ==============================
-- Visits per participant
-- ==============================
SELECT
    participant_id,
    COUNT(*) AS visit_count
FROM visits
GROUP BY participant_id;

