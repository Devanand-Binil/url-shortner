-- DROP TABLE IF EXISTS urls;

CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime', '+5 hours', '+30 minutes')),
    original_url TEXT ,
    last_updated TEXT ,
    referrer TEXT,
    clicks INTEGER NOT NULL DEFAULT 0
    
);
