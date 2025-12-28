import pandas as pd
from pathlib import Path
from typing import Optional, Dict

from core.db import get_connection

# Base directory resolution
BASE_DIR = Path(__file__).resolve().parent.parent
QUERY_DIR = BASE_DIR / "queries" / "analysis"
DB_PATH = BASE_DIR / "data" / "intelligence.db"


def run_query(
    query_file: str,
    params: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Execute a SQL query from the queries directory and return results
    as a pandas DataFrame.

    Parameters
    ----------
    query_file : str
        Name of the SQL file to execute.
    params : dict, optional
        Query parameters for parameterized SQL.

    Returns
    -------
    pd.DataFrame
        Query result.
    """
    query_path = QUERY_DIR / query_file

    if not query_path.exists():
        raise FileNotFoundError(f"Query file not found: {query_file}")

    with open(query_path, "r") as f:
        sql = f.read()

    conn = get_connection(DB_PATH)

    df = pd.read_sql(
        sql,
        conn,
        params=params
    )

    conn.close()
    return df


if __name__ == "__main__":
    # Example usage
    df = run_query("bmi_change.sql")
    print(df.head())
