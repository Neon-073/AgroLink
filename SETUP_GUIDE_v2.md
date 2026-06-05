# 🌾 AgroLink - Normalized Database Architecture (v2.0)

## Overview

AgroLink is a scalable agricultural marketplace platform built with:
- **Backend**: Flask + MySQL
- **Database**: Fully normalized with 7 optimized tables
- **Authentication**: JWT tokens with role-based access
- **Architecture**: 3 user roles (Farmer, Dealer, Consumer) with dedicated profile tables

---

## 📋 Table of Contents

1. [Database Design](#database-design)
2. [Installation & Setup](#installation--setup)
3. [API Endpoints](#api-endpoints)
4. [Database Schema](#database-schema)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)

---

## Database Design

### Architecture Highlights

✅ **Proper Normalization** - Each role has dedicated tables avoiding NULL columns
✅ **Foreign Key Relationships** - Enforced referential integrity with CASCADE delete
✅ **JSON for Flexibility** - Used only for arrays (crops_selected, deals_for, gardening_plants)
✅ **Indexed Queries** - Performance optimized with strategic indexes
✅ **Scalable Structure** - Ready for millions of products and users

### Tables Overview

```
user_details (center)
    ├─ farmer_details
    ├─ dealer_details
    └─ consumer_details

shop (products)
    ├─ user_products (M2M relationship)
    └─ reviews
```

---

## Installation & Setup

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd c:\Abzar\Projects\Agro Link

# Install Python packages
pip install flask mysql-connector-python flask-cors python-dotenv bcrypt pyjwt

# Verify installation
python -c "import flask, mysql, jwt; print('✅ All packages installed')"
```

### Step 2: Set Up MySQL Database

```bash
# Open MySQL command line
mysql -u root -p

# Run the schema script (from MySQL prompt)
source schema_normalized.sql;

# Verify database creation
USE user;
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
# Copy the example file
copy .env.example .env

# Edit .env with your database credentials
notepad .env
```

**Required settings:**
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=user
```

### Step 4: Run the Backend

```bash
# Start Flask server
python app_v2.py

# Expected output:
# ╔════════════════════════════════════════════════════════════════╗
# ║         🌾 AgroLink Backend (v2.0) Starting...               ║
# ║         Database: user                                        ║
# ║         Host: localhost                                       ║
# ╚════════════════════════════════════════════════════════════════╝
# ✅ Database connection successful
# 🚀 API Routes: [list of endpoints]
```

### Step 5: Test Connection

```bash
# Open browser and visit:
http://localhost:5000

# Expected response:
# {
#   "success": true,
#   "message": "🌾 AgroLink Backend v2.0",
#   "database": "user",
#   "endpoints": { ... }
# }
```

---

## API Endpoints

### 🔐 Authentication Endpoints

#### Register New User

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "username": "rajesh_farmer",
  "email": "rajesh@example.com",
  "phone_number": "+91 9876543210",
  "password": "secure_password",
  "role": "farmer",
  "location": "Punjab",
  "crops_selected": ["wheat", "rice"],
  "farm_location": "Village XYZ",
  "soil_type": "loamy",
  "irrigation_type": "drip",
  "farm_size": 25.5
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Registration successful",
  "user_id": 1,
  "role": "farmer",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Login User

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "rajesh@example.com",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "user_id": 1,
  "username": "rajesh_farmer",
  "role": "farmer",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 👤 User Endpoints

#### Get User by ID

**Endpoint:** `GET /api/user/<user_id>`

**Example:** `GET /api/user/1`

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "username": "rajesh_farmer",
    "email": "rajesh@example.com",
    "phone_number": "+91 9876543210",
    "location": "Punjab",
    "role": "farmer",
    "profile_photo": "https://...",
    "created_at": "2026-04-03 10:30:00"
  }
}
```

#### Get Complete User Profile

**Endpoint:** `GET /api/user/<user_id>/profile`

**Response (200 OK):**
```json
{
  "success": true,
  "profile": {
    "user_id": 1,
    "username": "rajesh_farmer",
    "email": "rajesh@example.com",
    "role": "farmer",
    "farm_details": {
      "user_id": 1,
      "crops_selected": ["wheat", "rice"],
      "farm_location": "Village XYZ",
      "soil_type": "loamy",
      "irrigation_type": "drip",
      "farm_size": 25.5
    }
  }
}
```

#### Update User Profile

**Endpoint:** `PUT /api/user/<user_id>` (Requires JWT Token)

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body:**
```json
{
  "location": "Haryana",
  "profile_photo": "https://..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "User updated"
}
```

---

### 📦 Product Endpoints

#### Get All Products

**Endpoint:** `GET /api/products`

**Query Parameters:**
```
GET /api/products?category=seeds&min_price=100&max_price=500&owner_id=1
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "products": [
    {
      "product_id": 1,
      "product_name": "Hybrid Wheat Seeds",
      "product_price": 350.00,
      "product_description": "High-yield hybrid wheat seeds...",
      "product_owner_id": 1,
      "owner_role": "farmer",
      "product_photo": "https://...",
      "category": "seeds",
      "stock_quantity": 100,
      "created_at": "2026-04-03 10:00:00"
    }
  ]
}
```

#### Get Product Details with Reviews

**Endpoint:** `GET /api/products/<product_id>`

**Example:** `GET /api/products/1`

**Response (200 OK):**
```json
{
  "success": true,
  "product": {
    "product_id": 1,
    "product_name": "Hybrid Wheat Seeds",
    "product_price": 350.00,
    "product_description": "High-yield hybrid wheat seeds",
    "product_owner_id": 1,
    "average_rating": 4.5,
    "review_count": 6,
    "reviews": [
      {
        "review_id": 1,
        "username": "farmer_john",
        "rating": 5,
        "comment": "Excellent seeds, great yield!",
        "photos": ["https://..."],
        "created_at": "2026-04-02 15:30:00"
      }
    ]
  }
}
```

#### Add Product

**Endpoint:** `POST /api/products/add` (Requires JWT Token)

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body:**
```json
{
  "product_name": "Hybrid Wheat Seeds",
  "product_price": 350.00,
  "product_description": "High-yield hybrid wheat seeds suitable for North India",
  "product_photo": "https://...",
  "category": "seeds",
  "stock_quantity": 100
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Product added successfully",
  "product_id": 1
}
```

#### Update Product

**Endpoint:** `PUT /api/products/<product_id>` (Requires JWT Token)

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body:**
```json
{
  "product_name": "Premium Hybrid Wheat Seeds",
  "product_price": 400.00,
  "product_description": "Updated description...",
  "stock_quantity": 80
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Product updated"
}
```

#### Delete Product

**Endpoint:** `DELETE /api/products/<product_id>` (Requires JWT Token)

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Product deleted"
}
```

---

### ⭐ Review Endpoints

#### Get Reviews for Product

**Endpoint:** `GET /api/reviews/<product_id>`

**Example:** `GET /api/reviews/1`

**Response (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "reviews": [
    {
      "review_id": 1,
      "username": "farmer_john",
      "rating": 5,
      "comment": "Excellent product!",
      "photos": ["https://..."],
      "created_at": "2026-04-02 15:30:00",
      "profile_photo": "https://..."
    }
  ]
}
```

#### Add Review

**Endpoint:** `POST /api/reviews` (Requires JWT Token)

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body:**
```json
{
  "product_id": 1,
  "rating": 5,
  "comment": "Excellent seeds, high germination rate!",
  "photos": ["https://image1.jpg", "https://image2.jpg"]
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Review added successfully",
  "review_id": 1
}
```

---

## Database Schema

### Table Relationships

```sql
-- One-to-One (farmer_details, dealer_details, consumer_details)
user_details (PK: user_id)
    ├─ farmer_details (FK: user_id) → One farmer per user
    ├─ dealer_details (FK: user_id) → One dealer per user
    └─ consumer_details (FK: user_id) → One consumer per user

-- One-to-Many (shop to user)
user_details (PK: user_id)
    └─ shop (FK: product_owner_id) → Multiple products per user

-- Many-to-Many (user_products)
user_details (PK: user_id) ←→ shop (PK: product_id)
    └─ user_products (FK: user_id, product_id)

-- Many-to-Many (reviews)
user_details (PK: user_id) ←→ shop (PK: product_id)
    └─ reviews (FK: user_id, product_id)
```

### Field Descriptions

**user_details:**
- `user_id` (INT) - Auto-incremented primary key
- `username` (VARCHAR) - Unique username for login
- `email` (VARCHAR) - Unique email address
- `phone_number` (VARCHAR) - Mobile number
- `password` (VARCHAR) - bcrypt hashed password
- `role` (ENUM) - 'farmer', 'dealer', or 'consumer'
- `location` (VARCHAR) - User location/address
- `profile_photo` (TEXT) - URL to profile picture

**farmer_details:**
- `crops_selected` (JSON) - ["wheat", "rice", "corn"]
- `farm_location` (VARCHAR) - Specific farm coordinates
- `soil_type` (VARCHAR) - loamy, sandy, clay, etc.
- `irrigation_type` (VARCHAR) - drip, flood, sprinkler
- `farm_size` (FLOAT) - Farm size in acres

**dealer_details:**
- `deals_for` (JSON) - ["seeds", "fertilizer", "pesticide"]
- `shop_photo` (TEXT) - Shop storefront image
- `gst_in` (VARCHAR) - GST Identification Number

**consumer_details:**
- `gardening_plants` (JSON) - ["tomato", "basil", "carrot"]

**shop:**
- `product_id` (INT) - Auto-incremented
- `product_name` (VARCHAR) - Name of product
- `product_price` (FLOAT) - Price in ₹
- `product_description` (TEXT) - Full description
- `product_owner_id` (INT) - FK to user_details
- `owner_role` (ENUM) - 'farmer' or 'dealer'
- `product_photo` (TEXT) - Product image URL
- `category` (VARCHAR) - seeds, fertilizer, pesticide, etc.
- `stock_quantity` (INT) - Available stock

---

## Examples

### Example 1: Farmer Registration & Add Product

```bash
# 1. Register as Farmer
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "rajesh_farmer",
    "email": "rajesh@agro.com",
    "phone_number": "+91 9876543210",
    "password": "pass123",
    "role": "farmer",
    "location": "Punjab",
    "farm_size": 25.5,
    "soil_type": "loamy",
    "crops_selected": ["wheat", "rice"]
  }'

