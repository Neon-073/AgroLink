-- ═══════════════════════════════════════════════════════════════════════════════
-- 🗄️ AgroLink - Normalized Database Schema (v2.0)
-- Database: user
-- Purpose: Scalable multi-role agricultural platform with proper normalization
-- ═══════════════════════════════════════════════════════════════════════════════
use AgroLink;

-- 1. DROP ALL EXISTING TABLES (Clean Slate)
-- ─────────────────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS user_products;
DROP TABLE IF EXISTS shop;
DROP TABLE IF EXISTS consumer_details;
DROP TABLE IF EXISTS dealer_details;
DROP TABLE IF EXISTS farmer_details;
DROP TABLE IF EXISTS user_details;
DROP DATABASE IF EXISTS user;

-- 2. CREATE DATABASE
-- ─────────────────────────────────────────────────────────────────────────────
CREATE DATABASE user CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE user;

-- ═════════════════════════════════════════════════════════════════════════════════
-- 3. CORE TABLES - User Management
-- ═════════════════════════════════════════════════════════════════════════════════

-- TABLE 1: user_details
-- Purpose: Central user table with authentication and basic info
-- Stores: Login credentials, profile info, role designation
CREATE TABLE user_details (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user identifier',
    username VARCHAR(100) NOT NULL UNIQUE COMMENT 'Username for login',
    phone_number VARCHAR(15) NOT NULL UNIQUE COMMENT 'Mobile number',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT 'Email address',
    password VARCHAR(255) NOT NULL COMMENT 'Hashed password (bcrypt)',
    location VARCHAR(255) COMMENT 'User location/address',
    role ENUM('farmer', 'dealer', 'consumer') NOT NULL COMMENT 'User role',
    profile_photo TEXT COMMENT 'Profile photo URL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation date',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update date',
    
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Central user authentication table';

-- TABLE 2: farmer_details
-- Purpose: Role-specific data for farmers
-- Stores: Farm information, preferences, equipment
CREATE TABLE farmer_details (
    user_id INT PRIMARY KEY COMMENT 'Reference to user_details.user_id',
    crops_selected JSON COMMENT 'Array of crop types: ["wheat", "rice", "corn", ...]',
    farm_location VARCHAR(255) COMMENT 'Specific farm location coordinates/address',
    soil_type VARCHAR(100) COMMENT 'Type of soil: loamy, sandy, clay, etc.',
    irrigation_type VARCHAR(100) COMMENT 'Irrigation method: drip, flood, sprinkler, etc.',
    farm_size FLOAT COMMENT 'Farm size in acres',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES user_details(user_id) ON DELETE CASCADE,
    INDEX idx_soil_type (soil_type),
    INDEX idx_irrigation_type (irrigation_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Farmer-specific information';

-- TABLE 3: dealer_details
-- Purpose: Role-specific data for dealers
-- Stores: Shop info, product categories, business details
CREATE TABLE dealer_details (
    user_id INT PRIMARY KEY COMMENT 'Reference to user_details.user_id',
    location VARCHAR(255) COMMENT 'Shop location',
    deals_for JSON COMMENT 'Array of product categories: ["seeds", "fertilizer", "pesticide", ...]',
    shop_photo TEXT COMMENT 'Shop storefront photo URL',
    gst_in VARCHAR(15) COMMENT 'GST Identification Number for India',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES user_details(user_id) ON DELETE CASCADE,
    INDEX idx_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Dealer-specific information';

-- TABLE 4: consumer_details
-- Purpose: Role-specific data for consumers
-- Stores: Personal preferences, gardening interests
CREATE TABLE consumer_details (
    user_id INT PRIMARY KEY COMMENT 'Reference to user_details.user_id',
    location VARCHAR(255) COMMENT 'Consumer location',
    gardening_plants JSON COMMENT 'Array of plants they grow: ["tomato", "basil", "carrot", ...]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES user_details(user_id) ON DELETE CASCADE,
    INDEX idx_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Consumer-specific information';

-- ═════════════════════════════════════════════════════════════════════════════════
-- 4. PRODUCT & MARKETPLACE TABLES
-- ═════════════════════════════════════════════════════════════════════════════════

-- TABLE 5: shop
-- Purpose: Products table - normalized structure
-- Stores: Product listings with owner information
CREATE TABLE shop (
    product_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique product identifier',
    product_name VARCHAR(150) NOT NULL COMMENT 'Product name',
    product_price FLOAT NOT NULL COMMENT 'Product price (₹)',
    product_description TEXT NOT NULL COMMENT 'Detailed product description',
    product_owner_id INT NOT NULL COMMENT 'User who listed the product',
    owner_role ENUM('farmer', 'dealer') NOT NULL COMMENT 'What role the owner has',
    product_photo TEXT COMMENT 'Product image URL',
    category VARCHAR(100) COMMENT 'Product category: seeds, fertilizer, pesticide, etc.',
    stock_quantity INT DEFAULT 0 COMMENT 'Available stock',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Product listing date',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update date',
    
    FOREIGN KEY (product_owner_id) REFERENCES user_details(user_id) ON DELETE CASCADE,
    INDEX idx_owner (product_owner_id),
    INDEX idx_category (category),
    INDEX idx_price (product_price),
    FULLTEXT INDEX ft_search (product_name, product_description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Product marketplace listings';

-- TABLE 6: user_products
-- Purpose: Many-to-many relationship between users and products they own
-- Stores: Links between products and multiple potential sellers
CREATE TABLE user_products (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Relationship identifier',
    user_id INT NOT NULL COMMENT 'User owner',
    product_id INT NOT NULL COMMENT 'Product reference',
    quantity_available INT DEFAULT 0 COMMENT 'Quantity this user has',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES user_details(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES shop(product_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id),
    INDEX idx_user (user_id),
    INDEX idx_product (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='User product ownership relationships';

-- TABLE 7: reviews
-- Purpose: Product reviews and ratings
-- Stores: Customer feedback with ratings and photos
CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique review identifier',
    product_id INT NOT NULL COMMENT 'Product being reviewed',
    user_id INT NOT NULL COMMENT 'User giving the review',
    rating INT NOT NULL COMMENT 'Rating (1-5 stars)',
    comment TEXT COMMENT 'Review text',
    photos JSON COMMENT 'Array of review photo URLs',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Review date',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last review update',
    
    FOREIGN KEY (product_id) REFERENCES shop(product_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_details(user_id) ON DELETE CASCADE,
    CHECK (rating >= 1 AND rating <= 5),
    INDEX idx_product (product_id),
    INDEX idx_user (user_id),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Product reviews and feedback';

-- ═════════════════════════════════════════════════════════════════════════════════
-- 5. VERIFY STRUCTURE
-- ═════════════════════════════════════════════════════════════════════════════════
-- Show tables created
SHOW TABLES;

-- Display column info for each table
DESCRIBE user_details;
DESCRIBE farmer_details;
DESCRIBE dealer_details;
DESCRIBE consumer_details;
DESCRIBE shop;
DESCRIBE user_products;
DESCRIBE reviews;
