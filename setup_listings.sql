-- Purpose: Create SQLite database schema for storing real estate listings

CREATE TABLE IF NOT EXISTS Listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    address TEXT NOT NULL,
    price REAL,
    bedrooms INTEGER,
    bathrooms REAL,
    square_footage INTEGER,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Index for faster queries by user_name
CREATE INDEX IF NOT EXISTS idx_user_name ON Listings (user_name);
