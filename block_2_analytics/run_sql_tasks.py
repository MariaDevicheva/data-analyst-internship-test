import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
SQL_DIR = BASE_DIR / "sql_python_tasks_2_4"
RESULTS_DIR = BASE_DIR / "results"
DB_PATH = RESULTS_DIR / "block_2_sql_tasks.db"

RESULTS_DIR.mkdir(exist_ok=True)


def run_sql_script(sql_file: Path) -> None:
    conn = sqlite3.connect(DB_PATH)
    sql = sql_file.read_text(encoding="utf-8")
    conn.executescript(sql)
    conn.close()


def export_query(query: str, output_file: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()

    df.to_csv(RESULTS_DIR / output_file, index=False)
    print(f"\n{output_file}")
    print(df)


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    print("Запуск SQL-задач...")

    run_sql_script(SQL_DIR / "task_2_id_chains.sql")
    export_query(
        """
        WITH RECURSIVE chain AS (
            SELECT id AS source_id, id AS connected_id
            FROM users

            UNION

            SELECT c.source_id, l.id2
            FROM chain c
            JOIN links l ON c.connected_id = l.id1

            UNION

            SELECT c.source_id, l.id1
            FROM chain c
            JOIN links l ON c.connected_id = l.id2
        )
        SELECT source_id AS id, MIN(connected_id) AS new_id
        FROM chain
        GROUP BY source_id
        ORDER BY id;
        """,
        "task_2_result.csv",
    )

    run_sql_script(SQL_DIR / "task_4_symmetric_pairs.sql")
    export_query(
        """
        SELECT
            i1.id AS id1,
            i2.id AS id2,
            i1.name AS name,
            i1.category AS category
        FROM items i1
        JOIN items i2
            ON i1.name = i2.name
            AND i1.category = i2.category
            AND i1.id < i2.id
        ORDER BY
            i1.category,
            i1.name,
            i1.id;
        """,
        "task_4_result.csv",
    )

    print("\nSQLite-база создана:")
    print(DB_PATH)


if __name__ == "__main__":
    main()