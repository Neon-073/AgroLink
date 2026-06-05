"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   AgroLink Backend - app.py (v2.0)                            ║
║              Flask + MySQL + Normalized Database Architecture                 ║
║                                                                                ║
║  Installation:                                                                 ║
║    pip install flask mysql-connector-python flask-cors python-dotenv          ║
║                 bcrypt pyjwt                                                   ║
║                                                                                ║
║  Setup Database:                                                               ║
║    1. Open MySQL: mysql -u root -p                                            ║
║    2. Run: source schema_normalized.sql                                        ║
║    3. Set .env variables                                                       ║
║                                                                                ║
║  Run: python app.py                                                            ║
║  Access: http://localhost:5000                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import bcrypt
import jwt
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)

# ═════════════════════════════════════════════════════════════════════════════
# DATABASE CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════
app.config.update(
    DB_CONFIG={
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'Neon@503810'),
        'database': os.getenv('DB_NAME', 'user'),  # NEW: database name is 'user'
    },
    SECRET_KEY=os.getenv('SECRET_KEY', 'agrolink-dev-secret-change-in-production'),
    JWT_EXPIRATION=int(os.getenv('JWT_EXPIRATION', 86400))  # 24 hours in seconds
)

print(f"🔗 Database Config: {app.config['DB_CONFIG']['database']} @ {app.config['DB_CONFIG']['host']}")

# ═════════════════════════════════════════════════════════════════════════════
# DATABASE CONNECTION UTILITY
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/api/farmer/crops', methods=['GET'])
def get_farmer_crops():
    # 1. Get the user_id from the URL (e.g., ?user_id=5)
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "message": "User ID is required"}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True) # dictionary=True makes it easier for JS to read

    try:
        # 2. Fetch only the crops belonging to this farmer
        query = "SELECT id, crop_name, quantity, status FROM farmer_details WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        crops = cursor.fetchall()

        # 3. Send the list back to the dashboard
        return jsonify({
            "success": True,
            "crops": crops
        }), 200

    except Exception as e:
        print(f"Database Error: {e}")
        return jsonify({"success": False, "message": "Could not fetch crops"}), 500
    finally:
        db.close()
        
