from src.utils.db import connect_db
from datetime import datetime

conn = connect_db()
cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO events (user_id, event_type, item, price, event_time)
    VALUES (%s, %s, %s, %s, %s)
    """,
    (1, "purchase", "sword", 50, datetime.now())
)

conn.commit()

print("Data inserted!")

cursor.close()
conn.close()