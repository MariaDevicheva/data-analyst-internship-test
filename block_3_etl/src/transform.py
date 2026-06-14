from pathlib import Path

import pandas as pd


LOG_PATH = Path("logs/data_quality.log")


def log_quality_issue(message: str) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)

    with open(LOG_PATH, "a", encoding="utf-8") as file:
        file.write(message + "\n")


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    df = customers.copy()

    df = df.drop_duplicates(subset=["customer_id"])
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    df["full_name"] = df["full_name"].astype(str).str.strip()
    df["email"] = df["email"].astype(str).str.lower().str.strip()
    df["phone"] = df["phone"].astype(str).str.strip()
    df["city"] = df["city"].astype(str).str.strip()

    df = df.dropna(subset=["customer_id", "created_at"])

    df["customer_id"] = df["customer_id"].astype(int)

    return df


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    df = products.copy()

    df = df.drop_duplicates(subset=["product_id"])

    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["currency"] = df["currency"].astype(str).str.strip()

    df = df.dropna(
        subset=[
            "product_id",
            "product_name",
            "category",
            "price",
            "currency",
        ]
    )

    df = df[df["price"] > 0]

    df["product_id"] = df["product_id"].astype(int)

    return df


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    df = orders.copy()

    df = df.drop_duplicates(subset=["order_id"])

    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")
    df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    df["order_timestamp"] = pd.to_datetime(
        df["order_timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    df["currency"] = df["currency"].astype(str).str.strip()
    df["status"] = df["status"].astype(str).str.strip()

    df = df.dropna(
        subset=[
            "order_id",
            "customer_id",
            "product_id",
            "quantity",
            "unit_price",
            "currency",
            "order_timestamp",
            "status",
        ]
    )

    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

    df["order_id"] = df["order_id"].astype(int)
    df["customer_id"] = df["customer_id"].astype(int)
    df["product_id"] = df["product_id"].astype(int)
    df["quantity"] = df["quantity"].astype(int)

    df["order_amount"] = df["quantity"] * df["unit_price"]

    return df


def clean_payments(payments: pd.DataFrame) -> pd.DataFrame:
    df = payments.copy()

    df = df.drop_duplicates(subset=["payment_id"])

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["payment_timestamp"] = pd.to_datetime(
        df["payment_timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    df["payment_method"] = df["payment_method"].astype(str).str.strip()
    df["currency"] = df["currency"].astype(str).str.strip()

    df = df.dropna(
        subset=[
            "payment_id",
            "order_id",
            "payment_method",
            "amount",
            "currency",
            "payment_timestamp",
        ]
    )

    df = df[df["amount"] > 0]

    df["payment_id"] = df["payment_id"].astype(int)
    df["order_id"] = df["order_id"].astype(int)

    return df


def clean_events(events: pd.DataFrame) -> pd.DataFrame:
    df = events.copy()

    df = df.drop_duplicates(subset=["event_id"])

    df["event_id"] = pd.to_numeric(df["event_id"], errors="coerce")
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")
    df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce")

    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    df["event_type"] = df["event_type"].astype(str).str.strip()

    df = df.dropna(
        subset=[
            "event_id",
            "customer_id",
            "event_type",
            "event_timestamp",
        ]
    )

    df["event_id"] = df["event_id"].astype(int)
    df["customer_id"] = df["customer_id"].astype(int)

    df["product_id"] = df["product_id"].astype("Int64")

    return df


def transform_data(raw_data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    if LOG_PATH.exists():
        LOG_PATH.unlink()

    clean_data = {
        "customers": clean_customers(raw_data["customers"]),
        "orders": clean_orders(raw_data["orders"]),
        "products": clean_products(raw_data["products"]),
        "payments": clean_payments(raw_data["payments"]),
        "events": clean_events(raw_data["events"]),
    }

    for table_name in raw_data:
        raw_rows = len(raw_data[table_name])
        clean_rows = len(clean_data[table_name])
        removed_rows = raw_rows - clean_rows

        log_quality_issue(
            f"{table_name}: raw_rows={raw_rows}, clean_rows={clean_rows}, removed_rows={removed_rows}"
        )

    return clean_data