# 🚀 AgroLink Deployment Checklist

**Project:** AgroLink v2.0 - Agricultural Marketplace  
**Database:** MySQL (Normalized Schema - 7 Tables)  
**Backend:** Flask + Python  
**Status:** Ready to Deploy

---

## ✅ Pre-Deployment Verification

### 1. **File Structure**
- [x] `schema_normalized.sql` - Database schema
- [x] `app_v2.py` - Flask backend
- [x] `test_agrolink.py` - Test suite
- [x] `requirements.txt` - Python dependencies
- [x] `.env.example` - Configuration template
- [x] `API_REFERENCE.md` - API documentation
- [x] Dashboard HTML files:
  - `agrolink-farmer-dashboard.html`
  - `agrolink-dealer-dashboard.html`
  - `agrolink-consumer-dashboard.html`
  - `agrolink-login.html`
  - `agrolink-register.html`

### 2. **Dependencies Installed**
```bash
# Python packages required
- flask>=3.0.0
- flask-cors>=4.0.0
- mysql-connector-python>=9.0.0
- bcrypt>=4.1.2
- PyJWT>=2.8.0
- python-dotenv>=1.0.0
```

### 3. **Database Schema** (7 Tables)
- [x] `user_details` - Authentication & basic info
- [x] `farmer_details` - Farmer-specific data
- [x] `dealer_details` - Dealer-specific data
- [x] `consumer_details` - Consumer-specific data
- [x] `shop` - Products marketplace
- [x] `user_products` - Many-to-many relationships
- [x] `reviews` - Product reviews & ratings

### 4. **API Endpoints** (14 Total)
**Health & Testing (2):**
- [x] `GET /` - API info
- [x] `GET /test-db` - Database test

**Authentication (2):**
- [x] `POST /auth/register` - Register user (all roles)
- [x] `POST /auth/login` - Login & get JWT token

**User Management (3):**
- [x] `GET /api/user/<id>` - Get basic info
- [x] `GET /api/user/<id>/profile` - Get full profile
- [x] `PUT /api/user/<id>` - Update profile

**Products (5):**
- [x] `GET /api/products` - List products (with filters)
- [x] `GET /api/products/<id>` - Get product details
- [x] `POST /api/products/add` - Add product
- [x] `PUT /api/products/<id>` - Update product
- [x] `DELETE /api/products/<id>` - Delete product

**Reviews (2):**
- [x] `GET /api/reviews/<product_id>` - Get reviews
- [x] `POST /api/reviews` - Add review

---

## 📋 Step-by-Step Deployment

### **Step 1: Environment Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Configure Database**
```bash
# Ensure MySQL is running
# Copy .env.example to .env
copy .env.example .env

# Edit .env with your credentials:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=user
```

### **Step 3: Initialize Database**
```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE user;
USE user;

# Run schema script
source schema_normalized.sql

# Verify tables
SHOW TABLES;
# Should show 7 tables
```

Or using command line:
```bash
mysql -u root -p user < schema_normalized.sql
```

### **Step 4: Test Backend Connection**
```bash
# Run the backend
python app_v2.py

# Test in another terminal
curl http://localhost:5000/test-db
```

### **Step 5: Run Test Suite**
```bash
# Unit tests
python test_agrolink.py

# Should show 11 test cases passing
```

---

## 🔧 Troubleshooting

### **Error: Database connection error 1045 (Access denied)**

**Solution:**
1. Verify MySQL is running:
   ```bash
   mysql -u root -p
   ```

2. Check `.env` credentials match MySQL setup:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_actual_password
   DB_NAME=user
   ```

3. Restart Flask app:
   ```bash
   python app_v2.py
   ```

### **Error: Database doesn't exist**

**Solution:**
```bash
# Create database
mysql -u root -p user < schema_normalized.sql

# Or manually:
mysql -u root -p
CREATE DATABASE user;
USE user;
source schema_normalized.sql;
```

### **Error: Module not found (flask, mysql-connector, etc.)**

**Solution:**
```bash
# Ensure venv is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

### **Error: CORS issues (frontend can't access API)**

**Solution:**
- CORS is already enabled in `app_v2.py`
- Add to frontend requests:
  ```javascript
  // Make sure to include credentials if using tokens
  fetch('http://localhost:5000/api/products', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_TOKEN'
    }
  })
  ```

### **Error: Token invalid or expired**

**Solution:**
- Tokens expire after 24 hours
- Login again to get new token:
  ```bash
  POST /auth/login
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

---

## 🚀 Production Deployment

### **Using Gunicorn (Production WSGI Server)**

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app_v2:app
   ```

3. Configure with Nginx (reverse proxy):
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### **Using Docker (Optional)**

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.10
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "app_v2.py"]
   ```

2. Build and run:
   ```bash
   docker build -t agrolink .
   docker run -p 5000:5000 --env-file .env agrolink
   ```

---

## 📊 Performance Monitoring

### **Database Optimization**
- Indexes created on `user_id`, `product_id`
- Foreign key relationships for data integrity
- Parameterized queries prevent SQL injection

### **API Performance**
- JWT tokens reduce database hits for auth
- CORS enabled for frontend optimization
- Error handling prevents crashes

### **Testing**
Run full test suite: `python test_agrolink.py`

---

## ✨ Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Database Schema | ✅ Ready | 7 tables, normalized |
| Backend API | ✅ Ready | 14 endpoints working |
| Authentication | ✅ Ready | JWT + bcrypt hashing |
| Dashboards | ✅ Ready | 5 HTML files created |
| Documentation | ✅ Ready | API Reference + Guides |
| Testing | ✅ Ready | 11 test cases |

---

## 📝 Next Steps for Production

1. **Update `.env` with production values:**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=generate-unique-secret-key
   ```

2. **Set up SSL/HTTPS** for production

3. **Configure database backups:**
   ```bash
   mysqldump -u root -p user > backup.sql
   ```

4. **Monitor API logs** for errors

5. **Set up automated testing** in CI/CD pipeline

---

**Last Updated:** April 3, 2026  
**Version:** 2.0  
**Ready for:** Development & Production Deployment
