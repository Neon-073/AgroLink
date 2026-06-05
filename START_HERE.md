# 🚀 START HERE - Quick Deployment in 10 Minutes

**AgroLink v2.0** is ready to deploy. Follow these exact steps:

---

## ⚡ 10-Minute Setup

### **Step 1: Open PowerShell in Project Directory**
```powershell
cd "c:\Abzar\Projects\Agro Link"
```

### **Step 2: Activate Virtual Environment**
```powershell
venv\Scripts\activate
```

### **Step 3: Update `.env` File**
```powershell
copy .env.example .env
# Edit .env with your MySQL credentials
```

**Expected content in `.env`:**
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root        # ⚠️ Change this to your actual MySQL password
DB_NAME=user
```

### **Step 4: Initialize Database** (IMPORTANT)
```powershell
# First, ensure MySQL is running and 'user' database exists
mysql -u root -p user < schema_normalized.sql

# To verify (optional):
mysql -u root -p user -e "SHOW TABLES;"
# Should display 7 tables
```

### **Step 5: Start Backend Server**
```powershell
python app_v2.py
```

**Expected output:**
```
🌾 AgroLink Backend (v2.0) Starting...
Database: user
Host: localhost
Running on http://127.0.0.1:5000
```

### **Step 6: Test in New PowerShell Window**
```powershell
curl http://localhost:5000/test-db
```

**Expected response:**
```json
{"message": "✅ Database connection successful", "database": "user", "tables": 7}
```

---

## ✅ Verification Checklist

- [ ] MySQL running and password configured
- [ ] `.env` file created and updated with correct password
- [ ] Database `user` created and schema imported
- [ ] Backend starts without errors
- [ ] `curl http://localhost:5000/test-db` returns 7 tables
- [ ] All 14 API endpoints showing in backend startup

---

## 📱 Test an API Call

Once backend is running, test with this curl command:

```powershell
# Register a farmer
$body = @{
    username = "farmer_john"
    email = "john@farm.com"
    password = "Pass123"
    role = "farmer"
    location = "Punjab"
    farm_size = "5 acres"
} | ConvertTo-Json

curl -X POST http://localhost:5000/auth/register `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

---

## 🔧 Troubleshooting

### **Error: "Access denied for user 'root'@'localhost'"**
- [ ] Check MySQL is running: `mysql -u root -p`
- [ ] Verify password in `.env` is correct
- [ ] Change `DB_PASSWORD` in `.env` to your actual MySQL password
- [ ] Restart backend: `python app_v2.py`

### **Error: "No module named 'flask'"**
- [ ] Make sure venv is activated: `venv\Scripts\activate`
- [ ] Reinstall: `pip install -r requirements.txt`

### **Error: "Database doesn't exist"**
- [ ] Create database and import schema:
  ```powershell
  mysql -u root -p user < schema_normalized.sql
  ```

---

## 📚 Documentation Files

- **API_REFERENCE.md** - Complete API documentation with examples
- **DEPLOYMENT_CHECKLIST.md** - Full deployment guide
- **PROJECT_STATUS.md** - Status report & architecture
- **QUICKSTART.md** - 5-minute overview

---

## 🎯 Next Steps After Deployment

1. **Connect Frontend:** Update HTML files with API URL
   ```javascript
   const API_URL = 'http://localhost:5000';
   ```

2. **Test Features:**
   - Register user
   - Login & get token
   - Create product
   - Add review

3. **Run Full Tests:**
   ```powershell
   python test_agrolink.py
   ```

---

## 🌞 You're Ready!

The backend is now running at: **http://localhost:5000**

**All 14 API endpoints are functional and ready to use.**

Refer to `API_REFERENCE.md` for detailed endpoint documentation.

---

**Status:** ✅ Production Ready  
**Version:** 2.0  
**Time to Deploy:** ~10 minutes
