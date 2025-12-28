import pandas as pd
from pathlib import Path
from core.db import get_connection


def load_participants(conn, df: pd.DataFrame):
    df = (
    df[["participant_id", "sex", "dob"]]
    .drop_duplicates("participant_id")
    .rename(columns={"dob": "date_of_birth"})
)


    df.to_sql(
        "participants",
        conn,
        if_exists="append",
        index=False
    )


def load_visits(conn, df: pd.DataFrame):
    df = df.sort_values(["participant_id", "visit_date"])
    df["visit_type"] = (
        df.groupby("participant_id").cumcount()
        .apply(lambda x: "baseline" if x == 0 else "followup")
    )

    visits = df[["participant_id", "visit_date", "visit_type"]]

    visits.to_sql(
        "visits",
        conn,
        if_exists="append",
        index=False
    )


def load_survey_measurements(conn, survey_df: pd.DataFrame):
    visit_map = pd.read_sql(
        "SELECT visit_id, participant_id, visit_date FROM visits",
        conn,
        parse_dates=["visit_date"]
    )

    df = survey_df.merge(
        visit_map,
        on=["participant_id", "visit_date"],
        how="inner"
    )

    df["smoking"] = df["smoking"].replace(9, None)

    survey = df[
        ["visit_id", "smoking", "alcohol", "education", "sleep_hours"]
    ]

    survey.to_sql(
        "survey_measurements",
        conn,
        if_exists="append",
        index=False
    )


def load_vital_measurements(conn, vitals_df: pd.DataFrame):
    visit_map = pd.read_sql(
        "SELECT visit_id, participant_id, visit_date FROM visits",
        conn,
        parse_dates=["visit_date"]
    )

    df = vitals_df.merge(
        visit_map,
        on=["participant_id", "visit_date"],
        how="inner"
    )

    df["bmi"] = df["weight_kg"] / (df["height_cm"] / 100) ** 2

    vitals = df[
        ["visit_id", "systolic_bp", "diastolic_bp",
         "height_cm", "weight_kg", "bmi"]
    ]

    vitals.to_sql(
        "vital_measurements",
        conn,
        if_exists="append",
        index=False
    )


if __name__ == "__main__":
    db_path = Path("data/intelligence.db")
    conn = get_connection(db_path)

    survey = pd.read_csv("data_raw/survey_wide.csv", parse_dates=["visit_date"])
    vitals = pd.read_csv("data_raw/vitals_wide.csv", parse_dates=["visit_date"])

    load_participants(conn, survey)
    load_visits(conn, survey)
    load_survey_measurements(conn, survey)
    load_vital_measurements(conn, vitals)

    conn.close()
    print("Data loaded safely.")
