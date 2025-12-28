-- ==============================
-- Participants
-- ==============================
CREATE TABLE IF NOT EXISTS participants (
    participant_id TEXT PRIMARY KEY,
    sex TEXT,
    date_of_birth DATE
);

-- ==============================
-- Visits
-- ==============================
CREATE TABLE IF NOT EXISTS visits (
    visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id TEXT NOT NULL,
    visit_date DATE NOT NULL,
    visit_type TEXT CHECK (visit_type IN ('baseline', 'followup')),
    FOREIGN KEY (participant_id)
        REFERENCES participants (participant_id)
);

-- ==============================
-- Survey Measurements
-- ==============================
CREATE TABLE IF NOT EXISTS survey_measurements (
    survey_id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id INTEGER NOT NULL,
    smoking INTEGER,
    alcohol INTEGER,
    education INTEGER,
    sleep_hours REAL,
    FOREIGN KEY (visit_id)
        REFERENCES visits (visit_id)
);

-- ==============================
-- Vital Measurements
-- ==============================
CREATE TABLE IF NOT EXISTS vital_measurements (
    vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id INTEGER NOT NULL,
    systolic_bp REAL,
    diastolic_bp REAL,
    height_cm REAL,
    weight_kg REAL,
    bmi REAL,
    FOREIGN KEY (visit_id)
        REFERENCES visits (visit_id)
);
