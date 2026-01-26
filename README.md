Team Excel Sheet - https://docs.google.com/spreadsheets/d/1gd4ohovlVMZiL2MNFqg6Jvo51dRFk4IUx_4-Ghn_Be0/edit?gid=0#gid=0

Progress tracking and task management Trello board: https://trello.com/b/vEybE1aY/momo-transaction-analytics-scrum-board

System design diagrams and technical architecture: https://drive.google.com/file/d/1goYUlZVnnQKxRoBbOAGn26IHWoS1l4j5/view?usp=sharing

Interactive diagram editor: https://app.diagrams.net/#G1goYUlZVnnQKxRoBbOAGn26IHWoS1l4j5


# MoMo SMS Financial Insights Platform

## Overview

The MoMo SMS Financial Insights Platform is a comprehensive full-stack application designed to process, analyze, and visualize Mobile Money transaction data. The system extracts financial transaction information from SMS messages in XML format, performs data validation and cleansing, stores the information in a relational database, and provides business intelligence through an interactive web-based dashboard.

This project demonstrates professional software engineering practices including ETL (Extract, Transform, Load) pipeline design, relational database modeling, and full-stack application development.

## Team Members

- Mugisha David
- Grace Karimi Njunge
- Gislain Kabanda
- Ange Muhawenimana

## Project Objectives

- Extract structured financial transaction data from unstructured SMS messages
- Implement data validation and cleansing processes to ensure data quality
- Design a normalized relational database for efficient data storage and retrieval
- Build a responsive web interface for transaction analysis and reporting
- Provide real-time and historical financial insights to users
- Maintain comprehensive audit logs for system transparency and compliance

## Technology Stack

- **Backend Framework**: Python with FastAPI for RESTful API development
- **Data Processing**: ElementTree and lxml libraries for XML parsing and manipulation
- **Database**: SQLite with optimized schema design and indexing
- **Frontend**: HTML5, CSS3, and vanilla JavaScript for responsive user interface
- **Version Control**: Git and GitHub for collaborative development
- **Documentation**: Markdown with comprehensive API and database schema documentation

## Project Structure

```
MoMo-SMS-Financial-Insights-Platform/
├── dsa/
│   └── xml_parser.py           # XML parsing and data extraction module
├── database/
│   └── database_setup.sql      # Complete database schema and seed data
├── documents/
│   └── JSON_SCHEMAS_GUIDE.md   # API data structures and specifications
├── modified_sms_v2.xml         # Sample SMS transaction data in XML format
├── README.md                   # This file
└── .git/                       # Version control repository

```

## Database Schema

The system uses a normalized relational database with the following core tables:

### User Table
Stores information about Mobile Money account holders.

```sql
CREATE TABLE user (
    user_id INT PRIMARY KEY,
    user_phone_number VARCHAR(20),
    user_name VARCHAR(50)
);
```

**Purpose**: Identifies transaction participants
**Fields**:
- `user_id`: Unique user identifier (auto-incremented)
- `user_phone_number`: Masked phone number for privacy
- `user_name`: Full name of the account holder

### Transaction Categories Table
Defines types of Mobile Money transactions.

```sql
CREATE TABLE transaction_categories (
    category_id INT PRIMARY KEY,
    category_type VARCHAR(50) NOT NULL
);
```

**Purpose**: Classifies different transaction types
**Supported Categories**:
- Money Transfer
- Airtime Purchase
- Bill Payment
- Cash Withdrawal
- Cash Deposit

### Transactions Table
Core table storing all Mobile Money transaction records.

```sql
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    category_id INT NOT NULL,
    transaction_time DATETIME NOT NULL
);
```

**Purpose**: Records all financial transactions
**Fields**:
- `transaction_id`: Unique transaction identifier
- `sender_id`: User initiating the transaction (foreign key)
- `receiver_id`: User receiving the transaction (foreign key)
- `amount`: Transaction amount in currency units
- `category_id`: Transaction type classification (foreign key)
- `transaction_time`: Timestamp of transaction occurrence

**Constraints**:
- Amount must be greater than zero
- Sender and receiver must be different users
- Foreign key constraints ensure referential integrity

**Performance Indexes**:
- `idx_sender`: Fast lookup by sender
- `idx_receiver`: Fast lookup by receiver
- `idx_category`: Fast lookup by category
- `idx_transaction_time`: Fast time-based queries

### System Logs Table
Maintains audit trail for all system operations.

```sql
CREATE TABLE system_logs (
    log_id INT PRIMARY KEY,
    action VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL,
    transaction_id INT,
    category_id INT
);
```

**Purpose**: Tracks data processing events and transactions
**Fields**:
- `log_id`: Unique log entry identifier
- `action`: Description of the operation performed
- `timestamp`: When the action occurred
- `transaction_id`: Associated transaction (optional)
- `category_id`: Associated category (optional)

### User Categories Junction Table
Maps users to their associated transaction categories.

