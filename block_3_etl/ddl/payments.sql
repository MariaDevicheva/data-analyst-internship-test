CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    payment_method TEXT,
    amount REAL,
    currency TEXT,
    payment_timestamp TIMESTAMP
);