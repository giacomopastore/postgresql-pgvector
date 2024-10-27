import os
from dotenv import load_dotenv
import psycopg2
import numpy as np

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()

# Insert a vector
embedding = np.array([4.5, 5.5, 6.5])
cur.execute("INSERT INTO items (embedding) VALUES (%s)", (embedding.tolist(),))

# Perform a similarity search
query_vector = np.array([4.3, 5.3, 6.3])
cur.execute("SELECT * FROM items ORDER BY embedding <-> %s::vector(3) LIMIT 1", (query_vector.tolist(),))
result = cur.fetchone()
print(f"Nearest neighbor: {result}")

conn.commit()
cur.close()
conn.close()