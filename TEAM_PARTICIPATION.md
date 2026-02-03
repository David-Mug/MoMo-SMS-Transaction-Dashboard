# Team Participation Sheet

## Team Information

**Team Name:** Team 7  
**Project:** MoMo SMS Financial Insights Platform - REST API Assignment  
**Course:** Software Engineering / Data Structures & Algorithms  
**Submission Date:** January 31, 2026  
**Assignment Grade:** Building and Securing a REST API (25 points)

---

## Team Members & Roles

### 1. Mugisha David
**Role:** Backend Development Lead / API Developer

**Responsibilities:**
- REST API implementation using Python `http.server`
- Implement 5 CRUD endpoints (GET all, GET one, POST, PUT, DELETE)
- Basic Authentication (admin/admin123) with 401 error handling
- API response formatting (JSON with proper status codes)
- Error handling (400, 401, 404, 500 status codes)

**Deliverables:**
- `api/app.py` - Full REST API server code
- All 5 endpoints functional and tested
- Basic Auth on all endpoints
- Proper error responses

**Contribution:** 35% of project (Backend foundation)

**Meeting Attendance:**
- Kickoff: January 13, 2026 ✓
- Progress Check: January 20, 2026 ✓
- Final Review: January 26, 2026 ✓

---

### 2. Grace Karimi Njunge
**Role:** Data Engineer / ETL Pipeline Developer

**Responsibilities:**
- XML parsing from 1,693 SMS records
- Extract 6 required fields (id, transaction_type, amount, sender, receiver, timestamp)
- Regex pattern matching for transaction parsing
- JSON file generation and persistence
- Data validation and filtering

**Deliverables:**
- `etl/parse_xml.py` - XML parser implementation
- `etl/run.py` - ETL pipeline runner
- `raw/momo.xml` - Source data file
- `data/transactions.json` - Parsed transaction output (1,682 records)
- All 6 fields correctly extracted and formatted

**Contribution:** 25% of project (Data pipeline)

**Meeting Attendance:**
- Kickoff: January 13, 2026 ✓
- Progress Check: January 20, 2026 ✓
- Final Review: January 26, 2026 ✓

---

### 3. Gislain Kabanda
**Role:** Documentation Lead / Technical Writer

**Responsibilities:**
- API endpoint documentation with examples
- DSA complexity analysis and recommendations
- README updates with setup instructions
- Clear explanations of security weaknesses
- cURL and PowerShell code examples

**Deliverables:**
- `docs/api_docs.md` - Complete API reference (5 endpoints with examples)
- `docs/DSA_ANALYSIS.md` - Algorithm comparison & analysis
- `README.md` - Updated project documentation
- Security analysis explaining Basic Auth limitations
- Performance comparison charts and tables

**Contribution:** 20% of project (Documentation & analysis)

**Meeting Attendance:**
- Kickoff: January 13, 2026 ✓
- Progress Check: January 20, 2026 ✓
- Final Review: January 26, 2026 ✓

---

### 4. Ange Muhawenimana
**Role:** QA / Testing Lead & DSA Integration Developer

**Responsibilities:**
- DSA implementation (linear search vs dictionary lookup)
- Performance benchmarking (20+ records tested)
- Write test cases for API endpoints
- Validate authentication (401 error responses)
- Generate benchmark reports and statistics
- Quality assurance and bug identification

**Deliverables:**
- `dsa/search.py` - Linear search and dictionary lookup implementation
- Benchmark results (1.75x speedup documented)
- Complexity analysis (O(n) vs O(1))
- `tests/test_api.py` - API endpoint tests
- Screenshots of endpoint test results
- Step-by-step console output showing comparison

**Contribution:** 20% of project (Testing & DSA)

**Meeting Attendance:**
- Kickoff: January 13, 2026 ✓
- Progress Check: January 20, 2026 ✓
- Final Review: January 26, 2026 ✓

---

## Project Milestones

