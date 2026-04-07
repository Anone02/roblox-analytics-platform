from kafka import KafkaConsumer
import json
from src.utils.db import connect_db
from datetime import datetime
print("🔥 Consumer started...")
consumer = KafkaConsumer(
    'roblox_events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = connect_db()
cursor = conn.cursor()

# Pastikan tabel sudah ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(50),
    item VARCHAR(50),
    price INT,
    event_time TIMESTAMP
);
""")
conn.commit()

# simpan session aktif di memory
active_sessions = {}

try:
    for message in consumer:
        event = message.value
        print("📥 Message received:", event)

        user_id = event['user_id']
        event_type = event['event_type']
        item = event['item']
        price = event['price']
        event_time = datetime.fromisoformat(event['event_time'])

        # USER
        cursor.execute("""
            INSERT INTO users (id, username)
            VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (user_id, f"user_{user_id}"))

        # EVENTS
        cursor.execute("""
            INSERT INTO events (user_id, event_type, event_time)
            VALUES (%s, %s, %s)
        """, (user_id, event_type, event_time))

        # TRANSACTION
        if event_type == "purchase":
            cursor.execute("""
                INSERT INTO transactions (user_id, item, price, event_time)
                VALUES (%s, %s, %s, %s)
            """, (user_id, item, price, event_time))

        # SESSION LOGIC
        if event_type == "login":
            active_sessions[user_id] = event_time

        elif event_type == "logout":
            if user_id in active_sessions:
                start_time = active_sessions[user_id]
                end_time = event_time
                duration = end_time - start_time

                cursor.execute("""
                    INSERT INTO sessions (user_id, start_time, end_time, duration)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, start_time, end_time, duration))

                del active_sessions[user_id]

        conn.commit()

        print("Processed:", event)

except KeyboardInterrupt:
    print("🛑 Stopping consumer...")