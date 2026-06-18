-- Задача 2. Цепочки ID

-- Даны таблицы:
-- users(id, new_id)
-- links(id1, id2)
--
-- links описывает историю изменений ID пользователя.
-- Например: 1 -> 2 -> 3 -> 5
--
-- Нужно для каждого исходного id определить единый финальный new_id:
-- минимальный id внутри всей цепочки.
--
-- Ожидаемый пример:
-- 1, 2, 3, 5 -> 1
-- 4 -> 4
-- 7, 8 -> 7
--
-- В файле представлены два подхода:
-- 1. Рекурсивный
-- 2. Нерекурсивный

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS links;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    new_id INTEGER
);

CREATE TABLE links (
    id1 INTEGER,
    id2 INTEGER
);

INSERT INTO users (id, new_id) VALUES
(1, NULL),
(2, NULL),
(3, NULL),
(4, NULL),
(5, NULL),
(7, NULL),
(8, NULL);

INSERT INTO links (id1, id2) VALUES
(1, 2),
(2, 3),
(3, 5),
(7, 8);


-- Подход 1. Рекурсивный

-- Строим все достижимые связи внутри цепочки.
-- Затем для каждого id выбираем минимальный id в его компоненте.

WITH RECURSIVE chain AS (
    SELECT
        u.id AS source_id,
        u.id AS connected_id
    FROM users u

    UNION

    SELECT
        c.source_id,
        l.id2 AS connected_id
    FROM chain c
    JOIN links l
        ON c.connected_id = l.id1

    UNION

    SELECT
        c.source_id,
        l.id1 AS connected_id
    FROM chain c
    JOIN links l
        ON c.connected_id = l.id2
)

SELECT
    source_id AS id,
    MIN(connected_id) AS new_id
FROM chain
GROUP BY source_id
ORDER BY id;


-- Подход 2. Нерекурсивный

-- Вариант без WITH RECURSIVE.
-- Работает для ограниченной глубины цепочки.
-- В примере максимальная цепочка: 1 -> 2 -> 3 -> 5.
--
-- Идея:
-- вручную раскрываем несколько уровней связей через LEFT JOIN,
-- затем собираем все найденные id и выбираем минимальный.

WITH expanded AS (
    SELECT
        u.id AS id,
        u.id AS id0,
        l1.id2 AS id1,
        l2.id2 AS id2,
        l3.id2 AS id3
    FROM users u
    LEFT JOIN links l1
        ON u.id = l1.id1
    LEFT JOIN links l2
        ON l1.id2 = l2.id1
    LEFT JOIN links l3
        ON l2.id2 = l3.id1
),
unpivoted AS (
    SELECT id, id0 AS chain_id
    FROM expanded

    UNION ALL

    SELECT id, id1 AS chain_id
    FROM expanded
    WHERE id1 IS NOT NULL

    UNION ALL

    SELECT id, id2 AS chain_id
    FROM expanded
    WHERE id2 IS NOT NULL

    UNION ALL

    SELECT id, id3 AS chain_id
    FROM expanded
    WHERE id3 IS NOT NULL
)

SELECT
    id,
    MIN(chain_id) AS new_id
FROM unpivoted
GROUP BY id
ORDER BY id;