```sql
CREATE TABLE user_categories (
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (user_id, category_id)
);
```

**Purpose**: Defines which transaction types each user can perform
**Relationship**: Many-to-many relationship between users and categories

## System Architecture

### ETL Pipeline

The system implements a complete Extract, Transform, Load pipeline:

1. **Extract**: XML parser reads Mobile Money SMS data files
   - Parses XML structure to identify transaction records
   - Extracts relevant fields from each transaction
   - Validates XML format and structure

2. **Transform**: Data cleansing and validation
   - Standardizes phone numbers and user information
   - Validates transaction amounts and dates
   - Categorizes transactions based on transaction type
   - Handles missing or invalid data

3. **Load**: Database insertion with error handling
   - Establishes database connections
   - Inserts processed records into appropriate tables
   - Maintains referential integrity
   - Logs all operations for audit purposes

### Data Flow

```
SMS XML Files
     |
     v
XML Parser (xml_parser.py)
     |
     v
Data Validation & Cleansing
     |
     v
Database Storage (SQLite)
     |
     v
Web Dashboard & Reports
```

## Installation

### Prerequisites

- Python 3.8 or higher
- SQLite 3
- Basic command line knowledge

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/your-repo/MoMo-SMS-Financial-Insights-Platform.git
cd MoMo-SMS-Financial-Insights-Platform
```

2. Create and activate a Python virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install required dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
sqlite3 momo_db.db < database/database_setup.sql
```

5. Run the XML parser to load sample data
```bash
python dsa/xml_parser.py modified_sms_v2.xml
```

## Usage

### Processing SMS Data

To process new SMS transaction files:

```bash
python dsa/xml_parser.py path/to/your/sms_data.xml
```

The parser will:
- Read the XML file
- Extract transaction information
- Validate data integrity
- Insert records into the database
- Generate processing logs

### Running the Web Dashboard

```bash
python main.py
```

Access the dashboard at http://localhost:8000

### Using the API

If FastAPI is enabled, access the interactive API documentation:

```
http://localhost:8000/docs
```

## Key Features

### Data Processing

- Reads and parses Mobile Money SMS data in XML format
- Handles multiple transaction types and categories
- Implements comprehensive error handling
- Validates data before database insertion
- Supports batch processing of multiple files

### Database

- Normalized schema prevents data redundancy
- Strategic indexing for optimal query performance
- Referential integrity through foreign keys
- Audit logging for compliance and debugging
- Support for complex analytical queries

### Dashboard

- Real-time transaction monitoring
- Category-based transaction filtering
- User performance analytics
- Date range-based reporting
- Visual representations of financial data

### Security

- Phone number masking for privacy protection
- Input validation to prevent SQL injection
- Audit logs for transaction accountability
- Data integrity constraints at database level

## API Documentation

For detailed API endpoint specifications, request/response formats, and data schemas, refer to [JSON_SCHEMAS_GUIDE.md](documents/JSON_SCHEMAS_GUIDE.md).

### Core Data Structures

**User Object**
```json
{
  "user_id": 1,
  "user_phone_number": "*********567",
  "user_name": "John Mukasa"
}
```

**Transaction Object**
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

**Transaction Category Object**
```json
{
  "category_id": 1,
  "category_type": "Money Transfer"
}
```

## Development


### Version Control Workflow

1. Create feature branch from main
2. Implement changes with descriptive commits
3. Push to remote and create pull request
4. Code review and testing
5. Merge to main after approval

## Documentation Files

- **JSON_SCHEMAS_GUIDE.md**: Complete API data structure specifications including all entity schemas, data types, and mapping strategies
- **MOMO DATABASE DESIGN DOCUMENT**: Comprehensive database design rationale and normalization decisions
- **AI Usage Log**: Project development notes and AI-assisted implementation records

## Performance Considerations

### Database Optimization

- Indexed columns for common query patterns
- Proper normalization to minimize data redundancy
- Composite primary keys for junction tables
- Foreign key constraints for referential integrity

### XML Processing

- Streaming XML parsing for large files
- Batch processing capabilities
- Error recovery mechanisms
- Transaction rollback on validation failure

## Troubleshooting

### Common Issues

**Database Connection Errors**
- Verify SQLite installation
- Check file permissions on database directory
- Ensure database initialization completed successfully

**XML Parsing Errors**
- Validate XML file structure
- Check for encoding issues (UTF-8 recommended)
- Verify element and attribute names match schema

**Data Validation Failures**
- Review error logs for specific validation issues
- Check phone number format
- Verify transaction amounts are positive numbers
- Ensure sender and receiver are different users

## Future Enhancements

- Real-time data streaming capabilities
- Machine learning for fraud detection
- Advanced analytics and predictive insights
- Multi-currency support
- Mobile application interface
- Enhanced reporting and export capabilities

## License

This project is developed as part of a software engineering course project.

## Contact and Support

For questions or issues, contact the development team through the project Trello board or GitHub repository issues section.

---

Last Updated: January 2026
