CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    currency TEXT,
    order_timestamp TIMESTAMP,
    status TEXT,
    order_amount REAL
);