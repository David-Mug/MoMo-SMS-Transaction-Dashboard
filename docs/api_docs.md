# REST API Documentation

## Overview
This REST API provides CRUD operations for Mobile Money (MoMo) transactions. It uses HTTP methods (GET, POST, PUT, DELETE) with JSON request/response format and Basic Authentication for security.

**Base URL:** `http://localhost:8000`

**Authentication:** Basic Auth (username: `admin`, password: `admin123`)

---

## Authentication

### Basic Authentication
All endpoints require Basic Authentication. Include the `Authorization` header with Base64-encoded credentials.

**Format:**
```
Authorization: Basic base64(username:password)
```

**Example (admin/admin123):**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

**Response on Missing/Invalid Auth (401):**
```json
{
  "error": "Unauthorized"
}
```

---

## Endpoints

### 1. GET /transactions
Retrieve all transactions

**Method:** `GET`

**URL:** `http://localhost:8000/transactions`

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "transaction_type": "received",
    "amount": 2000,
    "sender": "Jane Smith",
    "receiver": "Account Holder",
    "readable_date": "2024-05-10"
  },
  {
    "id": 2,
    "transaction_type": "transfer",
    "amount": 5000,
    "sender": "Account Holder",
    "receiver": "John Doe",
    "readable_date": "2024-05-10"
  }
]
```

**cURL Example:**
```bash
curl -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     http://localhost:8000/transactions
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-WebRequest -Uri "http://localhost:8000/transactions" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json
```

---

### 2. GET /transactions/{id}
Retrieve a single transaction by ID

**Method:** `GET`

**URL:** `http://localhost:8000/transactions/{id}`

**Parameters:**
- `id` (path parameter, required): Transaction ID (integer)

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": 1,
  "transaction_type": "received",
  "amount": 2000,
  "sender": "Jane Smith",
  "receiver": "Account Holder",
  "readable_date": "2024-05-10"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**cURL Example:**
```bash
curl -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     http://localhost:8000/transactions/1
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-WebRequest -Uri "http://localhost:8000/transactions/1" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json
```

---

### 3. POST /transactions
Create a new transaction

**Method:** `POST`

**URL:** `http://localhost:8000/transactions`

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Request Body:**
```json
{
  "transaction_type": "transfer",
  "amount": 50000,
  "sender": "Account Holder",
  "receiver": "Bob Wilson",
  "readable_date": "2024-05-20"
}
```

**Required Fields:**
- `transaction_type` (string): Type of transaction (payment, received, deposit, transfer)
- `amount` (number): Transaction amount
- `sender` (string or null): Sender name
- `receiver` (string or null): Receiver name
- `readable_date` (string): Date in YYYY-MM-DD format

**Validation Rules:**
- `payment`: sender must be null, receiver must be valid string
- `received`: receiver must be null, sender must be valid string
- `deposit`: both sender and receiver must be null
- `transfer`: both sender and receiver must be valid strings

**Response (201 Created):**
```json
{
  "message": "Transaction created successfully! Transaction id is 1683"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing field: readable_date"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/transactions \
     -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     -H "Content-Type: application/json" \
     -d '{
       "transaction_type": "transfer",
       "amount": 50000,
       "sender": "Account Holder",
       "receiver": "Bob Wilson",
       "readable_date": "2024-05-20"
     }'
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
$body = @{
    transaction_type = "transfer"
    amount = 50000
    sender = "Account Holder"
    receiver = "Bob Wilson"
    readable_date = "2024-05-20"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/transactions" `
                  -Method POST `
                  -Headers @{"Authorization"="Basic $auth"} `
                  -Body $body `
                  -ContentType "application/json"
```

---

### 4. PUT /transactions/{id}
Update an existing transaction

**Method:** `PUT`

**URL:** `http://localhost:8000/transactions/{id}`

**Parameters:**
- `id` (path parameter, required): Transaction ID to update

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Request Body (partial update):**
```json
{
  "amount": 75000,
  "receiver": "Alice Johnson"
}
```

**Updateable Fields:**
- `transaction_type`
- `amount`
- `sender`
- `receiver`
- `readable_date`

**Validation Rules:** Same as POST - validates transaction type constraints on update

