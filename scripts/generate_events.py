from src.utils.db import connect_db
from datetime import datetime
import random
import time

# CONFIG
NUM_USERS = 100
NUM_EVENTS = 1000  # total event yg mau di-generate

event_types = ["login", "logout", "purchase", "collect_item"]
items = ["sword", "shield", "potion", "hat"]

conn = connect_db()
cursor = conn.cursor()

for _ in range(NUM_EVENTS):
    user_id = random.randint(1, NUM_USERS)
    event_type = random.choice(event_types)
    item = random.choice(items) if event_type == "purchase" or event_type == "collect_item" else None
    price = random.randint(10, 100) if event_type == "purchase" else None

    cursor.execute(
        """
        INSERT INTO events (user_id, event_type, item, price, event_time)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, event_type, item, price, datetime.now())
    )

    # biar keliatan real-time-ish, bisa sleep 0.01 detik
    time.sleep(0.01)

conn.commit()
cursor.close()
conn.close()

print(f"{NUM_EVENTS} events generated successfully!")