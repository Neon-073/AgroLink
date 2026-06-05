#!/usr/bin/env python3
"""
Add sample products to shop database for marketplace testing
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'Neon@503810'),
    database=os.getenv('DB_NAME', 'user')
)
cursor = conn.cursor()

# Sample products
products = [
    ('Alphonso Mango (1 Dozen)', 380, 'GI certified Hapus from Ratnagiri', 1, 'farmer', 'https://via.placeholder.com/300?text=Mango', 'Fruits', 50),
    ('Thompson Seedless Grapes', 140, 'Export quality, Nashik vineyard', 2, 'farmer', 'https://via.placeholder.com/300?text=Grapes', 'Fruits', 30),
    ('Heirloom Tomatoes', 60, 'Chemical-free, 5 heirloom varieties', 1, 'farmer', 'https://via.placeholder.com/300?text=Tomatoes', 'Vegetables', 100),
    ('Fresh Cucumber (5kg box)', 175, 'Morning harvest, same-day dispatch', 2, 'farmer', 'https://via.placeholder.com/300?text=Cucumber', 'Vegetables', 40),
    ('Sharbati Wheat Flour', 85, 'Stone-ground, golden Sharbati wheat', 1, 'farmer', 'https://via.placeholder.com/300?text=Wheat', 'Grains', 75),
    ('Organic Weekly Veggie Box', 350, '6 seasonal greens + herbs, certified organic', 2, 'farmer', 'https://via.placeholder.com/300?text=VeggieBox', 'Organic', 25),
    ('Raw Coconut', 30, 'Fresh Ratnagiri coast coconuts', 1, 'farmer', 'https://via.placeholder.com/300?text=Coconut', 'Fruits', 200),
    ('Green Chillies', 40, 'Fiery Byadagi variety, fresh picked', 1, 'farmer', 'https://via.placeholder.com/300?text=Chillies', 'Spices', 60),
    ('Fresh Curry Leaves', 25, 'Organic curry leaves, full flavour', 2, 'farmer', 'https://via.placeholder.com/300?text=CurryLeaves', 'Spices', 80),
    ('Bitter Gourd', 50, 'Fresh karela, ideal for diabetes diet', 2, 'farmer', 'https://via.placeholder.com/300?text=BitterGourd', 'Vegetables', 70),
    ('Chickpea (Chana) 2kg', 180, 'Desi chana, high protein, unprocessed', 1, 'farmer', 'https://via.placeholder.com/300?text=Chickpea', 'Grains', 45),
    ('Pomegranate', 120, 'Bhagwa pomegranate, juicy & sweet', 2, 'farmer', 'https://via.placeholder.com/300?text=Pomegranate', 'Fruits', 55),
]

# Check if products already exist
cursor.execute('SELECT COUNT(*) FROM shop')
count = cursor.fetchone()[0]

if count == 0:
    query = '''INSERT INTO shop 
    (product_name, product_price, product_description, product_owner_id, owner_role, product_photo, category, stock_quantity) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    
    for product in products:
        cursor.execute(query, product)
    
    conn.commit()
    print(f'✅ Added {len(products)} sample products to shop database')
    
    # Show inserted products
    cursor.execute('SELECT product_id, product_name, product_price, category FROM shop')
    for row in cursor.fetchall():
        print(f'   {row[0]}. {row[1]} - ₹{row[2]} ({row[3]})')
else:
    print(f'⚠️  Database already has {count} products. Skipping insert.')
    print('\nExisting products:')
    cursor.execute('SELECT product_id, product_name, product_price, category FROM shop LIMIT 15')
    for row in cursor.fetchall():
        print(f'   {row[0]}. {row[1]} - ₹{row[2]} ({row[3]})')

cursor.close()
conn.close()