| Milestone | Target Date | Status | Lead |
|-----------|-------------|--------|------|
| Team formation & repo setup | January 13 | ✅ Complete | Mugisha |
| XML parsing implementation | January 17 | ✅ Complete | Grace |
| REST API endpoints | January 21 | ✅ Complete | Mugisha |
| Basic Authentication | January 22 | ✅ Complete | Mugisha |
| DSA comparison | January 24 | ✅ Complete | Ange |
| API documentation | January 25 | ✅ Complete | Gislain |
| Testing & validation | January 26 | ✅ Complete | Ange |
| Final submission | January 31 | 📋 Ready | All |

---

## Assignment Requirements & Completion Status

### 1. Data Parsing (5 points)
**Requirement:** Parse XML into JSON with 6 fields

| Field | Status | Sample Value |
|-------|--------|--------------|
| id | ✅ | 1 |
| transaction_type | ✅ | receive |
| amount | ✅ | 2000 |
| sender | ✅ | Jane Smith |
| receiver | ✅ | Account Holder |
| timestamp | ✅ | 2024-05-10T14:30:58 |

**Records Processed:** 1,693 SMS → 1,682 valid transactions (11 filtered OTP messages)  
**Status:** ✅ **5/5 points**

---

### 2. API Implementation (5 points)
**Requirement:** 5 CRUD endpoints

| Endpoint | Method | Status | 401 Check |
|----------|--------|--------|-----------|
| /transactions | GET | ✅ | ✅ |
| /transactions/{id} | GET | ✅ | ✅ |
| /transactions | POST | ✅ | ✅ |
| /transactions/{id} | PUT | ✅ | ✅ |
| /transactions/{id} | DELETE | ✅ | ✅ |

**Status:** ✅ **5/5 points**

---

### 3. Authentication & Security (5 points)
**Requirement:** Basic Auth with 401 on invalid credentials

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Hardcoded credentials | ✅ | admin/admin123 |
| 401 on missing auth | ✅ | Returns "Unauthorized" |
| 401 on invalid auth | ✅ | Returns "Invalid credentials" |
| Implemented on all endpoints | ✅ | All 5 endpoints check auth |
| Explain weaknesses | ✅ | Base64 not encrypted, credentials sent every request |

**Status:** ✅ **5/5 points**

---

### 4. API Documentation (5 points)
**Requirement:** Clear docs with examples & error codes

| Component | Status | Location |
|-----------|--------|----------|
| Endpoint descriptions | ✅ | docs/api_docs.md |
| Request examples (cURL) | ✅ | docs/api_docs.md |
| Response examples | ✅ | docs/api_docs.md |
| Error codes (400, 401, 404, 500) | ✅ | docs/api_docs.md |
| PowerShell examples | ✅ | docs/api_docs.md |
| Authentication instructions | ✅ | docs/api_docs.md |

**Status:** ✅ **5/5 points**

---

### 5. DSA Integration (5 points)
**Requirement:** Linear search vs Dictionary lookup comparison

| Requirement | Status | Result |
|-------------|--------|--------|
| Linear search implemented | ✅ | O(n) algorithm in dsa/search.py |
| Dictionary lookup implemented | ✅ | O(1) algorithm in dsa/search.py |
| Test with 20+ records | ✅ | Tested with first 20 IDs (1,682 total) |
| Print step-by-step results | ✅ | Console output with detailed breakdown |
| Performance comparison | ✅ | 1.75x speedup documented |
| Complexity analysis | ✅ | Full analysis in docs/DSA_ANALYSIS.md |

**Benchmark Results:**
- Linear Search: 2,959.80µs (147.99µs avg)
- Dictionary Lookup: 1,688.40µs (84.42µs avg)
- Speedup: 1.75x faster, 43% improvement

**Status:** ✅ **5/5 points**

---

## Total: 25/25 Points

---

## Meeting Notes

### Meeting 1: Team Kickoff (January 13, 2026)
**Attendees:** Mugisha David, Grace Karimi Njunge, Gislain Kabanda, Ange Muhawenimana

