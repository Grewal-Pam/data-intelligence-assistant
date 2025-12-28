# Data Model — Data Intelligence Assistant

## Purpose
This document defines the conceptual and logical data model used by the
Data Intelligence Assistant. The model is designed to support longitudinal,
cohort-based analysis while preserving data integrity, reproducibility,
and interpretability.

The model separates real-world entities (participants, visits, measurements)
from derived analytical outputs.

---

## Core Entities

### Participant
Represents a single individual enrolled in the study.

**Characteristics**
- Identified by a unique participant_id
- Attributes are static over time
- Does not contain time-varying or measurement data

**Examples**
- Sex
- Date of birth

---

### Visit
Represents a timepoint at which a participant is observed.

**Characteristics**
- Belongs to exactly one participant
- Encodes all temporal information
- Serves as the anchor for longitudinal analysis

**Examples**
- Baseline visit
- Follow-up visit

---

### Measurement
Represents any observed value collected during a visit.

**Characteristics**
- Belongs to exactly one visit
- Can represent different domains (survey, vitals, labs)
- Does not encode time directly

**Examples**
- Blood pressure
- BMI
- Smoking status
- Sleep duration

---

### Derived Insight
Represents computed or aggregated results derived from curated data.

**Characteristics**
- Never overwrites source data
- Fully reproducible from curated inputs
- Used for scientific interpretation and reporting

**Examples**
- BMI change between visits
- Average blood pressure by smoking status

---

## Relationships

- A Participant can have multiple Visits
- A Visit belongs to exactly one Participant
- A Visit can have multiple Measurements
- Derived Insights depend on Participants, Visits, and Measurements

---

## Design Principles

- Time is modeled explicitly through the Visit entity
- Raw and curated data are immutable
- Measurements are always visit-linked
- Derived data is stored separately from source data
- Schema design prioritizes correctness over convenience

---

## Rationale

This model ensures that longitudinal analyses are explicit and safe,
prevents accidental mixing of time-varying and static attributes,
and supports extensibility to additional data domains such as
biomaterial analyses and laboratory results.
