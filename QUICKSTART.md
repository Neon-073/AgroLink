# 🌾 AgroLink v2.0 - Quick Start Guide

## 📦 What's New

**7 New Files Created:**
1. ✅ `schema_normalized.sql` - Normalized database schema
2. ✅ `app_v2.py` - Production Flask backend  
3. ✅ `test_agrolink.py` - Automated test suite
4. ✅ `SETUP_GUIDE_v2.md` - Complete setup documentation
5. ✅ `API_REFERENCE.md` - Quick API reference
6. ✅ `IMPLEMENTATION_GUIDE.md` - Full implementation walkthrough
7. ✅ `.env.example` - Environment configuration template

---

## ⚡ 5-Minute Quick Start

### Step 1: Install Dependencies (1 min)
```bash
cd c:\Abzar\Projects\Agro Link
pip install flask mysql-connector-python flask-cors python-dotenv bcrypt pyjwt
```

### Step 2: Set Up Database (2 min)
```bash
# Open MySQL
mysql -u root -p

# Inside MySQL:
source schema_normalized.sql;  # or copy-paste file contents
SHOW TABLES;  # Should show 7 tables
EXIT;
```

### Step 3: Configure .env (1 min)
```bash
copy .env.example .env
# Edit .env with your database credentials
```

### Step 4: Start Backend (1 min)
```bash
python app_v2.py
# Should see: ✅ Database connection successful
```

### Step 5: Test It!
```bash
# In new terminal:
python test_agrolink.py
# Should see all ✅ green checkmarks
```

**Total Time:** ~5 minutes ⏱️

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| `SETUP_GUIDE_v2.md` | Installation & API reference | 20 min |
| `API_REFERENCE.md` | Quick API examples and cURL | 10 min |
| `IMPLEMENTATION_GUIDE.md` | Full deployment guide | 30 min |
| `README.md` (below) | Basic overview | 5 min |

---

## 🎯 What to Do Next

### For Development:
1. Run `python test_agrolink.py` to verify setup ✅
2. Open `API_REFERENCE.md` for endpoint examples
3. Test endpoints with Postman or cURL
4. Connect frontend dashboards to new API

### For Production:
1. Change SECRET_KEY in .env
2. Set FLASK_DEBUG=False
3. Use Gunicorn instead of Flask development server
4. Enable HTTPS/SSL
5. Set up database backups

---

## 🌐 Database Overview

### 7 Tables

```
user_details (Central)
  ├─ farmer_details (Farmer-specific)
  ├─ dealer_details (Dealer-specific)  
  └─ consumer_details (Consumer-specific)

shop (Products marketplace)
  ├─ user_products (M2M linking)
  └─ reviews (Product reviews)
```

### Foreign Keys (Referential Integrity)
- All tables link back to `user_details`
- CASCADE delete enabled (deleting user deletes related data)
- Indexes on frequently queried columns

---

## 🔌 API Endpoints Summary

### Authentication (No token needed)
```
POST /auth/register     - Register new user
POST /auth/login        - Login & get token
```

### Users (No token needed)
```
GET /api/user/<id>              - Get basic user info
GET /api/user/<id>/profile      - Get full profile with role details
PUT /api/user/<id>              - Update profile (needs token)
```

### Products
```
GET /api/products               - List all products (filterable)
GET /api/products/<id>          - Get product with reviews
POST /api/products/add          - Add product (needs token)
PUT /api/products/<id>          - Update product (needs token)
DELETE /api/products/<id>       - Delete product (needs token)
```

### Reviews
```
GET /api/reviews/<product_id>   - Get reviews for product
POST /api/reviews               - Add review (needs token)
```

### Testing
```
GET /                  - API info
GET /test-db           - Database test
```

---

## 🔐 JWT Authentication

### Getting a Token
```bash
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}

Response: {"token": "eyJhbGciOiJIUzI1NiIs..."}
```

### Using Token on Protected Endpoints
```bash
GET /api/user/1/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Token Expiry
- Default: 24 hours
- Configurable in `.env` (JWT_EXPIRATION)
- Login again to get new token

---

## 🧪 Test Examples

### Register a Farmer
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "rajesh_farmer",
    "email": "rajesh@farm.com",
    "phone_number": "+91 9876543210",
    "password": "pass123",
    "role": "farmer",
    "farm_size": 25.5,
    "soil_type": "loamy",
    "crops_selected": ["wheat", "rice"]
  }'
```

