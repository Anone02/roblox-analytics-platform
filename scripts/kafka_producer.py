from kafka import KafkaProducer
import json
import random
from datetime import datetime, timedelta
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

NUM_USERS = 100

event_types = ["login", "logout", "purchase", "collect_item"]
items = ["sword", "shield", "potion", "hat"]

# 🎯 user profile (behavior simulation)
user_profiles = {}
user_first_seen = {}

for user_id in range(1, NUM_USERS + 1):
    user_profiles[user_id] = random.choices(
        ["casual", "active", "spender", "whale"],
        weights=[50, 30, 15, 5]
    )[0]

    # 🎯 tentukan hari pertama user join
    user_first_seen[user_id] = datetime.now() - timedelta(days=random.randint(0, 2))

while True:
    user_id = random.randint(1, NUM_USERS)
    profile = user_profiles[user_id]

    base_time = user_first_seen[user_id]
    # event hanya setelah user join
    event_time = base_time + timedelta(seconds=random.randint(0, 86400 * 2))

    # 🎯 behavior berdasarkan tipe user
    if profile == "casual":
        event_type = random.choices(
            ["login", "logout", "collect_item"],
            weights=[50, 30, 20]
        )[0]

    elif profile == "active":
        event_type = random.choices(
            ["login", "logout", "collect_item", "purchase"],
            weights=[35, 30, 30, 5]
        )[0]

    elif profile == "spender":
        event_type = random.choices(
            ["login", "logout", "collect_item", "purchase"],
            weights=[30, 25, 25, 20]
        )[0]

    else:  # whale 🐋
        event_type = random.choices(
            ["login", "logout", "purchase"],
            weights=[30, 20, 50]
        )[0]

    item = random.choice(items) if event_type in ["purchase", "collect_item"] else None

    # 💰 harga beda tergantung tipe
    if event_type == "purchase":
        if profile == "whale":
            price = random.randint(100, 500)
        elif profile == "spender":
            price = random.randint(50, 200)
        else:
            price = random.randint(10, 100)
    else:
        price = None

    event = {
        "user_id": user_id,
        "event_type": event_type,
        "item": item,
        "price": price,
        "event_time": event_time.isoformat()
    }

    producer.send('roblox_events', value=event)
    print(f"[{profile.upper()}] Sent:", event)

    time.sleep(0.05)