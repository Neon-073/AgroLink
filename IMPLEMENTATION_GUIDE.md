# 🚀 AgroLink v2.0 - Implementation Guide

## Overview

This guide walks you through setting up the completely redesigned AgroLink system with a **normalized database schema** and **scalable Flask backend**.

**Key Improvements:**
- ✅ Normalized database (7 tables instead of 1)
- ✅ Role-specific profile tables
- ✅ Proper Foreign Key relationships
- ✅ JWT authentication
- ✅ Production-ready API
- ✅ Comprehensive error handling

---

## 📋 Pre-Implementation Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL/MariaDB installed and running
- [ ] Git or file access to project
- [ ] Text editor (VS Code recommended)
- [ ] Postman or cURL for API testing

---

## 🔧 Installation Steps

### Step 1: Install Python Packages

```bash
cd c:\Abzar\Projects\Agro Link

# Install all required packages
pip install flask mysql-connector-python flask-cors python-dotenv bcrypt pyjwt

# Verify installation
pip list | findstr flask

# Expected output:
# Flask              2.x.x
# mysql-connector-python  8.x.x
# flask-cors         4.x.x
# python-dotenv      0.x.x
# bcrypt             4.x.x
# pyjwt              2.x.x
```

### Step 2: Set Up Database

```bash
# Open MySQL command prompt
mysql -u root -p

# Enter your MySQL password when prompted
```

**Inside MySQL:**

```sql
-- Drop old database if it exists
DROP DATABASE IF EXISTS agrolink_db;

-- Create new database
CREATE DATABASE user CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE user;

-- Copy-paste the entire schema_normalized.sql file here
-- OR execute the file directly:
source C:\Abzar\Projects\Agro Link\schema_normalized.sql;

-- Verify tables
SHOW TABLES;
```

**Expected output:**
```
consumer_details
dealer_details
farmer_details
reviews
shop
user_details
user_products
```

### Step 3: Configure Environment

```bash
# Copy example file
copy .env.example .env

# Edit .env with your credentials
# Using Notepad:
notepad .env
```

**Inside .env:**
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=user
SECRET_KEY=your-secret-key-change-in-production
JWT_EXPIRATION=86400
```

### Step 4: Test Database Connection

```bash
# In MySQL:
USE user;
SELECT * FROM user_details;

# Should return empty table (that's OK)
```

### Step 5: Start Backend

```bash
# In PowerShell/CMD:
cd c:\Abzar\Projects\Agro Link
python app_v2.py

# Expected output:
# ╔════════════════════════════════════════════════════════════════╗
# ║         🌾 AgroLink Backend (v2.0) Starting...               ║
# ║         Database: user                                        ║
# ║         Host: localhost                                       ║
# ╚════════════════════════════════════════════════════════════════╝
# ✅ Database connection successful
# 🚀 API Routes: [list of endpoints]
# WARNING in app.run() from werkzeug: Running on http://127.0.0.1:5000
```

### Step 6: Test Connection

```bash
# Open new terminal/PowerShell
# In PowerShell:
Invoke-WebRequest -Uri http://localhost:5000 -Method GET

# Or in browser:
# Visit: http://localhost:5000
```

---

## ✅ Verification Checklist

### API Endpoints

- [ ] `GET /` returns API info
- [ ] `GET /test-db` returns database stats
- [ ] `POST /auth/register` accepts user data
- [ ] `POST /auth/login` returns JWT token
- [ ] `GET /api/products` returns product list
- [ ] `POST /api/products/add` requires token

### Run Full Test Suite

```bash
# In new terminal:
python test_agrolink.py

# Should show:
# ✅ API Health
# ✅ Database Connection
# ✅ Farmer Registration
# ✅ Dealer Registration
# ✅ Login
# ✅ Get User Profile
# ✅ Add Product
# ✅ Get Products
# ✅ Get Product Details
# ✅ Add Review
# ✅ Filter Products

