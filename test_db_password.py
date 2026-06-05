import mysql.connector
from mysql.connector import Error

test_passwords = ['Neoa@503810', 'Neon@503810', 'root', '', 'password', '123456']
for pwd in test_passwords:
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=pwd,
            database='user'
        )
        print(f'✅ Connection successful with password: "{pwd}"')
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) as count FROM user_details')
        result = cursor.fetchone()
        print(f'   Users in database:  {result["count"]}')
        cursor.close()
        conn.close()
        break
    except Error as e:
        print(f'❌ Password "{pwd}" failed')
