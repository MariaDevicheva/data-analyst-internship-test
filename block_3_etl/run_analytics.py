from pathlib import Path
import sqlite3

import pandas as pd


DB_PATH = Path("music_analytics.db")
RESULTS_DIR = Path("results")

RESULTS_DIR.mkdir(exist_ok=True)


QUERIES = {
    "query_1_revenue_by_status": """
        SELECT
            status,
            COUNT(*) AS orders_count,
            ROUND(SUM(order_amount), 2) AS total_order_amount,
            ROUND(AVG(order_amount), 2) AS avg_order_amount
        FROM orders
        GROUP BY status
        ORDER BY total_order_amount DESC;
    """,

    "query_2_top_product_categories": """
        SELECT
            p.category,
            COUNT(o.order_id) AS orders_count,
            SUM(o.quantity) AS total_quantity,
            ROUND(SUM(o.order_amount), 2) AS total_order_amount
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_order_amount DESC;
    """,

    "query_3_payment_methods": """
        SELECT
            payment_method,
            COUNT(*) AS payments_count,
            ROUND(SUM(amount), 2) AS total_payment_amount,
            ROUND(AVG(amount), 2) AS avg_payment_amount
        FROM payments
        GROUP BY payment_method
        ORDER BY payments_count DESC;
    """,

    "query_4_events_by_type": """
        SELECT
            event_type,
            COUNT(*) AS events_count,
            COUNT(DISTINCT customer_id) AS unique_customers
        FROM events
        GROUP BY event_type
        ORDER BY events_count DESC;
    """,

    "query_5_top_customers": """
        SELECT
            c.customer_id,
            c.full_name,
            c.city,
            COUNT(o.order_id) AS orders_count,
            ROUND(SUM(o.order_amount), 2) AS total_order_amount
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        GROUP BY
            c.customer_id,
            c.full_name,
            c.city
        ORDER BY total_order_amount DESC
        LIMIT 10;
    """,
}


def run_query(conn: sqlite3.Connection, name: str, query: str) -> None:
    df = pd.read_sql_query(query, conn)

    output_path = RESULTS_DIR / f"{name}.csv"
    df.to_csv(output_path, index=False)

    print(f"\n{name}.csv")
    print(df)


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "Database not found. Run `python src/main.py` before analytics."
        )

    conn = sqlite3.connect(DB_PATH)

    for name, query in QUERIES.items():
        run_query(conn, name, query)

    conn.close()

    print("\nAnalytics results saved to results/")


if __name__ == "__main__":
    main()