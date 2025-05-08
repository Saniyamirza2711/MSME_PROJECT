CREATE DATABASE inventory_db;
USE inventory_db;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stock INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE reorder_threshold (
    product_id INT PRIMARY KEY,
    threshold INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE otp_requests (
    otp_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    otp_code VARCHAR(6),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE SET NULL
);

SHOW TABLES;

INSERT INTO products (name, stock, price) VALUES
('butter', 100, 30),
('soap', 100, 30),
('tea powder', 100, 25),
('flour', 100, 60),
('shampoo', 100, 6),
('chips', 100, 20),
('salt', 100, 40.1),
('detergent', 100, 150),
('biscuit', 100, 20),
('chocolates', 100, 50);

-- Use correct product IDs
INSERT INTO reorder_threshold (product_id, threshold) VALUES
(1, 20),  -- butter: reorder if stock < 20
(2, 20),  -- soap: reorder if stock < 20
(3, 20),   -- tea powder: reorder if stock < 20
(4, 20),  -- flour: reorder if stock < 20
(5, 20),  -- shampoo: reorder if stock < 20
(6, 20),  -- chips: reorder if stock < 20
(7, 20),   -- salt: reorder if stock <20
(8, 20),  -- detergent: reorder if stock < 20
(9, 20),  -- biscuit: reorder if stock < 20
(10, 20); -- chocolates: reorder if stock < 20

SELECT * FROM products;
SELECT * FROM reorder_threshold;
DESC sales;