**Response (200 OK):**
```json
{
  "id": 1,
  "transaction_type": "received",
  "amount": 75000,
  "sender": "Jane Smith",
  "receiver": "Alice Johnson",
  "readable_date": "2024-05-10"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**cURL Example:**
```bash
curl -X PUT http://localhost:8000/transactions/1 \
     -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     -H "Content-Type: application/json" \
     -d '{
       "amount": 75000,
       "receiver": "Alice Johnson"
     }'
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
$body = @{
    amount = 75000
    receiver = "Alice Johnson"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/transactions/1" `
                  -Method PUT `
                  -Headers @{"Authorization"="Basic $auth"} `
                  -Body $body `
                  -ContentType "application/json"
```

---

### 5. DELETE /transactions/{id}
Delete a transaction

**Method:** `DELETE`

**URL:** `http://localhost:8000/transactions/{id}`

**Parameters:**
- `id` (path parameter, required): Transaction ID to delete

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Response (204 No Content):**
No response body - HTTP 204 indicates successful deletion

**Response (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/transactions/1 \
     -H "Authorization: Basic YWRtaW46YWRtaW4xMjM="
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-WebRequest -Uri "http://localhost:8000/transactions/1" `
                  -Method DELETE `
                  -Headers @{"Authorization"="Basic $auth"}
```

---

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Successful GET, PUT request |
| 201 | Created | Successful POST request |
| 204 | No Content | Successful DELETE request |
| 400 | Bad Request | Invalid JSON or missing required fields |
| 401 | Unauthorized | Missing or invalid authentication |
| 404 | Not Found | Transaction ID does not exist |
| 500 | Server Error | Internal server error |

---

## Data Model

### Transaction Object
```json
{
  "id": 1,
  "transaction_type": "received",
  "amount": 2000,
  "sender": "Jane Smith",
  "receiver": "Account Holder",
  "readable_date": "2024-05-10"
}
```

**Fields:**
- `id` (integer): Unique transaction identifier (auto-generated)
- `transaction_type` (string): Type of transaction
  - `received` - Money received
  - `transfer` - Money transferred
  - `payment` - Payment made
  - `deposit` - Deposit made
- `amount` (number): Transaction amount in RWF
- `sender` (string or null): Name of transaction sender
- `receiver` (string or null): Name of transaction receiver
- `readable_date` (string): Date in YYYY-MM-DD format

---

## Testing the API

### Quick Test Script (PowerShell)
```powershell
# Set up authentication
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))

# Test 1: Get all transactions
Write-Host "Test 1: GET /transactions"
Invoke-WebRequest -Uri "http://localhost:8000/transactions" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json | Select -First 2

# Test 2: Get single transaction
Write-Host "`nTest 2: GET /transactions/1"
Invoke-WebRequest -Uri "http://localhost:8000/transactions/1" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json

# Test 3: Create new transaction
Write-Host "`nTest 3: POST /transactions"
$body = @{transaction_type="transfer"; amount=10000; sender="Test"; receiver="User"; readable_date="2024-05-20"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/transactions" -Method POST `
                  -Headers @{"Authorization"="Basic $auth"} `
                  -Body $body -ContentType "application/json" | ConvertFrom-Json

# Test 4: Test auth failure
Write-Host "`nTest 4: GET /transactions (no auth)"
Try {
    Invoke-WebRequest -Uri "http://localhost:8000/transactions" 2>&1
} Catch {
    $_.Exception.Response.StatusCode
}
```

---

## Running the API

**Start the server:**
```bash
cd MoMo-SMS-Financial-Insights-Platform
python api/app.py
```

**Expected output:**
```
Server running at http://localhost:8000
```

---

## API Implementation Details

- **Framework:** Python `http.server` (stdlib only)
- **Port:** 8000
- **Format:** JSON request/response
- **Data Storage:** In-memory list (populated from XML file)
- **Authentication:** Basic Auth (Base64 encoded)
- **Endpoints:** 5 CRUD operations

---

## Security Considerations

### Current Implementation (Development Only)
- Basic Authentication implemented
- 401 Unauthorized response on missing/invalid credentials
- **NOT PRODUCTION READY** - credentials hardcoded and sent in Base64
- No HTTPS/TLS encryption
- No rate limiting
- No input validation/sanitization

### For Production Use
- Use HTTPS/TLS encryption
- Implement JWT tokens instead of Basic Auth
- Add rate limiting and request throttling
- Validate and sanitize all inputs
- Use environment variables for credentials
- Implement logging and monitoring
- Add CORS headers if needed
- Use a proper database instead of in-memory storage

---

## Support

For issues or questions, contact the development team:
- Backend: Mugisha David, Kabanda Gislain
- API Lead: Mugisha David

Last Updated: February 05, 2026

## Overview
This REST API provides CRUD operations for Mobile Money (MoMo) transactions. It uses HTTP methods (GET, POST, PUT, DELETE) with JSON request/response format and Basic Authentication for security.

**Base URL:** `http://localhost:8000`

**Authentication:** Basic Auth (username: `admin`, password: `admin123`)

---

## Authentication

### Basic Authentication
All endpoints require Basic Authentication. Include the `Authorization` header with Base64-encoded credentials.

**Format:**
```
Authorization: Basic base64(username:password)
```

**Example (admin/admin123):**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

**Response on Missing/Invalid Auth (401):**
```json
{
  "error": "Unauthorized"
}
```

---

## Endpoints

### 1. GET /transactions
Retrieve all transactions

**Method:** `GET`

**URL:** `http://localhost:8000/transactions`

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "transaction_type": "received",
    "amount": 2000,
    "sender": "Jane Smith",
    "receiver": "Account Holder",
    "readable_date": "2024-05-10"
  },
  {
    "id": 2,
    "transaction_type": "transfer",
    "amount": 5000,
    "sender": "Account Holder",
    "receiver": "John Doe",
    "readable_date": "2024-05-10"
  }
]
```

**cURL Example:**
```bash
curl -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     http://localhost:9000/transactions
```

**PowerShell Example:*8
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-WebRequest -Uri "http://localhost:8000/transactions" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json
```