# Response: { "user_id": 1, "token": "..." }

# 2. Add Wheat Seeds Product (using token)
curl -X POST http://localhost:5000/api/products/add \
  -H "Authorization: Bearer <token_from_step_1>" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Hybrid Wheat Seeds",
    "product_price": 350,
    "product_description": "High-yield seeds",
    "category": "seeds",
    "stock_quantity": 100
  }'

# Response: { "product_id": 1 }

# 3. Add Review (as different user)
curl -X POST http://localhost:5000/api/reviews \
  -H "Authorization: Bearer <consumer_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "rating": 5,
    "comment": "Great quality seeds!"
  }'
```

### Example 2: Dealer Registration & Browse Products

```bash
# 1. Register as Dealer
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sharma_dealer",
    "email": "sharma@agro.com",
    "phone_number": "+91 8765432109",
    "password": "pass123",
    "role": "dealer",
    "location": "Pune",
    "gst_in": "27ABCDE1234F1Z5",
    "deals_for": ["seeds", "fertilizer", "pesticide"]
  }'

# 2. Browse all seed products
curl "http://localhost:5000/api/products?category=seeds"

# 3. Get product with reviews
curl "http://localhost:5000/api/products/1"
```

---

## Troubleshooting

### Issue: "Database connection failed"

**Solution:**
```bash
# Check MySQL is running
# Windows:
net start MySQL80