# Final output:
# 🎉 All tests passed!
```

---

## 📊 Database Normalization Comparison

### Old Design (v1.0)
```
users
├─ Full structure for all roles
└─ Many NULL fields for unused roles (wasteful)
```

### New Design (v2.0)
```
user_details (central)
├─ farmer_details (only for farmers)
├─ dealer_details (only for dealers)
└─ consumer_details (only for consumers)

shop (products)
├─ user_products (M2M relationship)
└─ reviews
```

**Benefits:**
- Cleaner queries (no NULL checks needed)
- Better indexing performance
- Scalable for future role types
- No wasted database space

---

## 🔐 Security Features

### Password Security
```python
# Passwords automatically hashed using bcrypt
import bcrypt

password = "user_password"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Stored in database as: $2b$12$...

# Verified on login automatically
```

### JWT Tokens
```python
# Token format:
{
  "user_id": 1,
  "role": "farmer",
  "exp": 1659999999,
  "iat": 1659913599
}

# Expires after 24 hours (configurable in .env)
```

### Protected Endpoints
```
Authorization: Bearer <TOKEN>

# Required for:
- PUT /api/user/<id>
- POST /api/products/add
- PUT /api/products/<id>
- DELETE /api/products/<id>
- POST /api/reviews
```

---

## 🧪 Testing Scenarios

### Scenario 1: Farmer Adds Product & Farmer Reviews

```bash
# 1. Farmer registers
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer_john",
    "email": "john@farm.com",
    "phone_number": "+91 9876543210",
    "password": "pass123",
    "role": "farmer",
    "farm_size": 20,
    "soil_type": "loamy"
  }'
# Get: user_id=1, token=xyz

# 2. Another farmer reviews
POST /auth/register (same as above, different email/phone)
# Get: user_id=2, token=abc

# 3. First farmer adds product
curl -X POST http://localhost:5000/api/products/add \
  -H "Authorization: Bearer xyz" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Wheat Seeds",
    "product_price": 350,
    "product_description": "Quality seeds",
    "category": "seeds",
    "stock_quantity": 100
  }'
# Get: product_id=1

# 4. Second farmer reviews product
curl -X POST http://localhost:5000/api/reviews \
  -H "Authorization: Bearer abc" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "rating": 5,
    "comment": "Great quality!"
  }'
```

### Scenario 2: Dealer Sells Multiple Products

```bash
# 1. Dealer registers
POST /auth/register with role=dealer

# 2. Adds multiple products
POST /api/products/add (Seeds)
POST /api/products/add (Fertilizer)
POST /api/products/add (Pesticide)

# 3. Consumer browses and reviews
GET /api/products?category=seeds
GET /api/products?min_price=100&max_price=500
POST /api/reviews
```

---

## 🐛 Common Issues & Fixes

### Issue 1: "Can't connect to MySQL server"

**Solution:**
```bash
# Check if MySQL is running:
# Windows Services → MySQL80

# Or restart MySQL:
net stop MySQL80
net start MySQL80

# Verify credentials in .env:
# DB_HOST=localhost (NOT 127.0.0.1 for some systems)
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=your_password
```

### Issue 2: "No module named 'mysql'"

**Solution:**
```bash
pip install mysql-connector-python --upgrade
```

### Issue 3: "Table doesn't exist"

**Solution:**
```bash
# Verify database and tables:
mysql -u root -p user -e "SHOW TABLES;"

# If empty, run schema:
mysql -u root -p user < schema_normalized.sql
```

### Issue 4: "Token expired" error

**Solution:**
```bash
# Login again to get fresh token
POST /auth/login

# Or extend expiry in .env:
JWT_EXPIRATION=604800  # 7 days instead of 1
```

### Issue 5: "CORS error" from frontend

**Already enabled** in app.py:
```python
CORS(app, origins=["*"], supports_credentials=True)

