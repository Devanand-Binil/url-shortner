-- DROP TABLE IF EXISTS urls;

CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
    original_url TEXT ,
    ip TEXT ,
    country TEXT,
    clicks INTEGER NOT NULL DEFAULT 0
    
);