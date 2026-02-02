-- Drop existing database if it exists (for clean setup)
DROP DATABASE IF EXISTS momo_db;
CREATE DATABASE momo_db
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;
USE momo_db;

-- Create Users table
CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each user, auto-incremented',
    user_phone_number VARCHAR(20) COMMENT'Mobile phone number used for identification',
    user_name VARCHAR(50) COMMENT 'name of the user'
)
COMMENT='Stores user information for mobile money transactions';

-- Create Transactions table
CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each transaction category',
    category_type VARCHAR(50) NOT NULL COMMENT 'Specific type or name of the transaction category',
    INDEX idx_category_type (category_type) COMMENT 'Index for category type searches'
) 
COMMENT='Defines transaction categories for classification';

CREATE TABLE user_categories (
    user_id INT NOT NULL COMMENT 'Foreign key referencing the user',
    category_id INT NOT NULL COMMENT 'Foreign key referencing the transaction category',
    PRIMARY KEY (user_id, category_id) COMMENT 'Composite primary key',
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
) 
COMMENT='Junction table linking users to their associated transaction categories';

-- =====================================================
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each transaction',
    sender_id INT NOT NULL COMMENT 'Foreign key referencing the user who initiated the transaction',
    receiver_id INT NOT NULL COMMENT 'Foreign key referencing the user who received the transaction',
    amount DECIMAL(15, 2) NOT NULL COMMENT 'Monetary value of the transaction',
    category_id INT NOT NULL COMMENT 'Foreign key linking this transaction to its category type',
    transaction_time DATETIME NOT NULL COMMENT 'Timestamp indicating when the transaction occurred',
    CHECK (amount > 0),
    CHECK (sender_id != receiver_id),
    FOREIGN KEY (sender_id) REFERENCES user(user_id) 
    ON DELETE RESTRICT,
    FOREIGN KEY (receiver_id) REFERENCES user(user_id) 
        ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id) 
        ON DELETE RESTRICT,
    CONSTRAINT chk_different_users CHECK (sender_id != receiver_id),
    INDEX idx_sender (sender_id) COMMENT 'Index for fast sender lookups',
    INDEX idx_receiver (receiver_id) COMMENT 'Index for fast receiver lookups',
    INDEX idx_category (category_id) COMMENT 'Index for category-based queries',
    INDEX idx_transaction_time (transaction_time) COMMENT 'Index for time-based queries and sorting'
) 
COMMENT='Core table storing all mobile money transaction records';

CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each log entry',
    action VARCHAR(50) NOT NULL COMMENT 'Description of the specific action or event that was logged',
    timestamp DATETIME NOT NULL COMMENT 'Date and time when the log entry was created',
    transaction_id INT COMMENT 'Foreign key linking log entry to a specific transaction (nullable)',
    category_id INT COMMENT 'Foreign key linking log entry to a transaction category (nullable)',
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE ,
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE ,
    INDEX idx_timestamp (timestamp) COMMENT 'Index for time-based log queries',
    INDEX idx_action (action) COMMENT 'Index for action-based filtering',
    INDEX idx_transaction_log (transaction_id) COMMENT 'Index for transaction-related logs',
    INDEX idx_category_log (category_id) COMMENT 'Index for category-related logs'
) 
COMMENT='System logging table for auditing and tracking data processing events';

INSERT INTO user (user_phone_number, user_name) VALUES
('*********567', 'John Mukasa'),
('*********667', 'Sarah Nakato'),
('*********157', 'Peter Ochieng'),
('*********560', 'Mary Achieng'),
('*********123', 'David Okello');

INSERT INTO transaction_categories (category_type) VALUES
('Money Transfer'),
('Airtime Purchase'),
('Bill Payment'),
('Cash Withdrawal'),
('Cash Deposit');


-- Insert sample user-category associations
INSERT INTO user_categories (user_id, category_id) VALUES
(1, 1),  -- John uses Money Transfer
(1, 2),  -- John uses Airtime Purchase
(2, 1),  -- Sarah uses Money Transfer
(2, 3),  -- Sarah uses Bill Payment
(3, 1);  -- Peter uses Money Transfer;

-- Insert sample transactions
INSERT INTO transactions (sender_id, receiver_id, amount, category_id, transaction_time) VALUES
(1, 2, 50000.00, 1, '2025-01-15 10:30:00'),
(2, 3, 25000.00, 1, '2025-01-15 14:20:00'),
(3, 4, 10000.00, 1, '2025-01-16 09:15:00'),
(4, 5, 15000.00, 2, '2025-01-16 11:45:00'),
(5, 1, 30000.00, 1, '2025-01-17 08:30:00');

-- Insert sample system logs
INSERT INTO system_logs (action, timestamp, transaction_id, category_id) VALUES
('Transaction Processed', '2025-01-15 10:30:05', 1, 1),
('Transaction Processed', '2025-01-15 14:20:03', 2, 1),
('Transaction Processed', '2025-01-16 09:15:08', 3, 1),
('Airtime Purchase', '2025-01-16 11:45:12', 4, 2),
('Transaction Processed', '2025-01-17 08:30:15', 5, 1);

-- Testing basic CRUD operations:
-- Read
SELECT * FROM user;

-- Update 
UPDATE user SET user_phone_number = '*********222' WHERE user_name = 'John Mukasa';  
SELECT * FROM user WHERE user_name = 'John Mukasa';  -- Verify update

-- Delete 
DELETE FROM user WHERE user_name = 'David Okello'; 
-- Should not work because of the restrictions set earlier to maintain data integrity
SELECT * FROM user WHERE user_name = 'David Okello';  