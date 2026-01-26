# JSON Schemas Documentation

## Overview
This document contains detailed specifications, data types, mapping strategies, and SQL queries for all JSON schema entities used in the Momo payment system.

---

## Simple Entity Schemas

### 1. User Entity
**SQL Source:** `user` table

#### Data Structure:
```json
{
  "user_id": 1,
  "user_phone_number": "*********567",
  "user_name": "John Mukasa"
}
```

#### Data Types:
- `user_id`: Integer
- `user_phone_number`: String
- `user_name`: String

#### Mapping Strategy:
- Direct 1:1 column-to-property mapping
- All columns from `user` table included

---

### 2. Transaction Category Entity
**SQL Source:** `transaction_categories` table

#### Data Structure:
```json
{
  "category_id": 1,
  "category_type": "Money Transfer"
}
```

#### Data Types:
- `category_id`: Integer
- `category_type`: String

#### Mapping Strategy:
- Direct 1:1 column-to-property mapping
- All columns from `transaction_categories` table included

---

### 3. Basic Transaction Entity
**SQL Source:** `transactions` table (flat representation)

#### Data Structure:
```json
{
  "transaction_id": 1,
  "sender_id": 1,
  "receiver_id": 2,
  "amount": 50000.00,
  "category_id": 1,
  "transaction_time": "2025-01-15T10:30:00Z"
}
```

#### Data Types:
- `transaction_id`: Integer
- `sender_id`: Integer (foreign key)
- `receiver_id`: Integer (foreign key)
- `amount`: Number (decimal with 2 places)
- `category_id`: Integer (foreign key)
- `transaction_time`: String (ISO 8601 datetime)

#### Mapping Strategy:
- Direct mapping from `transactions` table
- Foreign keys represented as IDs only (not expanded)
- DATETIME converted to ISO 8601 string format

---

### 4. System Log Entity
**SQL Source:** `system_logs` table

#### Data Structure:
```json
{
  "log_id": 1,
  "action": "Transaction Processed",
  "timestamp": "2025-01-15T10:30:05Z",
  "transaction_id": 1,
  "category_id": 1
}
```

#### Data Types:
- `log_id`: Integer
- `action`: String
- `timestamp`: String (ISO 8601 datetime)
- `transaction_id`: Integer (nullable foreign key)
- `category_id`: Integer (nullable foreign key)

---

## Nested JSON with Related Data

### 5. User with Associated Categories
**SQL Sources:** `user`, `user_categories`, `transaction_categories` tables (JOIN)

#### Data Structure:
```json
{
  "user_id": 1,
  "user_phone_number": "*********567",
  "user_name": "John Mukasa",
  "categories": [
    {
      "category_id": 1,
      "category_type": "Money Transfer"
    },
    {
      "category_id": 2,
      "category_type": "Airtime Purchase"
    }
  ]
}
```

#### Nesting Strategy:
- Base user data from `user` table
- `categories` array populated via JOIN through `user_categories` junction table
- Each category is a complete object (not just an ID)

#### SQL Query:
```sql
SELECT 
    u.user_id,
    u.user_phone_number,
    u.user_name,
    tc.category_id,
    tc.category_type
FROM user u
LEFT JOIN user_categories uc ON u.user_id = uc.user_id
LEFT JOIN transaction_categories tc ON uc.category_id = tc.category_id
WHERE u.user_id = 1;
```

---

### 6. Transaction with Embedded Category
**SQL Sources:** `transactions`, `transaction_categories` tables (JOIN)

#### Data Structure:
```json
{
  "transaction_id": 1,
  "sender_id": 1,
  "receiver_id": 2,
  "amount": 50000.00,
  "transaction_time": "2025-01-15T10:30:00Z",
  "category": {
    "category_id": 1,
    "category_type": "Money Transfer"
  }
}
```

#### Nesting Strategy:
- Base transaction data from `transactions` table
- `category_id` replaced with nested category object
- Reduces need for client to make additional API calls

---

## Complex Transaction Objects

### 7. Complete Transaction with All Related Data
**SQL Sources:** `transactions`, `user` (2x), `transaction_categories`, `system_logs` tables (multiple JOINs)