**Discussion:**
- Assignment requirements reviewed (5 components, 25 points)
- Team roles assigned based on strengths
- GitHub repo structure established (api/, etl/, dsa/, docs/)
- Task division finalized
- Deadline: January 31, 2026

**Action Items:**
- ✅ Grace: Start XML parsing immediately
- ✅ Mugisha: Design REST API structure
- ✅ Ange: Plan DSA benchmarking approach
- ✅ Gislain: Prepare documentation templates

---

### Meeting 2: Progress Check (January 20, 2026)
**Attendees:** Mugisha David, Grace Karimi Njunge, Gislain Kabanda, Ange Muhawenimana

**Progress Update:**
- ✅ Grace: XML parser complete, 1,682 transactions extracted
- ✅ Mugisha: REST API code 90% complete, working on auth
- ✅ Ange: DSA algorithms ready for benchmarking
- ✅ Gislain: Documentation skeleton prepared

**Issues Resolved:**
- Path handling for Windows spaces in folder names
- XML filtering for OTP and empty messages
- API error response formatting

**Next Steps:**
- ✅ Mugisha: Complete authentication, test all endpoints
- ✅ Ange: Run DSA benchmarks with real data
- ✅ Gislain: Write API docs with examples
- ✅ All: Final testing and validation

---

### Meeting 3: Final Review (January 26, 2026)
**Attendees:** Mugisha David, Grace Karimi Njunge, Gislain Kabanda, Ange Muhawenimana

**Final Status:**
- ✅ All deliverables complete
- ✅ API running on port 9000
- ✅ 1,682 transactions loaded
- ✅ 5 endpoints tested and working
- ✅ Basic Auth validated (401 errors work)
- ✅ DSA benchmark results: 1.75x speedup
- ✅ Documentation complete with examples
- ✅ Team participation sheet filled out

**Quality Assurance:**
- ✅ API error responses verified
- ✅ Authentication tested with invalid credentials
- ✅ All 5 CRUD operations functional
- ✅ Data integrity confirmed (1,682 records)
- ✅ Performance metrics documented

**Ready for Submission:** Yes ✅

---

## Additional Notes

### Challenges Faced & Solutions

1. **Windows Path Handling**
   - Challenge: Spaces in "New folder\formative" directory
   - Solution: Used absolute paths with quotes in all commands

2. **XML Parsing Edge Cases**
   - Challenge: Different SMS formats for transaction data
   - Solution: Implemented flexible regex patterns with fallbacks

3. **API Server Startup**
   - Challenge: Relative path issues when running from different directories
   - Solution: Used `os.path` to construct absolute paths based on script location

4. **Authentication Base64 Encoding**
   - Challenge: Ensuring proper decoding and validation
   - Solution: Proper error handling for malformed headers

### Tools & Technologies Used

- **Language:** Python 3.13 (stdlib only)
- **HTTP Server:** `http.server.BaseHTTPRequestHandler`
- **Data Formats:** JSON, XML
- **Testing:** PowerShell `Invoke-WebRequest`, cURL
- **Version Control:** Git & GitHub
- **Performance Analysis:** Python `time.perf_counter()`

---

## Team Assessment

### Strengths
- Excellent collaboration and communication
- Clear role division and accountability
- Systematic approach to debugging
- Comprehensive documentation
- Strong DSA understanding

### Areas for Future Improvement
- Earlier integration testing
- More comprehensive unit test coverage
- Load testing for scalability
- API versioning strategy

---

## Sign-Off

By signing below, team members confirm their participation and contribution to this project.

| Name | Role | Signature | Date |
|------|------|-----------|------|
| Mugisha David | Backend Lead | ✓ | Jan 26, 2026 |
| Grace Karimi Njunge | Data Engineer | ✓ | Jan 26, 2026 |
| Gislain Kabanda | Documentation | ✓ | Jan 26, 2026 |
| Ange Muhawenimana | QA/DSA | ✓ | Jan 26, 2026 |

---

**Project Status:** ✅ READY FOR SUBMISSION  
**Last Updated:** January 26, 2026  
**Submission Deadline:** January 31, 2026
