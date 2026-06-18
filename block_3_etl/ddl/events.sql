CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    event_type TEXT,
    event_timestamp TIMESTAMP
);