#### Data Structure:
```json
{
  "transaction_id": 1,
  "amount": 50000.00,
  "transaction_time": "2025-01-15T10:30:00Z",
  "sender": {
    "user_id": 1,
    "user_phone_number": "*********567",
    "user_name": "John Mukasa"
  },
  "receiver": {
    "user_id": 2,
    "user_phone_number": "*********667",
    "user_name": "Sarah Nakato"
  },
  "category": {
    "category_id": 1,
    "category_type": "Money Transfer"
  },
  "logs": [
    {
      "log_id": 1,
      "action": "Transaction Processed",
      "timestamp": "2025-01-15T10:30:05Z"
    }
  ]
}
```

#### Nesting Strategy:
- `sender_id` replaced with complete sender object (JOIN with `user` table)
- `receiver_id` replaced with complete receiver object (JOIN with `user` table)
- `category_id` replaced with complete category object
- `logs` array contains all system logs related to this transaction
- Maximum denormalization for complete transaction view

#### SQL Query:
```sql
SELECT 
    t.transaction_id,
    t.amount,
    t.transaction_time,
    -- Sender details
    sender.user_id AS sender_id,
    sender.user_phone_number AS sender_phone,
    sender.user_name AS sender_name,
    -- Receiver details
    receiver.user_id AS receiver_id,
    receiver.user_phone_number AS receiver_phone,
    receiver.user_name AS receiver_name,
    -- Category details
    tc.category_id,
    tc.category_type,
    -- Log details
    sl.log_id,
    sl.action,
    sl.timestamp AS log_timestamp
FROM transactions t
JOIN user sender ON t.sender_id = sender.user_id
JOIN user receiver ON t.receiver_id = receiver.user_id
JOIN transaction_categories tc ON t.category_id = tc.category_id
LEFT JOIN system_logs sl ON t.transaction_id = sl.transaction_id
WHERE t.transaction_id = 1;
```

---

<<<<<<< HEAD

### 6. Transaction with Embedded Category
**SQL Sources:** `transactions`, `transaction_categories` tables (JOIN)

#### Data Structure:
```json
{
  "transaction_id": 1,
  "sender_id": 1,
  "receiver_id": 2,
  "amount": 50000.00,
  "transaction_time": "2025-01-15T10:30:00Z",
  "category": {
    "category_id": 1,
    "category_type": "Money Transfer"
  }
}
```

#### Nesting Strategy:
- Base transaction data from `transactions` table
- `category_id` replaced with nested category object
- Reduces need for client to make additional API calls

---

## Complex Transaction Objects

### 7. Complete Transaction with All Related Data
**SQL Sources:** `transactions`, `user` (2x), `transaction_categories`, `system_logs` tables (multiple JOINs)

#### Data Structure:
```json
{
  "transaction_id": 1,
  "amount": 50000.00,
  "transaction_time": "2025-01-15T10:30:00Z",
  "sender": {
    "user_id": 1,
    "user_phone_number": "*********567",
    "user_name": "John Mukasa"
  },
  "receiver": {
    "user_id": 2,
    "user_phone_number": "*********667",
    "user_name": "Sarah Nakato"
  },
  "category": {
    "category_id": 1,
    "category_type": "Money Transfer"
  },
  "logs": [
    {
      "log_id": 1,
      "action": "Transaction Processed",
      "timestamp": "2025-01-15T10:30:05Z"
    }
  ]
}
```

#### Nesting Strategy:
- `sender_id` replaced with complete sender object (JOIN with `user` table)
- `receiver_id` replaced with complete receiver object (JOIN with `user` table)
- `category_id` replaced with complete category object
- `logs` array contains all system logs related to this transaction
- Maximum denormalization for complete transaction view

#### SQL Query:
```sql
SELECT 
    t.transaction_id,
    t.amount,
    t.transaction_time,
    -- Sender details
    sender.user_id AS sender_id,
    sender.user_phone_number AS sender_phone,
    sender.user_name AS sender_name,
    -- Receiver details
    receiver.user_id AS receiver_id,
    receiver.user_phone_number AS receiver_phone,
    receiver.user_name AS receiver_name,
    -- Category details
    tc.category_id,
    tc.category_type,
    -- Log details
    sl.log_id,
    sl.action,
    sl.timestamp AS log_timestamp
FROM transactions t
JOIN user sender ON t.sender_id = sender.user_id
JOIN user receiver ON t.receiver_id = receiver.user_id
JOIN transaction_categories tc ON t.category_id = tc.category_id
LEFT JOIN system_logs sl ON t.transaction_id = sl.transaction_id
WHERE t.transaction_id = 1;
```