# Check credentials in .env
echo %DB_PASSWORD%

# Test connection directly
mysql -h localhost -u root -p user -e "SELECT 1;"
```

### Issue: "Table already exists error"

**Solution:**
```bash
# Delete the old database completely
mysql -u root -p -e "DROP DATABASE IF EXISTS user;"

# Run schema_normalized.sql again
```

### Issue: "Token expired"

**Solution:**
- Tokens expire after 24 hours by default
- Get a new token by logging in again
- Change JWT_EXPIRATION in .env to adjust expiry time

### Issue: "Unauthorized" on PUT/DELETE endpoints

**Solution:**
```bash
# Make sure to include Authorization header:
-H "Authorization: Bearer YOUR_TOKEN_HERE"

# Token should be from the login response
```

---

## Performance Optimization Tips

1. **Indexes** - Key columns are indexed for fast queries
2. **JSON Fields** - Only used when flexibility is needed
3. **Pagination** - Add `LIMIT` to product queries for large datasets
4. **Caching** - Consider Redis for frequently accessed products
5. **Search** - FULLTEXT indexes on product_name and description

---

## Next Steps

1. ✅ Database created and tested
2. ✅ Backend API running with JWT authentication
3. 🔄 Connect frontend dashboards to new API endpoints
4. 🔄 Migrate existing user data if needed
5. 🔄 Deploy to production server

---

## Support

For issues or questions:
- Check the error message returned by API
- Review `.env` configuration
- Verify database connection with `/test-db` endpoint
- Check browser console for frontend errors

---

**Version:** 2.0
**Last Updated:** April 3, 2026
**Status:** Production Ready ✅
