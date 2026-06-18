-- Задача 4. Поиск симметричных пар
-- Необходимо найти пары товаров,
-- имеющих одинаковые name и category.
--
-- Выводим каждую пару только один раз.
-- Поэтому используем условие:
--
-- i1.id < i2.id
--
-- чтобы избежать дублей вида:
--
-- (1,2) и (2,1)
DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT
);

INSERT INTO items (id, name, category) VALUES
(1, 'phone', 'electronics'),
(2, 'phone', 'electronics'),
(3, 'laptop', 'electronics'),
(4, 'laptop', 'electronics'),
(5, 'book', 'books'),
(6, 'book', 'books'),
(7, 'phone', 'accessories'),
(8, 'phone', 'accessories'),
(9, 'chair', 'home');

-- Решение
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