---



=======
>>>>>>> 558925ddade7c50b52dbfb3250c02be2e2a7c170
## API Response Examples

### 8. Transaction List Response
**Use Case:** `GET /api/transactions` - Retrieve multiple transactions

#### Data Structure:
```json
{
  "status": "success",
  "count": 3,
  "page": 1,
  "total_pages": 1,
  "transactions": [
    {
      "transaction_id": 1,
      "amount": 50000.00,
      "transaction_time": "2025-01-15T10:30:00Z",
      "sender": {
        "user_id": 1,
        "user_name": "John Mukasa"
      },
      "receiver": {
        "user_id": 2,
        "user_name": "Sarah Nakato"
      },
      "category": {
        "category_type": "Money Transfer"
      }
    },
    {
      "transaction_id": 2,
      "amount": 25000.00,
      "transaction_time": "2025-01-15T14:20:00Z",
      "sender": {
        "user_id": 2,
        "user_name": "Sarah Nakato"
      },
      "receiver": {
        "user_id": 3,
        "user_name": "Peter Ochieng"
      },
      "category": {
        "category_type": "Money Transfer"
      }
    },
    {
      "transaction_id": 3,
      "amount": 10000.00,
      "transaction_time": "2025-01-16T09:15:00Z",
      "sender": {
        "user_id": 3,
        "user_name": "Peter Ochieng"
      },
      "receiver": {
        "user_id": 4,
        "user_name": "Mary Achieng"
      },
      "category": {
        "category_type": "Money Transfer"
      }
    }
  ]
}
```

#### Features:
- Wrapper object with metadata (`status`, `count`, `page`, `total_pages`)
- Array of transaction objects
- Partial nesting (user names included, but not full user objects)
- Optimized for list views in mobile apps

---

### 9. User Transaction History Response
**Use Case:** `GET /api/users/{user_id}/transactions` - Get all transactions for a specific user

#### Data Structure:
```json
{
  "status": "success",
  "user": {
    "user_id": 1,
    "user_phone_number": "*********567",
    "user_name": "John Mukasa"
  },
  "summary": {
    "total_sent": 50000.00,
    "total_received": 30000.00,
    "net_balance_change": -20000.00,
    "transaction_count": 2
  },
  "sent_transactions": [
    {
      "transaction_id": 1,
      "receiver": {
        "user_id": 2,
        "user_name": "Sarah Nakato"
      },
      "amount": 50000.00,
      "category": "Money Transfer",
      "transaction_time": "2025-01-15T10:30:00Z"
    }
  ],
  "received_transactions": [
    {
      "transaction_id": 5,
      "sender": {
        "user_id": 5,
        "user_name": "David Okello"
      },
      "amount": 30000.00,
      "category": "Money Transfer",
      "transaction_time": "2025-01-17T08:30:00Z"
    }
  ]
}
```

#### Features:
- User details at top level
- Computed summary statistics (totals, balance change, transaction count)
- Transactions separated by direction (sent vs received)
- Optimized for mobile wallet/history views

#### SQL Queries Required:

**Get sent transactions:**
```sql
SELECT * FROM transactions WHERE sender_id = 1;
```

**Get received transactions:**
```sql
SELECT * FROM transactions WHERE receiver_id = 1;
```

**Compute summary:**
```sql
SELECT 
    SUM(CASE WHEN sender_id = 1 THEN amount ELSE 0 END) AS total_sent,
    SUM(CASE WHEN receiver_id = 1 THEN amount ELSE 0 END) AS total_received,
    COUNT(*) AS transaction_count
FROM transactions 
WHERE sender_id = 1 OR receiver_id = 1;
```

---

<<<<<<< HEAD

=======
>>>>>>> 558925ddade7c50b52dbfb3250c02be2e2a7c170
## Summary

This documentation provides a complete reference for all JSON schema entities used throughout the Momo system, including:
- **Simple entities** with direct database mappings
- **Nested structures** that combine related data
- **Complex responses** with full denormalization for specific use cases
- **API endpoints** with their respective data formats and SQL queries

Each schema includes detailed information about data types, mapping strategies, and the underlying SQL queries used to construct the JSON responses.
