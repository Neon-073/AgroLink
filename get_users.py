import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'Neon@503810'),
    database=os.getenv('DB_NAME', 'user')
)
cursor = conn.cursor(dictionary=True)

cursor.execute('SELECT user_id, username, phone_number, role FROM user_details LIMIT 10')
print('Available users:')
for row in cursor.fetchall():
    print(f"  ID: {row['user_id']}, Username: {row['username']}, Phone: {row['phone_number']}, Role: {row['role']}")

cursor.close()
conn.close()
