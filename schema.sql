-- DROP TABLE IF EXISTS urls;

CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CONVERT_TZ(CURRENT_TIMESTAMP(), 'UTC', 'Asia/Kolkata'),
    original_url TEXT ,
    last_updated TEXT ,
    referrer TEXT,
    clicks INTEGER NOT NULL DEFAULT 0
    
);
