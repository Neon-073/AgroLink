# 🌾 AgroLink v2.0 - System Architecture Overview

## 🏗️ Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER (Frontend)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │   Farmer         │  │   Dealer         │  │   Consumer       │          │
│  │   Dashboard      │  │   Dashboard      │  │   Dashboard      │          │
│  │   (HTML/CSS/JS)  │  │   (HTML/CSS/JS)  │  │   (HTML/CSS/JS)  │          │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘          │
│           │                     │                    │                      │
│           └─────────────────────┼────────────────────┘                      │
│                                 │                                            │
│                    JWT Token Stored in localStorage                          │
│                    All requests include Authorization header               │
│                                 │                                            │
└─────────────────────────────────┼────────────────────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │   HTTP/REST     │   JSON          │
                │   Requests      │   Responses     │
                │                 │                 │
┌───────────────┴─────────────────┴─────────────────┴─────────────────────────┐
│                        API LAYER (Flask Backend)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  HTTP Server (Port 5000)                                              │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                        │ │
│  │  Routes:                                                              │ │
│  │  ┌─ Health Check              ┌─ User Management                      │ │
│  │  │  GET /                      │  GET /api/user/<id>                  │ │
│  │  │  GET /test-db               │  GET /api/user/<id>/profile         │ │
│  │  │                             │  PUT /api/user/<id>                 │ │
│  │  ├─ Authentication            │                                       │ │
│  │  │  POST /auth/register        ├─ Product Management                 │ │
│  │  │  POST /auth/login           │  GET /api/products                  │ │
│  │  │  │                          │  GET /api/products/<id>             │ │
│  │  │  └─ Returns JWT Token       │  POST /api/products/add             │ │
│  │  │                             │  PUT /api/products/<id>             │ │
│  │  │                             │  DELETE /api/products/<id>          │ │
│  │  │                             │                                       │ │
│  │  │                             ├─ Review Management                   │ │
│  │  │                             │  GET /api/reviews/<product_id>      │ │
│  │  │                             │  POST /api/reviews                  │ │
│  │  │                             │                                       │ │
│  │  └─────────────────────────────┴───────────────────────────────────── │ │
│  │                                                                        │ │
│  │  Middleware:                                                          │ │
│  │  • CORS Enabled (cross-origin requests allowed)                      │ │
│  │  • JWT Authentication (@require_token decorator)                     │ │
│  │  • Error Handling (try-catch with meaningful messages)               │ │
│  │  • Request Logging                                                   │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                 │                                            │
│                    Database Query Execution Layer                            │
│                    • Connection pooling                                      │
│                    • Parameterized queries (SQL injection prevention)       │
│                    • Transaction management                                 │
│                                 │                                            │
└─────────────────────────────────┼────────────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │   MySQL     │   Port 3306 │
                    │   Protocol  │   TCP       │
                    │             │             │
┌───────────────────┴─────────────┴─────────────┴──────────────────────────────┐
│                      DATABASE LAYER (MySQL)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Database: "user"                                                            │
│  Character Set: utf8mb4 (Unicode support)                                   │
│                                                                              │
│  ┌─ CORE TABLES ─────────────────────┐  ┌─ MARKETPLACE ──────────────────┐ │
│  │                                   │  │                                │ │
│  │  [user_details]                   │  │  [shop]           [reviews]   │ │
│  │  • user_id (PK)                   │  │  • product_id      • review_id │ │
│  │  • username                       │  │  • product_name    • rating    │ │
│  │  • email                          │  │  • price           • comment   │ │
│  │  • password (bcrypt)              │  │  • description     • photos    │ │
│  │  • phone_number                   │  │  • owner_id (FK)   │ user_id   │ │
│  │  • role (ENUM)                    │  │  • photos          │ product_id│ │
│  │  • location                       │  │                    │           │ │
│  │                                   │  │  [user_products]   │           │ │
│  │  ├─ [farmer_details] (FK)        │  │  • user_id (FK)    │           │ │
│  │  │  • crops_selected (JSON)      │  │  • product_id (FK) │           │ │
│  │  │  • farm_location              │  │  • quantity        │           │ │
│  │  │  • soil_type                  │  │                    │           │ │
│  │  │  • irrigation_type            │  └────────────────────┴───────────┘ │
│  │  │  • farm_size                  │                                       │
│  │  │                               │                                       │
│  │  ├─ [dealer_details] (FK)        │                                       │
│  │  │  • location                   │                                       │
│  │  │  • deals_for (JSON)           │                                       │
│  │  │  • shop_photo                 │                                       │
│  │  │  • gst_in                     │                                       │
│  │  │                               │                                       │
│  │  └─ [consumer_details] (FK)      │                                       │
│  │     • location                   │                                       │
│  │     • gardening_plants (JSON)    │                                       │
│  │                                  │                                       │
│  └────────────────────────────────────────────────────────────────────────━│ │
│                                                                              │
│  Constraints:                                                                │
│  • Foreign key relationships with CASCADE delete                            │
│  • UNIQUE constraints on email, username, phone_number                     │
│  • CHECK constraint on review ratings (1-5)                                │
│  • Proper indexing for performance                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

