SELECT
    sm.education,
    AVG(sm.sleep_hours) AS avg_sleep
FROM survey_measurements sm
GROUP BY sm.education;
