# Import required libraries

from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import json
import sys
import os

sys.path.append("../dsa")  # Add the 'dsa' directory to the system path to allow import of the parsed data
from xml_parser import parse_xml

#construct path to the xml file
xml_path = os.path.join("..", "dsa", "modified_sms_V2.xml")
transactions = parse_xml(xml_path)  # Parse the XML file to get transactions

PORT = 8000 #Define port number

# This class tells Python how to respond to HTTP requests
# Every request sent to the server is handled here
class RequestHandler(BaseHTTPRequestHandler):

    #helper method to set HTTP headers
    def _set_headers(self, status=200):
        # Send an HTTP status code back to the client
        self.send_response(status)

        # Tell the client that our response is JSON data
        self.send_header("Content-Type", "application/json")

        # End the HTTP headers section
        self.end_headers()

    VALID_USERNAME = "group7"
    VALID_PASSWORD = "EWD"

    def _check_auth(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            return False
        
        # Get Base64 part
        encoded = auth_header.split(' ')[1]
        try:
            decoded = base64.b64decode(encoded).decode('utf-8')  # "username:password"
        except Exception:
            return False

        username, password = decoded.split(':')
        if username == self.VALID_USERNAME and password == self.VALID_PASSWORD:
            return True
        return False


    def do_GET(self):
        if not self._check_auth():
            self._set_headers(401)  # Unauthorized
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8'))
            return
        try:
            if self.path == "/transactions":
                self._set_headers(200)
                self.wfile.write(json.dumps(transactions).encode('utf-8'))
            elif self.path.startswith("/transactions/"):
                try:
                    #getting the transaction id from the url
                    trans_id = int(self.path.split("/")[-1])
                except ValueError:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "The transaction ID provided is invalid"}).encode('utf-8'))
                    return

                #Finding transaction based on ids
                trans = next((t for t in transactions if t["id"]==trans_id), None)
            
                if trans is None:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Transaction not found"}).encode('utf-8'))
                else:
                    self._set_headers(200)
                    self.wfile.write(json.dumps(trans).encode('utf-8'))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Endpoint provided was not found"}).encode('utf-8'))
        except BrokenPipeError:
            pass  # ignore broken pipe errors when client disconnects
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Server error", "details": str(e)}).encode('utf-8'))
    
    # Handle POST requests to add new transactions
    def do_POST(self):
        if not self._check_auth():
            self._set_headers(401)  # Unauthorized
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8'))
            return
        # Check if the URL is correct
        if self.path != "/transactions":
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))
            return

        try:
            # Read the JSON body from the client
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Define the fields we allow
            required_fields = ["transaction_type", "amount", "receiver",  "sender", "readable_date"]

            # Check that required fields exist
            for field in required_fields:
                if field not in data:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": f"Missing field: {field}"}).encode('utf-8'))
                    return

            # Check data types
            if not isinstance(data["amount"], (int, float)):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Amount must be a number"}).encode('utf-8'))
                return

            # Filter out unwanted fields
            transaction_to_store = {key: data[key] for key in required_fields if key in data}

            # Generate a new unique ID
            if transactions:
                new_id = max(t["id"] for t in transactions) + 1
            else:
                new_id = 1  # first transaction
            transaction_to_store["id"] = new_id

            # Append the transaction to the list
            transactions.append(transaction_to_store)

            # Respond to client
            self._set_headers(201)  # Created
            self.wfile.write(json.dumps(transaction_to_store).encode('utf-8'))

        except json.JSONDecodeError:
            # Invalid JSON from client
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode('utf-8'))

        except Exception as e:
            # Catch all other errors
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Internal Server Error", "details": str(e)}).encode('utf-8'))
    
    def do_PUT(self):
        #adding auth
        if not self._check_auth():
            self._set_headers(401)  # Unauthorized
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8'))
            return
        
        if not self.path.startswith("/transactions/"):
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))
            return

        try:
            txn_id = int(self.path.split("/")[-1])
            txn = next((t for t in transactions if t["id"] == txn_id), None)
            if not txn:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode('utf-8'))
                return

            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            updates = json.loads(body)

            # Update only fields provided
            for key, value in updates.items():
                txn[key] = value

            self._set_headers(200)
            self.wfile.write(json.dumps(txn).encode('utf-8'))

        except ValueError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid transaction ID"}).encode('utf-8'))
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Internal Server Error", "details": str(e)}).encode('utf-8'))

    # Handle DELETE requests according to the id provided.
    def do_DELETE(self):
        #adding auth
        if not self._check_auth():
            self._set_headers(401)  # Unauthorized
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8'))
            return

        if not self.path.startswith("/transactions/"):
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))
            return

        try:
            txn_id = int(self.path.split("/")[-1])
            index = next((i for i, t in enumerate(transactions) if t["id"] == txn_id), None)
            if index is None:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode('utf-8'))
                return

            transactions.pop(index)
            self._set_headers(204)  # No Content
            self.wfile.write(b'')

        except ValueError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid transaction ID"}).encode('utf-8'))
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Internal Server Error", "details": str(e)}).encode('utf-8'))
#Running the server
def run(PORT=8000):

    # Create an HTTP server instance
    server = HTTPServer(("", PORT), RequestHandler)

    # Print a message so we know the server is running
    print(f"Server running at http://localhost:{PORT}")

    # Keep the server running until it is force stoppen with CTRL+C
    server.serve_forever()

# This ensures the server only starts when this file is run directly
if __name__ == "__main__":
    run()