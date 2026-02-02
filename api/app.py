"""
REST API Server using http.server with Basic Authentication
Endpoints:
  GET    /transactions          - Get all transactions
  GET    /transactions/{id}     - Get single transaction
  POST   /transactions          - Create new transaction
  PUT    /transactions/{id}     - Update transaction
  DELETE /transactions/{id}     - Delete transaction
"""

import json
import base64
import re
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime

# Global transactions
TRANSACTIONS = []

# Auth credentials
AUTH_USERNAME = "admin"
AUTH_PASSWORD = "admin123"


class TransactionHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API"""
    
    def do_GET(self):
        """Handle GET requests"""
        if not self._check_auth():
            return
        
        path = urlparse(self.path).path
        
        # GET /transactions/{id}
        match = re.match(r'^/transactions/(\d+)$', path)
        if match:
            tx_id = int(match.group(1))
            return self._get_transaction(tx_id)
        
        # GET /transactions
        if path == '/transactions':
            return self._get_all_transactions()
        
        self._send_json(404, {"error": "Not Found"})
    
    def do_POST(self):
        """Handle POST requests"""
        if not self._check_auth():
            return
        
        path = urlparse(self.path).path
        
        if path == '/transactions':
            return self._create_transaction()
        
        self._send_json(404, {"error": "Not Found"})
    
    def do_PUT(self):
        """Handle PUT requests"""
        if not self._check_auth():
            return
        
        path = urlparse(self.path).path
        
        match = re.match(r'^/transactions/(\d+)$', path)
        if match:
            tx_id = int(match.group(1))
            return self._update_transaction(tx_id)
        
        self._send_json(404, {"error": "Not Found"})
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if not self._check_auth():
            return
        
        path = urlparse(self.path).path
        
        match = re.match(r'^/transactions/(\d+)$', path)
        if match:
            tx_id = int(match.group(1))
            return self._delete_transaction(tx_id)
        
        self._send_json(404, {"error": "Not Found"})
    
    def _check_auth(self):
        """Verify Basic Authentication"""
        auth_header = self.headers.get('Authorization', '')
        
        if not auth_header.startswith('Basic '):
            self._send_json(401, {"error": "Unauthorized", "message": "Missing Authorization header"})
            return False
        
        try:
            encoded = auth_header[6:]
            decoded = base64.b64decode(encoded).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            if username == AUTH_USERNAME and password == AUTH_PASSWORD:
                return True
            else:
                self._send_json(401, {"error": "Unauthorized", "message": "Invalid credentials"})
                return False
        except:
            self._send_json(401, {"error": "Unauthorized", "message": "Invalid Authorization header"})
            return False
    
    def _get_all_transactions(self):
        """GET /transactions - Return all transactions"""
        self._send_json(200, {"count": len(TRANSACTIONS), "data": TRANSACTIONS})
    
    def _get_transaction(self, tx_id):
        """GET /transactions/{id} - Return single transaction"""
        for tx in TRANSACTIONS:
            if tx['id'] == tx_id:
                return self._send_json(200, tx)
        
        self._send_json(404, {"error": "Not Found", "message": f"Transaction {tx_id} not found"})
    
    def _create_transaction(self):
        """POST /transactions - Create new transaction"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            payload = json.loads(body)
            
            # Validate required fields
            required = ['transaction_type', 'amount', 'sender', 'receiver']
            for field in required:
                if field not in payload:
                    return self._send_json(400, {"error": "Bad Request", "message": f"Missing field: {field}"})
            
            # Generate new ID
            new_id = max([tx['id'] for tx in TRANSACTIONS], default=0) + 1
            
            # Create transaction
            transaction = {
                'id': new_id,
                'transaction_type': payload['transaction_type'],
                'amount': payload['amount'],
                'sender': payload['sender'],
                'receiver': payload['receiver'],
                'timestamp': datetime.now().isoformat()
            }
            
            TRANSACTIONS.append(transaction)
            self._send_json(201, {"message": "Transaction created", "data": transaction})
        
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Bad Request", "message": "Invalid JSON"})
        except Exception as e:
            self._send_json(500, {"error": "Server Error", "message": str(e)})
    
    def _update_transaction(self, tx_id):
        """PUT /transactions/{id} - Update transaction"""
        try:
            # Find transaction
            transaction = None
            for tx in TRANSACTIONS:
                if tx['id'] == tx_id:
                    transaction = tx
                    break
            
            if not transaction:
                return self._send_json(404, {"error": "Not Found", "message": f"Transaction {tx_id} not found"})
            
            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            payload = json.loads(body)
            
            # Update fields
            updateable = ['transaction_type', 'amount', 'sender', 'receiver']
            for field in updateable:
                if field in payload:
                    transaction[field] = payload[field]
            
            self._send_json(200, {"message": "Transaction updated", "data": transaction})
        
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Bad Request", "message": "Invalid JSON"})
        except Exception as e:
            self._send_json(500, {"error": "Server Error", "message": str(e)})
    
    def _delete_transaction(self, tx_id):
        """DELETE /transactions/{id} - Delete transaction"""
        global TRANSACTIONS
        
        for i, tx in enumerate(TRANSACTIONS):
            if tx['id'] == tx_id:
                deleted = TRANSACTIONS.pop(i)
                return self._send_json(200, {"message": "Transaction deleted", "data": deleted})
        
        self._send_json(404, {"error": "Not Found", "message": f"Transaction {tx_id} not found"})
    
    def _send_json(self, status_code, data):
        """Send JSON response"""
        response = json.dumps(data, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Custom logging"""
        auth = self.headers.get('Authorization', 'No Auth')
        if auth.startswith('Basic '):
            auth = '[Auth]'
        print(f"[{self.log_date_time_string()}] {self.client_address[0]} {self.command} {self.path} - {auth}")


def load_transactions(json_file):
    """Load transactions from JSON file"""
    global TRANSACTIONS
    try:
        with open(json_file, 'r') as f:
            TRANSACTIONS = json.load(f)
        print(f"✓ Loaded {len(TRANSACTIONS)} transactions")
    except FileNotFoundError:
        print(f"✗ {json_file} not found")
        TRANSACTIONS = []
    except json.JSONDecodeError:
        print(f"✗ Invalid JSON in {json_file}")
        TRANSACTIONS = []


def run_server(host='localhost', port = 8000):
    """Run HTTP server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, TransactionHandler)
    
    print("\n" + "="*70)
    print("REST API SERVER")
    print("="*70)
    print(f"\nServer: http://{host}:{port}")
    print(f"Transactions: {len(TRANSACTIONS)} loaded")
    print(f"Auth: Basic (admin/admin123)")
    print("\nEndpoints:")
    print(f"  GET    /transactions         - Get all")
    print(f"  GET    /transactions/{{id}}    - Get one")
    print(f"  POST   /transactions         - Create")
    print(f"  PUT    /transactions/{{id}}    - Update")
    print(f"  DELETE /transactions/{{id}}    - Delete")
    print("\nPress Ctrl+C to stop")
    print("="*70 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        httpd.server_close()


if __name__ == '__main__':
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file = os.path.join(base_dir, 'data', 'transactions.json')
    load_transactions(json_file)
    run_server()
