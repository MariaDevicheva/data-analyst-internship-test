import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def read_events_xml(path: Path) -> pd.DataFrame:
    tree = ET.parse(path)
    root = tree.getroot()

    rows = []

    for event in root:
        row = {}
        for child in event:
            row[child.tag] = child.text
        rows.append(row)

    return pd.DataFrame(rows)


def extract_data() -> dict[str, pd.DataFrame]:
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    orders = pd.read_json(DATA_DIR / "orders.json")
    products = pd.read_excel(DATA_DIR / "products.xlsx")
    payments = pd.read_csv(DATA_DIR / "payments.csv", sep="^")
    events = read_events_xml(DATA_DIR / "events.xml")

    return {
        "customers": customers,
        "orders": orders,
        "products": products,
        "payments": payments,
        "events": events,
    }