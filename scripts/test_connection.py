from src.utils.db import connect_db

conn = connect_db()
print("Connected successfully!")
conn.close()