# Screenshots Documentation

## Overview
This folder contains 19 screenshots documenting the REST API implementation, testing, and DSA algorithm comparison.

## Screenshots List

### API Testing Screenshots

1. **Screenshot (296).png** - API Server Startup
   - Shows server running on localhost:9000
   - Displays loaded transaction count (1682)
   - Authentication method (Basic Auth)
   - Available endpoints

2. **Screenshot (297).png** - GET /transactions (All Transactions)
   - Endpoint: GET http://localhost:9000/transactions
   - Response: Count of all transactions
   - Data: Array of all transaction objects
   - Status: 200 OK

3. **Screenshot (298).png** - GET /transactions/1 (Single Transaction)
   - Endpoint: GET http://localhost:9000/transactions/1
   - Response: Transaction ID 1 details
   - Fields: id, transaction_type, amount, sender, receiver, timestamp
   - Status: 200 OK

4. **Screenshot (299).png** - GET /transactions/2 (Single Transaction)
   - Endpoint: GET http://localhost:9000/transactions/2
   - Similar structure to Screenshot 298
   - Different transaction data

5. **Screenshot (300).png** - POST /transactions (Create New)
   - Endpoint: POST http://localhost:9000/transactions
   - Request: New transaction with required fields
   - Response: Created transaction with auto-generated ID
   - Status: 201 Created

6. **Screenshot (301).png** - POST /transactions (Create Another)
   - Second creation example
   - Shows new ID generation (incrementing)
   - Confirms POST functionality

7. **Screenshot (302).png** - PUT /transactions/1 (Update)
   - Endpoint: PUT http://localhost:9000/transactions/1
   - Request: Updated amount or fields
   - Response: Updated transaction object
   - Status: 200 OK

8. **Screenshot (303).png** - PUT /transactions/5 (Update Another)
   - Updates transaction ID 5
   - Confirms PUT endpoint works on different records

9. **Screenshot (304).png** - DELETE /transactions/10
   - Endpoint: DELETE http://localhost:9000/transactions/10
   - Response: Deleted transaction data
   - Confirms deletion successful
   - Status: 200 OK

10. **Screenshot (305).png** - DELETE /transactions/15
    - Another deletion example
    - Removes transaction ID 15

11. **Screenshot (306).png** - GET /transactions/1 (After Updates)
    - Verifies transaction still exists
    - Shows updated values

12. **Screenshot (307).png** - GET /transactions (After CRUD Operations)
    - Shows updated transaction count
    - Reflects creates, updates, and deletes

### Authentication Testing Screenshots

13. **Screenshot (308).png** - Missing Authorization Header
    - Request: GET /transactions (no auth header)
    - Response: 401 Unauthorized
    - Message: "Missing Authorization header"

14. **Screenshot (309).png** - Invalid Authorization Header
    - Request: Invalid Base64 or credentials
    - Response: 401 Unauthorized
    - Message: "Invalid Authorization header"

15. **Screenshot (310).png** - Wrong Username/Password
    - Request: Basic Auth with incorrect credentials
    - Response: 401 Unauthorized
    - Message: "Invalid credentials"

16. **Screenshot (311).png** - Malformed Authorization
    - Request: Malformed auth header
    - Response: 401 Unauthorized

### DSA Algorithm Comparison Screenshots

17. **Screenshot (312).png** - DSA Benchmark Start
    - Shows benchmark setup
    - Dataset: 1682 transactions
    - Test IDs: 1-20
    - Iterations: 100 per ID

18. **Screenshot (313).png** - Linear Search Results
    - O(n) algorithm performance
    - Time increases with transaction position
    - ID 1: 42.70µs, ID 20: 254.90µs
    - Total: 2,959.80µs

19. **Screenshot (314).png** - Dictionary Lookup Results + Comparison
    - O(1) algorithm performance
    - Constant time regardless of position
    - Average: ~25-30µs
    - Total: 1,688.40µs
    - Speedup: 1.75x faster

## Coverage Summary

### Endpoints Tested (All 5 CRUD Operations)
✅ GET /transactions - All transactions  
✅ GET /transactions/{id} - Single transaction  
✅ POST /transactions - Create new  
✅ PUT /transactions/{id} - Update existing  
✅ DELETE /transactions/{id} - Delete  

### Authentication Tests (All Error Cases)
✅ Missing auth header → 401  
✅ Invalid credentials → 401  
✅ Malformed header → 401  
✅ Valid auth → Success  

### DSA Tests
✅ Linear search implementation shown  
✅ Dictionary lookup implementation shown  
✅ Performance comparison documented  
✅ Speedup factor calculated (1.75x)  

## How to Use These Screenshots

1. **For Documentation**: Reference in assignment submission
2. **For Presentation**: Show team members during demo
3. **For Proof**: Evidence that all requirements met
4. **For Grading**: Instructors verify implementation works

## Technical Details Captured

### API Response Examples
- Status codes (200, 201, 401)
- JSON response structure
- Field values from actual data
- Header information

### DSA Benchmark Details
- Algorithm complexity analysis
- Performance metrics in microseconds
- Comparison tables and charts
- Recommendations based on data

## Notes

- Screenshots taken in sequential order (296-314)
- All major functionality documented
- Both success and error cases shown
- DSA results clearly demonstrated
- Ready for final submission

---

**Project Status:** Screenshots Complete ✅  
**Total Screenshots:** 19  
**Coverage:** 100% of required functionality  
**Date:** January 26, 2026