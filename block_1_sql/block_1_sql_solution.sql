-- Задача 1. Самый прослушиваемый Rock-альбом
SELECT
    al.title AS album,
    ar.name AS artist,
    COUNT(*) AS listens
FROM listening_logs AS ll
JOIN songs AS s
    ON ll.song_id = s.song_id
JOIN albums AS al
    ON s.album_id = al.album_id
JOIN artists AS ar
    ON al.artist_id = ar.artist_id
JOIN song_genres AS sg
    ON s.song_id = sg.song_id
JOIN genres AS g
    ON sg.genre_id = g.genre_id
WHERE g.name = 'Rock'
GROUP BY
    al.album_id,
    al.title,
    ar.name
ORDER BY
    listens DESC,
    album
LIMIT 1;

-- Задача 2. Кто в топ-20% по хитам
WITH song_listens AS (
    SELECT
        s.song_id,
        COUNT(ll.user_id) AS listens
    FROM songs AS s
    LEFT JOIN listening_logs AS ll
        ON s.song_id = ll.song_id
    GROUP BY s.song_id
),
ranked_songs AS (
    SELECT
        song_id,
        listens,
        NTILE(5) OVER (ORDER BY listens DESC) AS listen_group
    FROM song_listens
),
top_songs AS (
    SELECT song_id
    FROM ranked_songs
    WHERE listen_group = 1
)
SELECT
    ar.name AS artist,
    COUNT(DISTINCT ts.song_id) AS top_songs
FROM top_songs AS ts
JOIN song_artists AS sa
    ON ts.song_id = sa.song_id
JOIN artists AS ar
    ON sa.artist_id = ar.artist_id
GROUP BY
    ar.artist_id,
    ar.name
ORDER BY
    top_songs DESC,
    artist
LIMIT 1;


-- Задача 3. Альбом с самой крутой коллаборацией
WITH collab_songs AS (
    SELECT
        song_id
    FROM song_artists
    GROUP BY song_id
    HAVING COUNT(DISTINCT artist_id) > 1
)

SELECT
    al.title AS album,
    ar.name AS artist,
    COUNT(*) AS collab_count
FROM collab_songs cs
JOIN songs s
    ON cs.song_id = s.song_id
JOIN albums al
    ON s.album_id = al.album_id
JOIN artists ar
    ON al.artist_id = ar.artist_id
GROUP BY
    al.album_id,
    al.title,
    ar.name
ORDER BY
    collab_count DESC,
    album
LIMIT 1;

-- Задача 4. Динамика прослушиваний по месяцам
SELECT
    strftime('%Y-%m', listen_time) AS year_month,
    COUNT(*) AS total_listens
FROM listening_logs
GROUP BY
    year_month
ORDER BY
    year_month;

-- Задача 5. Популярность жанров по регионам
SELECT
    g.name AS genre,
    ll.region,
    COUNT(*) AS total_listens
FROM listening_logs ll
JOIN song_genres sg
    ON ll.song_id = sg.song_id
JOIN genres g
    ON sg.genre_id = g.genre_id
GROUP BY
    g.name,
    ll.region
ORDER BY
    g.name,
    total_listens DESC;

