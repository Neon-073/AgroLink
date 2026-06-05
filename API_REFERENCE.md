# 🌾 AgroLink API Reference

**Version:** 2.0  
**Base URL:** `http://localhost:5000`  
**Documentation:** Complete endpoint reference for AgroLink Backend API

---

## 📌 Quick Navigation

- [Health & Testing](#health--testing)
- [Authentication](#authentication)
- [User Management](#user-management)
- [Products](#products)
- [Reviews](#reviews)
- [Common Patterns](#common-patterns)

---

## Health & Testing

### GET `/`
**Description:** Get API info and available endpoints  
**Auth Required:** No  
**Response:**
```json
{
  "message": "AgroLink Backend v2.0 API",
  "database": "user",
  "endpoints": 14,
  "status": "running"
}
```

### GET `/test-db`
**Description:** Test database connectivity  
**Auth Required:** No  
**Response:**
```json
{
  "message": "✅ Database connection successful",
  "database": "user",
  "tables": 7
}
```

---

## Authentication

### POST `/auth/register`
**Description:** Register a new user (all roles)  
**Auth Required:** No  
**Request Body:**
```json
{
  "username": "farmer_john",
  "email": "john@farm.com",
  "password": "SecurePass123",
  "phone": "9876543210",
  "role": "farmer",
  "location": "Punjab",
  "farm_size": "5 acres",
  "soil_type": "Loamy",
  "irrigation_type": "Drip",
  "crops_selected": ["Wheat", "Rice"]
}
```
**Response:**
```json
{
  "success": true,
  "user_id": 1,
  "role": "farmer"
}
```
**Roles:** `farmer`, `dealer`, `consumer`

### POST `/auth/login`
**Description:** User login - returns JWT token  
**Auth Required:** No  
**Request Body:**
```json
{
  "username": "farmer_john",
  "password": "SecurePass123"
}
```
**Response:**
```json
{
  "success": true,
  "user_id": 1,
  "role": "farmer",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login successful"
}
```
**Token Expiry:** 24 hours  
**Usage:** Add to Authorization header: `Authorization: Bearer <token>`

---

## User Management

### GET `/api/user/<id>`
**Description:** Get basic user info  
**Auth Required:** No  
**Parameters:**
- `id` (int, path): User ID

**Response:**
```json
{
  "user_id": 1,
  "username": "farmer_john",
  "email": "john@farm.com",
  "phone": "9876543210",
  "role": "farmer",
  "location": "Punjab"
}
```

### GET `/api/user/<id>/profile`
**Description:** Get full profile with role-specific details  
**Auth Required:** No  
**Parameters:**
- `id` (int, path): User ID

**Response (Farmer):**
```json
{
  "user_id": 1,
  "username": "farmer_john",
  "email": "john@farm.com",
  "role": "farmer",
  "farm_details": {
    "farm_location": "Punjab",
    "soil_type": "Loamy",
    "irrigation_type": "Drip",
    "farm_size": "5 acres",
    "crops_selected": ["Wheat", "Rice"]
  }
}
```

### PUT `/api/user/<id>`
**Description:** Update user profile  
**Auth Required:** Yes (Token)  
**Parameters:**
- `id` (int, path): User ID

**Request Body:**
```json
{
  "email": "newemail@farm.com",
  "phone": "9876543211",
  "location": "Haryana"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Profile updated successfully"
}
```

---

## Products

### GET `/api/products`
**Description:** List all products with filters  
**Auth Required:** No  
**Query Parameters:**
- `category` (string): Filter by category (e.g., `category=Vegetables`)
- `owner_role` (string): Filter by owner role (`farmer`, `dealer`)
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter
- `search` (string): Search by product name

**Example:** `GET /api/products?category=Vegetables&min_price=10&max_price=100`

**Response:**
```json
[
  {
    "product_id": 1,
    "product_name": "Organic Wheat",
    "product_price": 25.50,
    "product_description": "High-quality wheat",
    "category": "Grains",
    "owner_role": "farmer",
    "stock_quantity": 100,
    "product_owner_id": 1,
    "rating": 4.5
  }
]
```

### GET `/api/products/<id>`
**Description:** Get product details with reviews  
**Auth Required:** No  
**Parameters:**
- `id` (int, path): Product ID

**Response:**
```json
{
  "product_id": 1,
  "product_name": "Organic Wheat",
  "product_price": 25.50,
  "product_description": "High-quality wheat",
  "category": "Grains",
  "stock_quantity": 100,
  "product_owner_id": 1,
  "owner_role": "farmer",
  "reviews": [
    {
      "review_id": 1,
      "rating": 5,
      "comment": "Excellent quality",
      "user_id": 2
    }
  ]
}
```

### POST `/api/products/add`
**Description:** Add new product (requires token)  
**Auth Required:** Yes (Token)  
**Request Body:**
```json
{
  "product_name": "Fresh Tomatoes",
  "product_price": 15.99,
  "product_description": "Farm-fresh red tomatoes",
  "category": "Vegetables",
  "stock_quantity": 50,
  "product_photo": "https://example.com/tomato.jpg"
}
```
**Response:**
```json
{
  "success": true,
  "product_id": 5,
  "message": "Product added successfully"
}
```

### PUT `/api/products/<id>`
**Description:** Update product details  
**Auth Required:** Yes (Token)  
**Parameters:**
- `id` (int, path): Product ID

**Request Body:**
```json
{
  "product_price": 18.99,
  "stock_quantity": 75,
  "product_description": "Updated description"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Product updated successfully"
}
```

### DELETE `/api/products/<id>`
**Description:** Delete product  
**Auth Required:** Yes (Token)  
**Parameters:**
- `id` (int, path): Product ID

**Response:**
```json
{
  "success": true,
  "message": "Product deleted successfully"
}
```

---

## Reviews

### GET `/api/reviews/<product_id>`
**Description:** Get all reviews for a product  
**Auth Required:** No  
**Parameters:**
- `product_id` (int, path): Product ID

**Response:**
```json
[
  {
    "review_id": 1,
    "product_id": 1,
    "user_id": 2,
    "rating": 5,
    "comment": "Excellent quality",
    "photos": ["http://example.com/review-photo1.jpg"]
  },
  {
    "review_id": 2,
    "product_id": 1,
    "user_id": 3,
    "rating": 4,
    "comment": "Good, but delivery was slow"
  }
]
```

### POST `/api/reviews`
**Description:** Add review for a product  
**Auth Required:** Yes (Token)  
**Request Body:**
```json
{
  "product_id": 1,
  "rating": 5,
  "comment": "Excellent quality and fresh",
  "photos": ["http://example.com/review1.jpg"]
}
```
**Response:**
```json
{
  "success": true,
  "review_id": 5,
  "message": "Review added successfully"
}
```
**Rating Range:** 1-5 stars

---

## Common Patterns

### Authentication Flow

**1. Register:**
```bash
POST /auth/register
{
  "username": "john",
  "password": "pass123",
  "role": "farmer"
}
```

**2. Login & Get Token:**
```bash
POST /auth/login
{
  "username": "john",
  "password": "pass123"
}
```
Response: `{"token": "eyJ..."}`

**3. Use Token in Requests:**
```bash
GET /api/user/1
Authorization: Bearer eyJ...
```

### Error Responses

**400 - Bad Request:**
```json
{
  "error": "Missing required field: email"
}
```

**401 - Unauthorized:**
```json
{
  "error": "Invalid or missing token"
}
```

**404 - Not Found:**
```json
{
  "error": "Product not found"
}
```

**500 - Server Error:**
```json
{
  "error": "Database error occurred"
}
```

### Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing/invalid token)
- `404` - Not Found
- `500` - Server Error

---

## CURL Examples

### Register Farmer:
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer_john",
    "email": "john@farm.com",
    "password": "Pass123",
    "role": "farmer",
    "location": "Punjab",
    "farm_size": "5 acres"
  }'
```

### Login:
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer_john",
    "password": "Pass123"
  }'
```

### Get Products:
```bash
curl -X GET "http://localhost:5000/api/products?category=Vegetables" \
  -H "Content-Type: application/json"
```

### Add Product (with token):
```bash
curl -X POST http://localhost:5000/api/products/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "product_name": "Fresh Tomatoes",
    "product_price": 15.99,
    "category": "Vegetables",
    "stock_quantity": 50
  }'
```

---

## Database Schema Reference

**7 Tables:**
1. `user_details` - User authentication & basic info
2. `farmer_details` - Farmer-specific data
3. `dealer_details` - Dealer-specific data
4. `consumer_details` - Consumer-specific data
5. `shop` - Products marketplace
6. `user_products` - Many-to-many product allocation
7. `reviews` - Product reviews & ratings

---

## Support & Troubleshooting

**Database Connection Error?**
- Check MySQL is running
- Verify credentials in `.env`
- Ensure database `user` exists

**Token Invalid?**
- Token expires after 24 hours
- Login again to get new token
- Include `Authorization: Bearer <token>` in header

**CORS Issues?**
- CORS is enabled for all origins (`*`)
- Verify Content-Type header is set

---

**Last Updated:** April 3, 2026  
**API Version:** 2.0  
**Status:** Production Ready
