from src.utils.db import connect_db
from datetime import datetime

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO events (user_id, event_type, event_time)
    VALUES (%s, %s, %s)
""", (user_id, event_type, event_time)
)

conn.commit()

print("Data inserted!")

cursor.close()
conn.close()