---

### 2. GET /transactions/{id}
Retrieve a single transaction by ID

**Method:** `GET`

**URL:** `http://localhost:8000/transactions/{id}`

**Parameters:**
- `id` (path parameter, required): Transaction ID (integer)

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": 1,
  "transaction_type": "received",
  "amount": 2000,
  "sender": "Jane Smith",
  "receiver": "Account Holder",
  "readable_date": "2024-05-10"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**cURL Example:**
```bash
curl -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     http://localhost:8000/transactions/1
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-WebRequest -Uri "http://localhost:8000/transactions/1" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json
```

---

### 3. POST /transactions
Create a new transaction

**Method:** `POST`

**URL:** `http://localhost:9000/transactions`
8000/transactions`

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Request Body:**
```json
{
  "transaction_type": "transfer",
  "amount": 50000,
  "sender": "Account Holder",
  "receiver": "Bob Wilson",
  "readable_date": "2024-05-20"
}
```

**Required Fields:**
- `transaction_type` (string): Type of transaction (payment, received, deposit, transfer)
- `amount` (number): Transaction amount
- `sender` (string or null): Sender name
- `receiver` (string or null): Receiver name
- `readable_date` (string): Date in YYYY-MM-DD format

**Validation Rules:**
- `payment`: sender must be null, receiver must be valid string
- `received`: receiver must be null, sender must be valid string
- `deposit`: both sender and receiver must be null
- `transfer`: both sender and receiver must be valid strings

**Response (201 Created):**
```json
{
  "message": "Transaction created successfully! Transaction id is 1683"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing field: readable_date
```

**cURL Example:**
```bash
curl -X POST http://localhost:9000/transactions \
     -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     -H "Content-Type: application/json" \
     -d '{
       "transaction_type": "tr8000/transactions \
     -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     -H "Content-Type: application/json" \
     -d '{
       "transaction_type": "transfer",
       "amount": 50000,
       "sender": "Account Holder",
       "receiver": "Bob Wilson",
       "readable_date": "2024-05-20"
     }'
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
$body = @{
    transaction_type = "transfer"
    amount = 50000
    sender = "Account Holder"
    receiver = "Bob Wilson"
    readable_date = "2024-05-20"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8n/json"
```

---

### 4. PUT /transactions/{id}
Update an existing transaction

**Method:** `PUT`

**URL:** `http://localhost:9000/transactions/{id}`

**Parameters:**8000/transactions/{id}`

**Parameters:**
- `id` (path parameter, required): Transaction ID to update

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Request Body (partial update):**
```json
{
  "amount": 75000,
  "receiver": "Alice Johnson"
}
```

**Updateable Fields:**
- `transaction_type`
- `amount`
- `sender`
- `receiver`
- `readable_date`

**Validation Rules:** Same as POST - validates transaction type constraints on update

**Response (200 OK):**
```json
{
  "id": 1,
  "transaction_type": "received",
  "amount": 75000,
  "sender": "Jane Smith",
  "receiver": "Alice Johnson",
  "readable_date": "2024-05-10"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**cURL Example:**
```bash
curl -X PUT http://localhost:8000/transactions/1 \
     -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
     -H "Content-Type: application/json" \
     -d '{
       "amount": 75000,
       "receiver": "Alice Johnson"
     }'
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
$body = @{
    amount = 75000
    receiver = "Alice Johnson"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8n"="Basic $auth"} `
                  -Body $body `
                  -ContentType "application/json"
```

---

### 5. DELETE /transactions/{id}
Delete a transaction

**Method:** `DELETE`

**URL:** `http://localhost:9000/transactions/{id}`

**Parameters:**
- `id` (path parameter, req8000/transactions/{id}`

**Parameters:**
- `id` (path parameter, required): Transaction ID to delete

**Headers:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json
```

**Response (204 No Content):**
No response body - HTTP 204 indicates successful deletion

**Response (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/transactions/1 \
     -H "Authorization: Basic YWRtaW46YWRtaW4xMjM="
```

**PowerShell Example:**
```powershell
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-WebRequest -Uri "http://localhost:8

---

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Successful GET, PUT request |
| 201 | Created | Successful POST request |
| 400 | Bad Request | Invalid JSON or missing required fields |
| 401 | Unauthorized | Missing or invalid authentication |
| 404 | Not Found | Transaction ID does not exist |
| 500 | Server Error | Internal server error |

---

## Data Model

### Transaction Object
```json
{
  "id": 1,
  "transaction_type": "receive",
  "amount": 2000,
  "sender": "Jane Smith",
  "receiver": "Account Holder",
  "timestamp": "2024-05-10T14:30:58.724000"
}
```

**Fields:**
- `id` (integer): Unique transaction identifier (auto-generated)
- `transaction_type` (string): Type of transaction
  - `receive` - Money received
  - `transfer` - Money transferred
  - `payment` - Payment made
  - `deposit` - Deposit made
  - `withdrawal` - Withdrawal d",
  "amount": 2000,
  "sender": "Jane Smith",
  "receiver": "Account Holder",
  "readable_date": "2024-05-10"
}
```

**Fields:**
- `id` (integer): Unique transaction identifier (auto-generated)
- `transaction_type` (string): Type of transaction
  - `received` - Money received
  - `transfer` - Money transferred
  - `payment` - Payment made
  - `deposit` - Deposit made
- `amount` (number): Transaction amount in RWF
- `sender` (string or null): Name of transaction sender
- `receiver` (string or null): Name of transaction receiver
- `readable_date` (string): Date in YYYY-MM-DD format
# Test 2: Get single transaction
Write-Host "`nTest 2: GET /transactions/1"
Invoke-WebRequest -Uri "http://localhost:9000/transactions/1" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json

# Test 3: Create new transaction
Write-Host "`nTest 3: POST /transactions"
$body = @{transaction_type="transfer"; amount=10000; sender="Test"; receiver="User"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:9000/transactions" -Method POST `
                  -Headers @{"Authorization"="Basic $auth"} `
                  -Body $body -ContentType "application/json" | ConvertFrom-Json
8000/transactions" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json | Select -First 2

# Test 2: Get single transaction
Write-Host "`nTest 2: GET /transactions/1"
Invoke-WebRequest -Uri "http://localhost:8000/transactions/1" `
                  -Headers @{"Authorization"="Basic $auth"} | ConvertFrom-Json

# Test 3: Create new transaction
Write-Host "`nTest 3: POST /transactions"
$body = @{transaction_type="transfer"; amount=10000; sender="Test"; receiver="User"; readable_date="2024-05-20"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/transactions" -Method POST `
                  -Headers @{"Authorization"="Basic $auth"} `
                  -Body $body -ContentType "application/json" | ConvertFrom-Json

# Test 4: Test auth failure
Write-Host "`nTest 4: GET /transactions (no auth)"
Try {
    Invoke-WebRequest -Uri "http://localhost:8

**Expected output:**
```
 Loaded 1682 transactions

======================================================================
REST API SERVER
======================================================================

Server: http://localhost:9000
Transactions: 1682 loaded
Auth: Basic (admin/admin123)

Endpoints:
  GET    /transactions         - Get all
  GET    /transactions/{id}    - Get one
  POST   /transactions         - Create
Server running at http://localhost:8000

## Security Considerations

### Current Implementation (Development Only)
-  Basic Authentication implemented
-  401 Unauthorized response on missing/invalid credentials
-  **NOT PRODUCTION READY** - credentials hardcoded and sent in Base64
-  No HTTPS/TLS encryption
-  No rate limiting
-  No input validation/sanitization

### For Production Use
- Use HTTPS/TLS encryption
- Implement JWT tokens instead of Basic Auth
- Add rate limiting and request throttling
- Validate and sanitize all inputs
- Use environment variables for credentials
- Implement logging and monitoring
- Add CORS headers if needed
- Use a proper database instead of JSON files

---

## Support

For issues or questions, contact the development team:
- Backend: Mugisha David, Kabanda Gislain
- API Lead: Mugisha David

Last Updated: February 02, 2026