### Registration Flow
```
User Registration Form
    │
    ├─ Validate input
    ├─ Hash password (bcrypt)
    ├─ Create JWT token
    │
    ├─→ INSERT into user_details
    │
    ├─→ Based on role:
    │   ├─ Farmer     → INSERT into farmer_details
    │   ├─ Dealer     → INSERT into dealer_details
    │   └─ Consumer   → INSERT into consumer_details
    │
    └─→ Response: { user_id, token, role }
```

### Product Add Flow
```
Add Product Request (with token)
    │
    ├─ Verify JWT token
    ├─ Check user role (must be farmer/dealer)
    │
    ├─→ INSERT into shop
    │   └─ product_owner_id = current_user_id
    │
    ├─→ INSERT into user_products
    │   └─ Link user to product
    │
    └─→ Response: { product_id }
```

### Review Flow
```
Add Review Request (with token)
    │
    ├─ Verify JWT token
    ├─ Validate rating (1-5)
    ├─ Check product exists
    │
    ├─→ INSERT into reviews
    │   ├─ product_id
    │   ├─ user_id
    │   ├─ rating
    │   └─ comment
    │
    ├─ Calculate average rating
    │
    └─→ Response: { review_id }
```

---

## 🔐 Security Flow

```
┌─────────────────────────────────────────────────────┐
│      1. USER REGISTRATION / LOGIN                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Password: "user_password"                          │
│      │                                              │
│      ├─→ bcrypt.hashpw() (rounds=12)               │ 
│      │                                              │
│      └─→ Stored: "$2b$12$..." (never reversible)   │
│                                                     │
│  On Login: bcrypt.checkpw(input, stored)           │
│      └─→ Returns: True/False                        │
│                                                     │
│  If Password Match:                                 │
│      ├─→ Create JWT: {user_id, role, exp}          │
│      ├─→ Sign with SECRET_KEY                      │
│      └─→ Return JWT to client                      │
│                                                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  2. PROTECTED ENDPOINT REQUEST                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Client sends:                                      │
│  Authorization: Bearer eyJhbGciOiJIUzI1NiIs...    │
│                                                     │
│  Server:                                            │
│  ├─ Extract token from header                       │
│  ├─ Verify signature with SECRET_KEY               │
│  ├─ Check expiration time                           │
│  ├─ Extract user_id and role                        │
│  └─ Attach to request object                        │
│                                                     │
│  If valid:   Continue to endpoint                   │
│  If invalid: Return 401 Unauthorized               │
│                                                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  3. PARAMETERIZED QUERIES (SQL Injection Prevention) │
├─────────────────────────────────────────────────────┤
│                                                     │
│  UNSAFE: query = f"SELECT * FROM shop WHERE      │
│          product_id = {input}"                      │
│          └─→ Vulnerable to: '; DROP TABLE shop; -- │
│                                                     │
│  SAFE:   query = "SELECT * FROM shop WHERE         │
│          product_id = %s"                          │
│          params = (input,)                         │
│          cursor.execute(query, params)             │
│          └─→ Input treated as data only             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 📈 System Scalability

```
Current (Local Development)
└─ SQLite or MySQL (local)
   └─ ~100 concurrent users
   └─ ~10,000 products
   └─ Suitable for: Testing, small teams

Next Step (Production Ready)
└─ MySQL on dedicated server
   └─ ~1,000 concurrent users
   └─ ~1,000,000 products
   └─ Gunicorn + Nginx load balancing
   └─ Suitable for: Medium business

Enterprise Scale
├─ MySQL replication (master-slave)
│  └─ ~10,000 concurrent users
│  └─ ~10,000,000 products
├─ Redis cache layer
├─ Elasticsearch for search
├─ CDN for static files
├─ Microservices architecture
└─ Suitable for: Large platforms
```

---

## 🔄 Deployment Architectures

### Quick Start (Development)
```
┌──────────────────┐
│  Flask Dev Server│ (app_v2.py)
│  Port 5000       │
├──────────────────┤
│  SQLite/MySQL    │ (schema_normalized.sql)
│  Localhost       │
└──────────────────┘
```

### Production (Single Server)
```
┌─────────────────────────┐
│  Nginx Reverse Proxy    │
│  Port 80/443            │
├─────────────────────────┤
│  Gunicorn WSGI Server   │
│  Workers × 4            │
├─────────────────────────┤
│  MySQL Server           │
│  Data & Backups         │
└─────────────────────────┘
```

### Enterprise (Scalable)
```
┌──────────────────────┐
│  CloudFlare DNS      │
├──────────────────────┤
│  Nginx Load Balancer │
├──────────────────────┤
│  ┌────────────────┐  │
│  │ Gunicorn × 10  │  │ Multiple servers
│  │ Port 5000-5009 │  │
│  └────────────────┘  │
├──────────────────────┤
│  MySQLCluster        │
│  (Master + Slaves)   │
├──────────────────────┤
│  Redis Cache         │
│  Elasticsearch       │
└──────────────────────┘
```

---

## 📝 Data Normalization Comparison

### Before (v1.0): Denormalized
```sql
users
├─ full_name           (string)
├─ email               (string)
├─ phone               (string)
├─ password            (string)
├─ role                (enum)
├─ profile_photo       (URL)
├─ shop_photo          (URL)     ← NULL for farmers
├─ soil_type           (string)  ← NULL for dealers
├─ irrigation_type     (string)  ← NULL for dealers
├─ dealer_category     (string)  ← NULL for farmers
├─ my_crops            (JSON)    ← NULL for dealers
├─ my_products         (JSON)    ← NULL for farmers
└─ created_at          (timestamp)

