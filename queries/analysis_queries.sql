-- ==============================
-- BMI change between visits
-- ==============================
SELECT
    p.participant_id,
    MAX(CASE WHEN v.visit_type = 'baseline' THEN vm.bmi END) AS bmi_baseline,
    MAX(CASE WHEN v.visit_type = 'followup' THEN vm.bmi END) AS bmi_followup,
    MAX(CASE WHEN v.visit_type = 'followup' THEN vm.bmi END) -
    MAX(CASE WHEN v.visit_type = 'baseline' THEN vm.bmi END) AS bmi_change
FROM participants p
JOIN visits v ON p.participant_id = v.participant_id
JOIN vital_measurements vm ON v.visit_id = vm.visit_id
GROUP BY p.participant_id;

-- ==============================
-- Blood pressure by smoking status
-- ==============================
SELECT
    sm.smoking,
    AVG(vm.systolic_bp) AS avg_systolic,
    AVG(vm.diastolic_bp) AS avg_diastolic
FROM survey_measurements sm
JOIN vital_measurements vm ON sm.visit_id = vm.visit_id
GROUP BY sm.smoking;

-- ==============================
-- Education vs sleep duration
-- ==============================
SELECT
    sm.education,
    AVG(sm.sleep_hours) AS avg_sleep
FROM survey_measurements sm
GROUP BY sm.education;