### Add a Product (with token)
```bash
curl -X POST http://localhost:5000/api/products/add \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Hybrid Wheat Seeds",
    "product_price": 350,
    "product_description": "High-yield seeds",
    "category": "seeds",
    "stock_quantity": 100
  }'
```

### Browse Products
```bash
# Get all products
curl http://localhost:5000/api/products

# Filter by category
curl "http://localhost:5000/api/products?category=seeds"

# Price range filter
curl "http://localhost:5000/api/products?min_price=100&max_price=500"
```

---

## ✅ Verification Checklist

After setup, verify these work:

- [ ] `GET /` returns API info
- [ ] `GET /test-db` shows database stats
- [ ] `POST /auth/register` creates user with JWT
- [ ] `POST /auth/login` returns token
- [ ] `POST /api/products/add` needs valid token
- [ ] `GET /api/products` returns product list
- [ ] All 11 tests in `test_agrolink.py` pass ✅

---

## 🆘 Troubleshooting

### Database won't connect
```bash
# Check MySQL is running:
net start MySQL80

# Verify credentials in .env match your setup
```

### "Table doesn't exist"
```bash
mysql -u root -p user -e "SHOW TABLES;"

# If empty, run schema:
mysql -u root -p user < schema_normalized.sql
```

### "Token required" error
```bash
# Make sure to:
1. Login first to get token
2. Include Authorization header
3. Use exact format: "Bearer <token>"
```

### Port 5000 already in use
```bash
# Change port in app_v2.py line 360:
app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

---

## 📊 Database Statistics

After testing, you should see something like:

```json
{
  "success": true,
  "database": "user",
  "tables": 7,
  "statistics": {
    "total_users": 3,
    "total_products": 2
  }
}
```

---

## 🎓 Understanding the Architecture

### User Roles

**Farmer:**
- Register with farm details
- Add crops as products
- Review dealer products
- View other products

**Dealer:**
- Register with shop details  
- Add products for sale
- Review farmer products
- Browse all products

**Consumer:**
- Register with location
- Browse all products
- Add reviews
- Cannot sell products

### Data Flow

```
1. User registers → Stored in user_details + role-specific table
2. Farmer adds crop → Stored in shop as product
3. Dealer adds fertilizer → Stored in shop as product
4. Consumer reviews → Stored in reviews table
5. Average rating calculated from reviews
```

---

## 🚀 Next Steps

1. **Read Documentation**
   - Start with `SETUP_GUIDE_v2.md` (30 min detailed guide)
   - Quick reference: `API_REFERENCE.md`

2. **Test the System**
   - Run: `python test_agrolink.py`
   - All tests should pass ✅

3. **Integrate Frontend**
   - Update dashboard HTML files
   - Point API calls to new endpoints
   - Handle JWT tokens in localStorage

4. **Customize for Your Needs**
   - Add more fields to tables
   - Extend API with business logic
   - Add admin dashboard

5. **Deploy**
   - See `IMPLEMENTATION_GUIDE.md` for production setup
   - Use Gunicorn for production
   - Enable HTTPS/SSL

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Install packages | `pip install -r requirements.txt` |
| Start backend | `python app_v2.py` |
| Run tests | `python test_agrolink.py` |
| View docs | See files in project directory |
| Database backup | `mysqldump -u root -p user > backup.sql` |
| Test endpoint | `curl http://localhost:5000/test-db` |

---

## 💡 Tips

✨ **Pro Tips:**

1. **Save tokens** - Store JWT after login for API calls
2. **Use Postman** - Easier than cURL for testing
3. **Check .env** - Most errors are config-related
4. **Monitor MySQL** - Use `SHOW PROCESSLIST;` to debug slow queries
5. **Version control** - Keep `schema_v2.0.sql` and `app_v2.py` backed up

---

## 📈 Performance

Expected performance on localhost:
- Register: < 100ms
- Login: < 100ms
- Add product: < 150ms
- Get products: < 50ms
- Add review: < 100ms

---

## 🎯 Success!

When you see this, you're ready:

```
✅ Database Connection: user (7 tables)
✅ API Health: Running on port 5000
✅ Auth: JWT tokens working
✅ Products: CRUD operations functional
✅ Reviews: Rating system active
✅ All tests: PASSED
```

---

**Version:** 2.0.0
**Database:** user (Normalized)
**Framework:** Flask + MySQL
**Status:** ✅ Production Ready

🌾 **Happy farming with AgroLink!** 🌾
