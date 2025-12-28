import sqlite3
from pathlib import Path


def get_connection(db_path: Path) -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.
    """
    return sqlite3.connect(db_path)


def initialize_schema(db_path: Path, schema_path: Path) -> None:
    """
    Initialize the database schema by executing the SQL file.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Default paths (can be overridden later)
    db_path = Path("data/intelligence.db")
    schema_path = Path("schemas/schema.sql")

    db_path.parent.mkdir(parents=True, exist_ok=True)

    initialize_schema(db_path, schema_path)
    print("Database schema initialized successfully.")
