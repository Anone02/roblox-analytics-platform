import psycopg2

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="roblox_db",
        user="admin",
        password="admin",
        port=5432
    )
    return conn