CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(50),
    item VARCHAR(50),
    price INT,
    event_time TIMESTAMP
);