-- 1. Топ-10 клиентов по сумме заказов
SELECT
    c.customer_id,
    c.full_name,
    c.email,
    ROUND(SUM(o.order_amount), 2) AS total_order_amount
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY
    c.customer_id,
    c.full_name,
    c.email
ORDER BY total_order_amount DESC
LIMIT 10;


-- 2. Выручка по месяцам
SELECT
    strftime('%Y-%m', o.order_timestamp) AS month,
    ROUND(SUM(o.order_amount), 2) AS revenue
FROM orders o
WHERE o.status = 'completed'
GROUP BY month
ORDER BY month;


-- 3. Самые популярные товары по количеству проданных единиц
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS total_quantity_sold,
    ROUND(SUM(o.order_amount), 2) AS total_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_quantity_sold DESC
LIMIT 10;


-- 4. Последняя активность топ-5 клиентов по сумме заказов
WITH top_customers AS (
    SELECT
        customer_id,
        SUM(order_amount) AS total_order_amount
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
    ORDER BY total_order_amount DESC
    LIMIT 5
)
SELECT
    c.customer_id,
    c.full_name,
    ROUND(tc.total_order_amount, 2) AS total_order_amount,
    MAX(e.event_timestamp) AS last_activity
FROM top_customers tc
JOIN customers c
    ON tc.customer_id = c.customer_id
LEFT JOIN events e
    ON tc.customer_id = e.customer_id
GROUP BY
    c.customer_id,
    c.full_name,
    tc.total_order_amount
ORDER BY total_order_amount DESC;


-- 5. Клиенты без заказов
SELECT
    c.customer_id,
    c.full_name,
    c.email,
    c.city,
    c.created_at
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;