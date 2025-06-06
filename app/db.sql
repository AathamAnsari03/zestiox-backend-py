-- Create database
CREATE DATABASE IF NOT EXISTS zestiox CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE zestiox;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(10) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu categories
CREATE TABLE menu_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Menu items
CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES menu_categories(id)
);

-- Orders
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Preparing',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order items
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

-- Cart (one active cart per user)
CREATE TABLE cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

-- Sample data for menu_categories
INSERT INTO menu_categories (name) VALUES
('Starters'),
('Indian Breads'),
('Main Course'),
('Rice & Biryani'),
('Desserts'),
('Beverages');

-- Sample data for users
INSERT INTO users (name, mobile, password_hash) VALUES
('Amit Sharma', '9876543210', '$2b$12$examplehash1'),
('Priya Singh', '9123456789', '$2b$12$examplehash2');

-- Sample data for menu_items (50+ Indian dishes)
INSERT INTO menu_items (name, price, category_id) VALUES
('Paneer Tikka', 180.00, 1),
('Chicken Tikka', 220.00, 1),
('Veg Spring Roll', 150.00, 1),
('Hara Bhara Kebab', 160.00, 1),
('Gobi Manchurian', 140.00, 1),
('Samosa', 40.00, 1),
('Aloo Tikki', 50.00, 1),
('Fish Amritsari', 250.00, 1),
('Tandoori Mushroom', 170.00, 1),
('Chilli Paneer', 180.00, 1),

('Butter Naan', 40.00, 2),
('Garlic Naan', 50.00, 2),
('Tandoori Roti', 25.00, 2),
('Lachha Paratha', 45.00, 2),
('Missi Roti', 30.00, 2),
('Stuffed Kulcha', 60.00, 2),
('Roomali Roti', 35.00, 2),
('Plain Naan', 35.00, 2),
('Cheese Naan', 70.00, 2),
('Onion Kulcha', 55.00, 2),

('Paneer Butter Masala', 220.00, 3),
('Dal Makhani', 180.00, 3),
('Chicken Curry', 250.00, 3),
('Mutton Rogan Josh', 320.00, 3),
('Chole Masala', 160.00, 3),
('Bhindi Masala', 150.00, 3),
('Kadai Paneer', 210.00, 3),
('Egg Curry', 170.00, 3),
('Aloo Gobi', 140.00, 3),
('Palak Paneer', 200.00, 3),

('Veg Biryani', 180.00, 4),
('Chicken Biryani', 240.00, 4),
('Mutton Biryani', 320.00, 4),
('Jeera Rice', 90.00, 4),
('Peas Pulao', 110.00, 4),
('Curd Rice', 80.00, 4),
('Fried Rice', 120.00, 4),
('Egg Fried Rice', 140.00, 4),
('Lemon Rice', 100.00, 4),
('Ghee Rice', 110.00, 4),

('Gulab Jamun', 60.00, 5),
('Rasgulla', 60.00, 5),
('Kheer', 70.00, 5),
('Jalebi', 50.00, 5),
('Ice Cream', 80.00, 5),
('Rasmalai', 90.00, 5),
('Gajar Halwa', 85.00, 5),
('Kulfi', 70.00, 5),
('Mysore Pak', 75.00, 5),
('Ladoo', 55.00, 5),

('Masala Chai', 30.00, 6),
('Lassi', 50.00, 6),
('Sweet Lime Juice', 60.00, 6),
('Cold Coffee', 70.00, 6),
('Buttermilk', 40.00, 6);

-- Sample data for orders
INSERT INTO orders (user_id, total_amount, status) VALUES
(1, 460.00, 'Delivered'),
(2, 320.00, 'Preparing');

-- Sample data for order_items
INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES
(1, 1, 2, 180.00),   -- Paneer Tikka x2
(1, 11, 4, 40.00),   -- Butter Naan x4
(2, 22, 1, 180.00),  -- Dal Makhani x1
(2, 32, 2, 70.00);   -- Kheer x2

-- Sample data for cart_items
INSERT INTO cart_items (user_id, menu_item_id, quantity) VALUES
(1, 21, 1),   -- Paneer Butter Masala x1
(1, 12, 2),   -- Garlic Naan x2
(2, 31, 1);   -- Veg Biryani x1