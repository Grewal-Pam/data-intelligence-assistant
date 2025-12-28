# Design Intent — Data Intelligence Assistant

## Goal
Enable trustworthy, longitudinal analysis of cohort study data
by separating participants, visits, and measurements, and by
preserving temporal meaning throughout the data lifecycle.

## Core Principles
- Raw data is immutable
- Time is modeled explicitly via visits
- All measurements are visit-linked
- Derived results never overwrite source data
- Every result must be explainable and reproducible

## Core Entities

### Participant
Represents a single enrolled individual.
Contains only static attributes that do not change over time.

### Visit
Represents a timepoint of observation for a participant.
All temporal logic is anchored here.

### Measurement
Represents any observed value collected during a visit.
Measurements are domain-agnostic and extensible.

### Derived Insight
Represents computed results used for scientific interpretation.
Derived data is stored separately from source data.

## Intended Outcomes
- Support longitudinal comparisons
- Enable safe joins across domains
- Reduce analysis errors
- Improve scientist productivity
