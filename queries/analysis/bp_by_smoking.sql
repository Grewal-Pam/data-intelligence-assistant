SELECT
    sm.smoking,
    AVG(vm.systolic_bp) AS avg_systolic,
    AVG(vm.diastolic_bp) AS avg_diastolic
FROM survey_measurements sm
JOIN vital_measurements vm
  ON sm.visit_id = vm.visit_id
WHERE sm.smoking = :smoking_status
GROUP BY sm.smoking;
