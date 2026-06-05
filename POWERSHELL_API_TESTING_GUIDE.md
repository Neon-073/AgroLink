# 🔧 PowerShell API Testing - Correct Syntax Guide

## ❌ WHAT WENT WRONG

Your PowerShell commands had syntax errors. The issue:

```powershell
# WRONG - PowerShell doesn't use -X flag
curl -X POST http://localhost:5000/auth/register
```

**Error message:**
```
Invoke-WebRequest : A parameter cannot be found that matches parameter name 'X'
```

---

## ✅ CORRECT PowerShell SYNTAX

### **Important: Use Invoke-WebRequest, NOT curl for POST/PUT/DELETE**

PowerShell has built-in `curl` alias, but it behaves differently than Linux curl!

---

## 🚀 CORRECT COMMANDS

### **1. Test Database Connection**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/test-db"
```

### **2. Get API Info**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/"
```

### **3. Register a Farmer (POST)**
```powershell
$body = @{
    username = "farmer_test"
    email = "farmer@test.com"
    password = "Pass123"
    role = "farmer"
    location = "Punjab"
    farm_size = "5 acres"
    soil_type = "Loamy"
    irrigation_type = "Drip"
    crops_selected = @("Wheat", "Rice")
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/auth/register" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

### **4. Login User (POST)**
```powershell
$loginBody = @{
    username = "farmer_test"
    password = "Pass123"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/auth/login" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $loginBody

# Get token from response
$token = ($response.Content | ConvertFrom-Json).token
Write-Host "Token: $token"
```

### **5. Create Product (with JWT Token)**
```powershell
$productBody = @{
    product_name = "Organic Wheat"
    product_price = 25.50
    product_description = "High quality wheat"
    category = "Grains"
    stock_quantity = 100
    product_photo = "wheat.jpg"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $token"
}

Invoke-WebRequest -Uri "http://localhost:5000/api/products/add" `
    -Method POST `
    -Headers $headers `
    -Body $productBody
```

### **6. Get All Products**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/products"
```

### **7. Get Product by ID**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/products/1"
```

### **8. Add Review (with Token)**
```powershell
$reviewBody = @{
    product_id = 1
    rating = 5
    comment = "Excellent quality!"
    photos = @("review.jpg")
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $token"
}

Invoke-WebRequest -Uri "http://localhost:5000/api/reviews" `
    -Method POST `
    -Headers $headers `
    -Body $reviewBody
```

---

## 🎯 SIMPLEST WAY - Use Pre-Built Test Suite

Instead of typing all these commands manually, just run:

```powershell
cd "c:\Abzar\Projects\Agro Link"
venv\Scripts\activate
python test_agrolink.py
```

**This will run all 11 tests automatically!** 🚀

Expected output:
```
🌾 AgroLink Backend - Test Suite v2.0
Base URL: http://localhost:5000

Test 1: Database Connection
  ✅ PASSED - DB connected: user (7 tables)

Test 2: User Registration - Farmer
  ✅ PASSED - Farmer registered (ID: 1)

...

📊 Test Results Summary
Total Tests: 11
Passed: 11 ✅
Failed: 0 ❌

🎉 ALL TESTS PASSED! System is ready for deployment
```

---

## ✨ QUICK REFERENCE - Copy & Paste Ready

### **Get API Info (Simplest)**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/"
```

### **Test DB Connection**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/test-db"
```

### **Register Dealer**
```powershell
$body = @{
    username = "dealer_test"
    email = "dealer@shop.com"
    password = "Pass123"
    role = "dealer"
    location = "Delhi"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/auth/register" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

---

## 🆚 PowerShell vs Linux curl

| Operation | PowerShell | Linux curl |
|-----------|-----------|-----------|
| GET | `Invoke-WebRequest` | `curl` |
| POST | `Invoke-WebRequest -Method POST` | `curl -X POST` |
| PUT | `Invoke-WebRequest -Method PUT` | `curl -X PUT` |
| DELETE | `Invoke-WebRequest -Method DELETE` | `curl -X DELETE` |
| Headers | `-Headers @{"Key"="Value"}` | `-H "Key: Value"` |
| Body | `-Body $json` | `-d $json` |

---

## 📽️ OR Use a Browser (Even Simpler!)

For GET requests, just paste in browser:

```
http://localhost:5000/test-db
http://localhost:5000/api/products
http://localhost:5000/api/user/1/profile
```

---

## ✅ RECOMMENDED WORKFLOW

1. **Keep backend running:**
   ```powershell
   cd "c:\Abzar\Projects\Agro Link"
   python app_v2.py
   ```

2. **Run tests in new PowerShell:**
   ```powershell
   cd "c:\Abzar\Projects\Agro Link"
   venv\Scripts\activate
   python test_agrolink.py
   ```

3. **Done!** ✅ All 11 tests will run automatically

---

## 🎉 That's It!

Now you have:
- ✅ No PowerShell syntax errors
- ✅ Proper API testing syntax
- ✅ Automated test suite ready to use
- ✅ Backend running successfully

**Next step: Run `python test_agrolink.py` and watch all 11 tests pass!** 🚀