def get_db():
    """Create and return a MySQL database connection."""
    try:
        print(f"📝 Attempting connection with config: {app.config['DB_CONFIG']}")
        conn = mysql.connector.connect(**app.config['DB_CONFIG'])
        if conn.is_connected():
            print(f"✅ Connection successful")
            return conn
        else:
            print(f"❌ Connection not active")
            return None
    except Exception as e:
        print(f"❌ Database connection error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def execute_query(query, params=None, fetch_one=False):
    """Execute a query and return results."""
    conn = get_db()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        return result
    except Error as e:
        print(f"❌ Query error: {e}")
        print(f"   Query: {query}")
        print(f"   Params: {params}")
        conn.rollback()
        return None
    finally:
        conn.close()


def execute_insert(query, params=None):
    """Execute INSERT query and return last inserted ID."""
    conn = get_db()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    except Error as e:
        print(f"❌ Insert error: {e}")
        print(f"   Query: {query}")
        print(f"   Params: {params}")
        conn.rollback()
        return None
    finally:
        conn.close()


def execute_update(query, params=None):
    """Execute UPDATE/DELETE query."""
    conn = get_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0
    except Error as e:
        print(f"❌ Update error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# ═════════════════════════════════════════════════════════════════════════════
# JWT TOKEN UTILITIES
# ═════════════════════════════════════════════════════════════════════════════

def create_token(user_id, role):
    """Create JWT token with user_id and role."""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=app.config['JWT_EXPIRATION']),
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def verify_token(token):
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def require_token(f):
    """Decorator to require valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'success': False, 'message': 'Missing token'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        
        request.user_id = payload['user_id']
        request.role = payload['role']
        return f(*args, **kwargs)
    return decorated

# ═════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK & DATABASE TEST
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - serve HTML or API info."""
    # Check if client accepts HTML
    accept_header = request.headers.get('Accept', '')
    if 'text/html' in accept_header or request.args.get('ui') == '1':
        try:
            with open('agrolink-login.html', 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return '''
            <html>
            <head><title>AgroLink</title></head>
            <body style="font-family: Arial; margin: 50px;">
            <h1>🌾 AgroLink - Agricultural Marketplace</h1>
            <p><strong>Welcome to AgroLink!</strong></p>
            <ul style="font-size: 18px; line-height: 1.8;">
                <li><a href="/login">Login</a></li>
                <li><a href="/register">Register</a></li>
                <li><a href="/dashboard">Dashboard</a></li>
            </ul>
            <hr>
            <p><strong>Backend Status:</strong> ✅ Running</p>
            <p><strong>API Available at:</strong> http://localhost:5000/test-db</p>
            </body>
            </html>
            '''
    
    # Default: serve JSON API info
    return jsonify({
        'success': True,
        'message': '🌾 AgroLink Backend v2.0',
        'database': app.config['DB_CONFIG']['database'],
        'ui_url': 'http://localhost:5000/?ui=1',
        'endpoints': {
            'health': '/test-db',
            'auth': '/auth/register, /auth/login',
            'users': '/api/user/<id>, /api/user/<id>/profile',
            'products': '/api/products, /api/products/add',
            'reviews': '/api/reviews/<product_id>'
        }
    }), 200


@app.route('/test-db', methods=['GET'])
def test_db():
    """Test database connection and show table stats."""
    try:
        conn = get_db()
        if not conn:
            return jsonify({'success': False, 'message': '❌ Database connection failed - get_db() returned None'}), 500
        
        cursor = conn.cursor()
        
        # Get table count
        cursor.execute("""
            SELECT COUNT(*) as table_count 
            FROM information_schema.tables 
            WHERE table_schema = %s
        """, (app.config['DB_CONFIG']['database'],))
        tables = cursor.fetchone()[0]
        
        # Get user count
        cursor.execute("SELECT COUNT(*) as user_count FROM user_details")
        users = cursor.fetchone()[0]
        
        # Get product count
        cursor.execute("SELECT COUNT(*) as product_count FROM shop")
        products = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': '✅ Database connection successful',
            'database': app.config['DB_CONFIG']['database'],
            'host': app.config['DB_CONFIG']['host'],
            'tables': tables,
            'statistics': {
                'total_users': users,
                'total_products': products
            }
        }), 200
    except Exception as e:
        import traceback
        error_msg = f"Exception in /test-db: {type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        return jsonify({'success': False, 'message': error_msg}), 500

# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/auth/register', methods=['POST'])
def register():
    """Register new user (farmer, dealer, or consumer)."""
    try:
        data = request.get_json()
        
        # Validate required fields (email is optional)
        required = ['username', 'phone_number', 'password', 'role']
        if not all(k in data for k in required):
            print(f"❌ Missing required fields. Provided: {list(data.keys())}")
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Validate role
        if data['role'] not in ['farmer', 'dealer', 'consumer']:
            print(f"❌ Invalid role: {data['role']}")
            return jsonify({'success': False, 'message': 'Invalid role'}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Insert into user_details
        insert_query = """
            INSERT INTO user_details 
            (username, email, phone_number, password, role, location)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data['username'],
            data.get('email', None),
            data['phone_number'],
            password_hash.decode('utf-8'),
            data['role'],
            data.get('location', '')
        )
        
        print(f"📝 Attempting to register: username={data['username']}, role={data['role']}")
        result = execute_insert(insert_query, params)
        if not result:
            print(f"❌ execute_insert returned None/0 for user insert")
            return jsonify({'success': False, 'message': 'Registration failed: Could not insert user. Username or phone already exists'}), 400
        user_id = result
        print(f"✅ User inserted with ID: {user_id}")
        
        # Create role-specific details
        if data['role'] == 'farmer':
            farmer_query = """
                INSERT INTO farmer_details (user_id, crops_selected, farm_location, soil_type, irrigation_type, farm_size)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            execute_insert(farmer_query, (
                user_id,
                json.dumps(data.get('crops_selected', [])),
                data.get('farm_location', ''),
                data.get('soil_type', ''),
                data.get('irrigation_type', ''),
                data.get('farm_size', 0.0)
            ))
            print(f"✅ Farmer details created for user {user_id}")
        
        elif data['role'] == 'dealer':
            dealer_query = """
                INSERT INTO dealer_details (user_id, location, deals_for, gst_in)
                VALUES (%s, %s, %s, %s)
            """
            execute_insert(dealer_query, (
                user_id,
                data.get('location', ''),
                json.dumps(data.get('deals_for', [])),
                data.get('gst_in', '')
            ))
            print(f"✅ Dealer details created for user {user_id}")
        
        elif data['role'] == 'consumer':
            consumer_query = """
                INSERT INTO consumer_details (user_id, location, gardening_plants)
                VALUES (%s, %s, %s)
            """
            execute_insert(consumer_query, (
                user_id,
                data.get('location', ''),
                json.dumps(data.get('gardening_plants', []))
            ))
            print(f"✅ Consumer details created for user {user_id}")
        
        # Create token
        token = create_token(user_id, data['role'])
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user_id': user_id,
            'role': data['role'],
            'token': token
        }), 201
    
    except Exception as e:
        print(f"❌ Registration exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user with username/email/phone and password and validate role."""
    try:
        data = request.get_json()
        
        # Get credentials - accept any identifier (username, email, or phone)
        username = data.get('username', '').strip() if data.get('username') else None
        email = data.get('email', '').strip() if data.get('email') else None
        phone = data.get('phone', '').strip() if data.get('phone') else None
        password = data.get('password', '')
        selected_role = data.get('role', '').lower()
        
        # Validate required fields
        errors = []
        
        # At least one identifier is required
        if not (username or email or phone):
            errors.append('username/email/phone')
        if not password:
            errors.append('password')
        if not selected_role:
            errors.append('role')
        
        if errors:
            return jsonify({
                'success': False, 
                'message': f'Missing required fields: {", ".join(errors)}'
            }), 400
        
        # Try to find user by any identifier
        user = None
        
        # Try username first (most reliable)
        if username:
            query = """
                SELECT user_id, username, password, role 
                FROM user_details 
                WHERE username = %s
                LIMIT 1
            """
            user = execute_query(query, (username,), fetch_one=True)
        
        # Try email if not found
        if not user and email:
            query = """
                SELECT user_id, username, password, role 
                FROM user_details 
                WHERE email = %s
                LIMIT 1
            """
            user = execute_query(query, (email,), fetch_one=True)
        
        # Try phone if not found
        if not user and phone:
            query = """
                SELECT user_id, username, password, role 
                FROM user_details 
                WHERE phone_number = %s
                LIMIT 1
            """
            user = execute_query(query, (phone,), fetch_one=True)
        
        if not user:
            print(f"❌ User not found: username={username}, email={email}, phone={phone}")
            return jsonify({'success': False, 'message': 'User not found'}), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            print(f"❌ Invalid password for user: {user['username']}")
            return jsonify({'success': False, 'message': 'Invalid password'}), 401
        
        # IMPORTANT: Validate that the user's role matches the selected role
        if user['role'] != selected_role:
            print(f"❌ Role mismatch: user has role '{user['role']}' but tried to login as '{selected_role}'")
            return jsonify({
                'success': False, 
                'message': f'Invalid role. You are registered as a {user["role"]}, not a {selected_role}'
            }), 401
        
        print(f"✅ Login successful: user_id={user['user_id']}, role={user['role']}")
        
        # Create token
        token = create_token(user['user_id'], user['role'])
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role'],
            'token': token
        }), 200
    
    except Exception as e:
        print(f"❌ Login exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('authlogout', methods=['POST'])
def logout():
    """Logout user - client-side token removal."""
    try:
        print("✅ User logged out")
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ═════════════════════════════════════════════════════════════════════════════
# USER ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details by ID."""
    try:
        query = """
            SELECT user_id, username, email, phone_number, location, role, profile_photo, created_at
            FROM user_details
            WHERE user_id = %s
        """
        user = execute_query(query, (user_id,), fetch_one=True)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        return jsonify({'success': True, 'data': user}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    """Get complete user profile including role-specific details."""
    try:
        # Get base user info
        user_query = "SELECT user_id, username, email, phone_number, location, role, profile_photo FROM user_details WHERE user_id = %s"
        user = execute_query(user_query, (user_id,), fetch_one=True)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        profile = user.copy()
        
        # Get role-specific details
        if user['role'] == 'farmer':
            farmer_query = "SELECT * FROM farmer_details WHERE user_id = %s"
            farmer = execute_query(farmer_query, (user_id,), fetch_one=True)
            if farmer:
                profile['farm_details'] = farmer
        
        elif user['role'] == 'dealer':
            dealer_query = "SELECT * FROM dealer_details WHERE user_id = %s"
            dealer = execute_query(dealer_query, (user_id,), fetch_one=True)
            if dealer:
                profile['dealer_info'] = dealer
        
        elif user['role'] == 'consumer':
            consumer_query = "SELECT * FROM consumer_details WHERE user_id = %s"
            consumer = execute_query(consumer_query, (user_id,), fetch_one=True)
            if consumer:
                profile['consumer_info'] = consumer
        
        return jsonify({'success': True, 'profile': profile}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/user/<int:user_id>', methods=['PUT'])
@require_token
def update_user(user_id):
    """Update user profile."""
    try:
        if request.user_id != user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Update user_details
        update_query = """
            UPDATE user_details 
            SET location = %s, profile_photo = %s
            WHERE user_id = %s
        """
        execute_update(update_query, (
            data.get('location'),
            data.get('profile_photo'),
            user_id
        ))
        
        return jsonify({'success': True, 'message': 'User updated'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ═════════════════════════════════════════════════════════════════════════════
# PRODUCT ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filters."""
    try:
        # Handle filters
        category = request.args.get('category')
        owner_id = request.args.get('owner_id')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        
        query = "SELECT * FROM shop WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        if owner_id:
            query += " AND product_owner_id = %s"
            params.append(owner_id)
        
        if min_price:
            query += " AND product_price >= %s"
            params.append(float(min_price))
        
        if max_price:
            query += " AND product_price <= %s"
            params.append(float(max_price))
        
        query += " ORDER BY created_at DESC LIMIT 100"
        
        products = execute_query(query, params)
        
        return jsonify({
            'success': True,
            'count': len(products) if products else 0,
            'products': products or []
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product with reviews."""
    try:
        # Get product
        product_query = "SELECT * FROM shop WHERE product_id = %s"
        product = execute_query(product_query, (product_id,), fetch_one=True)
        
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        # Get reviews
        reviews_query = """
            SELECT r.review_id, r.rating, r.comment, r.photos, r.created_at, u.username
            FROM reviews r
            JOIN user_details u ON r.user_id = u.user_id
            WHERE r.product_id = %s
            ORDER BY r.created_at DESC
        """
        reviews = execute_query(reviews_query, (product_id,))
        
        product['reviews'] = reviews or []
        
        # Calculate average rating
        if reviews:
            avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
            product['average_rating'] = round(avg_rating, 2)
            product['review_count'] = len(reviews)
        else:
            product['average_rating'] = 0
            product['review_count'] = 0
        
        return jsonify({'success': True, 'product': product}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/farmer/crops', methods=['POST'])
@require_token
def add_farmer_crop():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    # query to insert data
    query = "INSERT INTO farmer_crops (user_id, crop_name, quantity) VALUES (%s, %s, %s)"
    values = (request.user_id, data['crop_name'], data['quantity'])
    
    try:
        cursor.execute(query, values)
        db.commit()
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        db.close()


@app.route('/api/products/add', methods=['POST'])
@require_token
def add_product():
    """Add new product to shop."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('product_name') or not data.get('product_price') or not data.get('product_description'):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Check user role
        role_query = "SELECT role FROM user_details WHERE user_id = %s"
        user = execute_query(role_query, (request.user_id,), fetch_one=True)
        
        if user['role'] not in ['farmer', 'dealer']:
            return jsonify({'success': False, 'message': 'Only farmers and dealers can add products'}), 403
        
        # Insert product
        insert_query = """
            INSERT INTO shop 
            (product_name, product_price, product_description, product_owner_id, owner_role, product_photo, category, stock_quantity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('product_name'),
            float(data.get('product_price')),
            data.get('product_description'),
            request.user_id,
            user['role'],
            data.get('product_photo', ''),
            data.get('category', 'General'),
            int(data.get('stock_quantity', 0))
        )
        
        product_id = execute_insert(insert_query, params)
        
        if not product_id:
            return jsonify({'success': False, 'message': 'Failed to add product'}), 500
        
        # Also add to user_products linking table
        link_query = "INSERT INTO user_products (user_id, product_id, quantity_available) VALUES (%s, %s, %s)"
        execute_insert(link_query, (request.user_id, product_id, data.get('stock_quantity', 0)))
        
        return jsonify({
            'success': True,
            'message': 'Product added successfully',
            'product_id': product_id
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    



@app.route('/api/products/<int:product_id>', methods=['PUT'])
@require_token
def update_product(product_id):
    """Update product details."""
    try:
        # Check ownership
        owner_query = "SELECT product_owner_id FROM shop WHERE product_id = %s"
        product = execute_query(owner_query, (product_id,), fetch_one=True)
        
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        if product['product_owner_id'] != request.user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        update_query = """
            UPDATE shop 
            SET product_name = %s, product_price = %s, product_description = %s, category = %s, stock_quantity = %s
            WHERE product_id = %s
        """
        
        execute_update(update_query, (
            data.get('product_name'),
            float(data.get('product_price')),
            data.get('product_description'),
            data.get('category'),
            int(data.get('stock_quantity', 0)),
            product_id
        ))
        
        return jsonify({'success': True, 'message': 'Product updated'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@require_token
def delete_product(product_id):
    """Delete product."""
    try:
        # Check ownership
        owner_query = "SELECT product_owner_id FROM shop WHERE product_id = %s"
        product = execute_query(owner_query, (product_id,), fetch_one=True)
        
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        if product['product_owner_id'] != request.user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        delete_query = "DELETE FROM shop WHERE product_id = %s"
        execute_update(delete_query, (product_id,))
        
        return jsonify({'success': True, 'message': 'Product deleted'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ═════════════════════════════════════════════════════════════════════════════
# CROP ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════


@app.route('/api/farmer/crops', methods=['GET', 'POST'])
@require_token
def handle_crops():
    if request.method == 'POST':
        data = request.json
        query = "INSERT INTO farmer_crops (user_id, crop_name, quantity) VALUES (%s, %s, %s)"
        execute_insert(query, (request.user_id, data['crop_name'], data['quantity']))
        return jsonify({'success': True})
    
    # GET logic to load crops
    query = "SELECT * FROM farmer_crops WHERE user_id = %s"
    crops = execute_query(query, (request.user_id,))
    return jsonify({'success': True, 'crops': crops})

# ═════════════════════════════════════════════════════════════════════════════
# REVIEW ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/api/reviews/<int:product_id>', methods=['GET'])
def get_reviews(product_id):
    """Get all reviews for a product."""
    try:
        query = """
            SELECT r.review_id, r.rating, r.comment, r.photos, r.created_at, u.username, u.profile_photo
            FROM reviews r
            JOIN user_details u ON r.user_id = u.user_id
            WHERE r.product_id = %s
            ORDER BY r.created_at DESC
        """
        reviews = execute_query(query, (product_id,))
        
        return jsonify({
            'success': True,
            'count': len(reviews) if reviews else 0,
            'reviews': reviews or []
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/reviews', methods=['POST'])
@require_token
def add_review():
    """Add review for a product."""
    try:
        data = request.get_json()
        
        # Validate
        if not data.get('product_id') or not data.get('rating'):
            return jsonify({'success': False, 'message': 'Missing product_id or rating'}), 400
        
        if not 1 <= int(data['rating']) <= 5:
            return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
        
        insert_query = """
            INSERT INTO reviews (product_id, user_id, rating, comment, photos)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        review_id = execute_insert(insert_query, (
            int(data['product_id']),
            request.user_id,
            int(data['rating']),
            data.get('comment', ''),
            json.dumps(data.get('photos', []))
        ))
        
        if not review_id:
            return jsonify({'success': False, 'message': 'Failed to add review'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Review added successfully',
            'review_id': review_id
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ═════════════════════════════════════════════════════════════════════════════
# UI ROUTES - SERVE HTML FILES
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/login')
def login_page():
    """Serve login page."""
    try:
        with open('agrolink-login.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'<h1>Error loading login page: {str(e)}</h1>', 500

@app.route('/register')
def register_page():
    """Serve registration page."""
    try:
        with open('agrolink-register.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'<h1>Error loading registration page: {str(e)}</h1>', 500

@app.route('/dashboard')
def dashboard_root():
    """Serve main dashboard landing page."""
    return '''
    <html>
    <head>
        <title>AgroLink Dashboard</title>
        <style>
            body { font-family: Arial; margin: 50px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2ecc71; text-align: center; }
            .roles { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 30px 0; }
            .role-card { padding: 20px; text-align: center; background: #f9f9f9; border-radius: 5px; cursor: pointer; transition: 0.3s; }
            .role-card:hover { background: #e8f5e9; transform: scale(1.05); }
            a { text-decoration: none; color: #2ecc71; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 Choose Your Dashboard</h1>
            <div class="roles">
                <div class="role-card"><a href="/dashboard/farmer">🌾 Farmer</a></div>
                <div class="role-card"><a href="/dashboard/dealer">🏪 Dealer</a></div>
                <div class="role-card"><a href="/dashboard/consumer">👤 Consumer</a></div>
            </div>
            <p style="text-align: center;"><a href="/">← Back to Home</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard/farmer')
def farmer_dashboard():
    """Serve farmer dashboard."""
    try:
        with open('agrolink-farmer-dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'<h1>Error loading farmer dashboard: {str(e)}</h1>', 500

@app.route('/dashboard/dealer')
def dealer_dashboard():
    """Serve dealer dashboard."""
    try:
        with open('agrolink-dealer-dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'<h1>Error loading dealer dashboard: {str(e)}</h1>', 500

@app.route('/dashboard/consumer')
def consumer_dashboard():
    """Serve consumer dashboard."""
    try:
        with open('agrolink-consumer-dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'<h1>Error loading consumer dashboard: {str(e)}</h1>', 500

# ═════════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═════════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500


if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         🌾 AgroLink Backend (v2.0) Starting...               ║")
    print("║         Database: user                                        ║")
    print("║         Host: {:<46} ║".format(app.config['DB_CONFIG']['host']))
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    # Test database connection on startup
    test_conn = get_db()
    if test_conn:
        print("✅ Database connection successful")
        test_conn.close()
    else:
        print("❌ Database connection failed - check your configuration")
    
    print()
    print("🚀 API Routes:")
    print("   GET  /                          - API info")
    print("   GET  /test-db                   - Database test")
    print("   POST /auth/register             - Register new user")
    print("   POST /auth/login                - Login")
    print("   GET  /api/user/<id>             - Get user")
    print("   GET  /api/user/<id>/profile     - Get full profile")
    print("   PUT  /api/user/<id>             - Update user (requires token)")
    print("   GET  /api/products              - List products")
    print("   GET  /api/products/<id>         - Get product details")
    print("   POST /api/products/add          - Add product (requires token)")
    print("   PUT  /api/products/<id>         - Update product (requires token)")
    print("   DEL  /api/products/<id>         - Delete product (requires token)")
    print("   GET  /api/reviews/<product_id>  - Get reviews")
    print("   POST /api/reviews               - Add review (requires token)")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