# But restrict in production:
CORS(app, origins=["https://yourdomain.com"], supports_credentials=True)
```

---

## 📁 Project Structure

```
c:\Abzar\Projects\Agro Link\
├── app_v2.py                    # Production backend
├── schema_normalized.sql         # Database schema
├── test_agrolink.py             # Test suite
├── .env.example                 # Config template
├── API_REFERENCE.md             # Quick API reference
├── SETUP_GUIDE_v2.md            # Detailed setup guide
├── IMPLEMENTATION_GUIDE.md      # This file
├── agrolink-login.html
├── agrolink-register.html
├── agrolink-farmer-dashboard.html
├── agrolink-dealer-dashboard.html
├── agrolink-consumer-dashboard.html
└── __pycache__/                 # Python cache (auto-created)
```

---

## 🚀 Production Deployment

### Before Going Live

1. **Change SECRET_KEY in .env**
   ```
   SECRET_KEY=generate-long-random-string-here
   ```

2. **Set FLASK_DEBUG=False**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

3. **Use strong database password**
   ```
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'very_strong_password_123!';
   ```

4. **Enable SSL for login**
   - Use HTTPS (SSL certificate)
   - Set secure cookie flags

5. **Add rate limiting**
   - Limit login attempts
   - Limit API calls per user

6. **Enable database backups**
   ```bash
   # Daily backup
   mysqldump -u root -p user > backup_$(date +%Y%m%d).sql
   ```

### Deploy to Server

```bash
# Use production server like Gunicorn:
pip install gunicorn

# Run with Gunicorn:
gunicorn -w 4 -b 0.0.0.0:5000 app_v2:app

# Or use Docker for containerization
```

---

## 📈 Performance Monitoring

### View Database Growth

```sql
-- Check database size
SELECT 
    SUM(ROUND(((data_length + index_length) / 1024 / 1024), 2)) AS size_mb
FROM INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'user';

-- Check slowest queries
SET GLOBAL log_queries_not_using_indexes=1;
SELECT * FROM mysql.slow_log;
```

### Monitor API Usage

```python
# Add to app_v2.py for request logging:
@app.before_request
def log_request():
    print(f"{datetime.now()} - {request.method} {request.path}")
```

---

## 🔄 Future Enhancements

1. **Caching Layer** - Redis for frequently accessed products
2. **Full-Text Search** - Elasticsearch for product search
3. **Recommendations** - ML-based crop/product suggestions
4. **Notifications** - Real-time order updates
5. **Payment Integration** - Razorpay/Stripe
6. **Mobile App** - React Native frontend

---

## 📞 Support & Troubleshooting

### Quick Fixes

```bash
# Restart everything:
1. Stop Flask (Ctrl+C)
2. Stop MySQL: net stop MySQL80
3. Start MySQL: net start MySQL80
4. Start Flask: python app_v2.py

# Reset database:
mysql -u root -p user < schema_normalized.sql

# Check logs:
# Flask console output shows most errors
# Check .env file is correctly configured
```

### Getting Help

1. Check `SETUP_GUIDE_v2.md` for detailed info
2. Review `API_REFERENCE.md` for endpoint details
3. Run `python test_agrolink.py` to diagnose issues
4. Check MySQL error log: `mysql -u root -p -e "SHOW ENGINE INNODB STATUS\G"`

---

## ✨ Success Indicators

You'll know the system is working when:

✅ `python test_agrolink.py` shows all green checkmarks
✅ You can register farmers, dealers, and consumers
✅ Farmers can add products
✅ Consumers can browse and review products
✅ JWT tokens work on protected endpoints
✅ Database queries complete in < 100ms

---

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MySQL Reference](https://dev.mysql.com/doc/)
- [JWT Overview](https://jwt.io/)
- [REST API Best Practices](https://restfulapi.net/)

---

**Version:** 2.0
**Last Updated:** April 3, 2026
**Status:** Production Ready ✅
