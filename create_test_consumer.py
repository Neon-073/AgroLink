import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'Neon@503810'),
    database=os.getenv('DB_NAME', 'user')
)
cursor = conn.cursor()

# Create test consumer user
username = 'demo_consumer'
password = 'Demo@123'
phone = '9999999999'
hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

try:
    # Insert user
    query = '''INSERT INTO user_details 
    (username, password, phone_number, role, location) 
    VALUES (%s, %s, %s, %s, %s)'''
    
    cursor.execute(query, (username, hashed_pw, phone, 'consumer', 'Delhi'))
    conn.commit()
    
    cursor.execute('SELECT LAST_INSERT_ID()')
    user_id = cursor.fetchone()[0]
    
    print(f'✅ Created test consumer user:')
    print(f'   User ID: {user_id}')
    print(f'   Username: {username}')
    print(f'   Password: {password}')
    print(f'   Phone: {phone}')
    
except Exception as e:
    print(f'❌ Error: {e}')

cursor.close()
conn.close()