Issues:
• Wasted space (many NULL values)
• Complex queries (need to check role first)
• Difficult to add new role types
• Hard to enforce constraints
```

### After (v2.0): Normalized (BCNF)
```
user_details
├─ user_id
├─ username
├─ email
├─ phone
├─ password
├─ role
└─ created_at

farmer_details (only created if role='farmer')
├─ user_id (FK) ─→ user_details
├─ crops_selected (JSON)
├─ soil_type
├─ irrigation_type
└─ farm_size

dealer_details (only created if role='dealer')
├─ user_id (FK) ─→ user_details
├─ shop_photo
├─ deals_for (JSON)
└─ gst_in

consumer_details (only created if role='consumer')
├─ user_id (FK) ─→ user_details
└─ gardening_plants (JSON)

Benefits:
✓ No NULL values
✓ Cleaner queries
✓ Easy to add roles
✓ Strong constraints
✓ Better performance
```

---

## 🧠 Key Design Decisions

### 1. Role-Specific Tables
✅ Why: Each role has different attributes
❌ Alternative: Single table with many NULLs (wasteful)

### 2. JSON for Flexible Arrays
✅ Why: Crop/product types can change without schema migration
❌ Alternative: Normalize to separate tables (over-engineered)

### 3. Central user_details Table
✅ Why: Single source of truth for user identity
❌ Alternative: Separate tables per role (complex joins)

### 4. Foreign Key with CASCADE Delete
✅ Why: Ensure referential integrity, auto-cleanup
❌ Alternative: Manual deletion handling (error-prone)

### 5. Indexed Key Columns
✅ Why: Fast lookups on email, user_id, product_id
❌ Alternative: No indexes (slow queries)

---

## 📊 Performance Metrics

### Expected Response Times (Localhost)
```
Operation                    Time        Notes
─────────────────────────────────────────────────
Register user                50-100ms    bcrypt hashing
Login                         50-100ms    bcrypt comparison
Get products (10)             20-50ms     Indexed query
Add product                   30-80ms     Insert + FK check
Add review                    20-60ms     Insert + constraint check
Get product with reviews      40-100ms    JOIN operation
Filter products (100 results) 50-150ms    WHERE + LIMIT
```

### Scaling Characteristics
```
Users       Products    Performance
──────────────────────────────────
1,000       10,000      Instant (<100ms)
10,000      100,000     Instant (<100ms)
100,000     1,000,000   Slow queries (>1s)
1,000,000   10,000,000  Requires indexing strategy
```

---

## 🔧 Monitoring & Maintenance

### Database Health Checks
```sql
-- Check database size
SELECT SUM(data_length + index_length) / 1024 / 1024 AS size_mb
FROM information_schema.tables
WHERE table_schema = 'user';

-- Check table row counts
SELECT table_name, table_rows
FROM information_schema.tables
WHERE table_schema = 'user';

-- Check slow queries
SELECT query_time, query FROM mysql.slow_log
LIMIT 10;
```

### Backup Strategy
```bash
# Daily automated backup
0 2 * * * mysqldump -u root -p user > /backups/user_$(date +\%Y\%m\%d).sql

# Monthly archive
0 0 1 * * tar -czf /archive/user_$(date +\%Y\%m).tar.gz /backups/
```

---

## 🎯 System Capabilities

### Current System Can Handle
✅ 3 user roles with different attributes
✅ Product marketplace with reviews and ratings
✅ JWT authentication with expiration
✅ Role-based access control
✅ Complex product filtering
✅ 14 REST endpoints
✅ Full CRUD operations

### Future Enhancements
🔮 Payment integration (Razorpay/Stripe)
🔮 Push notifications
🔮 Advanced search (Elasticsearch)
🔮 Recommendation engine
🔮 Admin dashboard
🔮 Analytics and reporting
🔮 Mobile API endpoints

---

**AgroLink v2.0 - Complete Normalized Architecture**
**Status:** Production Ready ✅
**Estimated Setup Time:** 5-10 minutes
**Scalability:** Up to 1M+ users with optimization
