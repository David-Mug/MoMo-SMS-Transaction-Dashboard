# Import required libraries

from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import json
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Absolute path to dsa directory
DSA_DIR = os.path.join(BASE_DIR, "..", "dsa")
# Add dsa directory to Python path
sys.path.append(DSA_DIR)

from xml_parser import parse_xml

#absolute path to the xml file
xml_path = os.path.join(DSA_DIR, "modified_sms_V2.xml")

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

    VALID_USERNAME = "admin"
    VALID_PASSWORD = "admin123"

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
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8')+ b"\n")
            return
        try:
            if self.path == "/transactions":
                self._set_headers(200)
                self.wfile.write(json.dumps(transactions).encode('utf-8')+ b"\n")
            elif self.path.startswith("/transactions/"):
                try:
                    #getting the transaction id from the url
                    trans_id = int(self.path.split("/")[-1])
                except ValueError:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "The transaction ID provided is invalid"}).encode('utf-8')+ b"\n")
                    return

                #Finding transaction based on ids
                trans = next((t for t in transactions if t["id"]==trans_id), None)
            
                if trans is None:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Transaction not found"}).encode('utf-8')+ b"\n")
                else:
                    self._set_headers(200)
                    self.wfile.write(json.dumps(trans).encode('utf-8')+ b"\n")
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Endpoint provided was not found"}).encode('utf-8')+ b"\n")
        except BrokenPipeError:
            pass  # ignore broken pipe errors when client disconnects
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Server error", "details": str(e)}).encode('utf-8')+ b"\n")
    
    # Handle POST requests to add new transactions
    def do_POST(self):
        if not self._check_auth():
            self._set_headers(401)  # Unauthorized
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8')+ b"\n")
            return
        # Check if the URL is correct
        if self.path != "/transactions":
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8')+ b"\n")
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
                    self.wfile.write(json.dumps({"error": f"Missing field: {field}"}).encode('utf-8')+ b"\n")
                    return
            trans_type = data["transaction_type"]
            sender = data["sender"]
            receiver = data["receiver"]

            # Helper function
            def is_valid_string(value):
                return isinstance(value, str) and value.strip()

            if trans_type == "payment":
                # sender must be null, receiver must be present
                if sender is not None:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Payment transactions must have a null sender"
                    }).encode("utf-8"))
                    return

                if not is_valid_string(receiver):
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Payment transactions must have a valid receiver"
                    }).encode("utf-8"))
                    return

            elif trans_type == "received":
                # receiver must be null, sender must be present
                if receiver is not None:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Received transactions must have a null receiver"
                    }).encode("utf-8"))
                    return

                if not is_valid_string(sender):
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Received transactions must have a valid sender"
                    }).encode("utf-8"))
                    return

            elif trans_type == "deposit":
                # both must be null
                if sender is not None or receiver is not None:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Deposit transactions must have null sender and receiver"
                    }).encode("utf-8"))
                    return

            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "error": f"Unsupported transaction type: {trans_type}"
                }).encode("utf-8"))
                return

            # Check data types
            if not isinstance(data["amount"], (int, float)):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Amount must be a number"}).encode('utf-8')+ b"\n")
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
            self.wfile.write(json.dumps({"message": f"Transaction created successfully! Transaction id is{new_id}"}).encode('utf-8')+ b"\n")

        except json.JSONDecodeError:
            # Invalid JSON from client
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode('utf-8')+ b"\n")

        except Exception as e:
            # Catch all other errors
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Internal Server Error", "details": str(e)}).encode('utf-8')+ b"\n")
    
    def do_PUT(self):
        #adding auth
        if not self._check_auth():
            self._set_headers(401)  # Unauthorized
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8')+ b"\n")
            return
        
        if not self.path.startswith("/transactions/"):
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8')+ b"\n")
            return

        try:
            trans_id = int(self.path.split("/")[-1])
            trans = next((t for t in transactions if t["id"] == trans_id), None)
            if not trans:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode('utf-8')+ b"\n")
                return

            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            updates = json.loads(body)
                        # Helper function
            def is_valid_string(value):
                return isinstance(value, str) and value.strip()

            updated_trans = trans.copy()
            updated_trans.update(updates)

            trans_type = updated_trans.get("transaction_type")
            sender = updated_trans.get("sender")
            receiver = updated_trans.get("receiver")

            if trans_type == "payment":
                if sender is not None:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Payment transactions must have a null sender"
                    }).encode("utf-8"))
                    return

                if not is_valid_string(receiver):
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Payment transactions must have a valid receiver"
                    }).encode("utf-8"))
                    return

            elif trans_type == "received":
                if receiver is not None:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Received transactions must have a null receiver"
                    }).encode("utf-8"))
                    return

                if not is_valid_string(sender):
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Received transactions must have a valid sender"
                    }).encode("utf-8"))
                    return

            elif trans_type == "deposit":
                if sender is not None or receiver is not None:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "error": "Deposit transactions must have null sender and receiver"
                    }).encode("utf-8"))
                    return

            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "error": f"Unsupported transaction type: {trans_type}"
                }).encode("utf-8"))
                return

            # Update only fields provided
            for key, value in updates.items():
                trans[key] = value

            self._set_headers(200)
            self.wfile.write(json.dumps(trans).encode('utf-8')+ b"\n")

        except ValueError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid transaction ID"}).encode('utf-8')+ b"\n")
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Internal Server Error", "details": str(e)}).encode('utf-8')+ b"\n")

    # Handle DELETE requests according to the id provided.
    def do_DELETE(self):
        #adding auth
        if not self._check_auth():
            self._set_headers(401)  # Unauthorized
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8')+ b"\n")
            return

        if not self.path.startswith("/transactions/"):
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8')+ b"\n")
            return

        try:
            trans_id = int(self.path.split("/")[-1])
            index = next((i for i, t in enumerate(transactions) if t["id"] == trans_id), None)
            if index is None:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode('utf-8')+ b"\n")
                return

            transactions.pop(index)
            self._set_headers(204)  # No Content
            self.wfile.write(b'')

        except ValueError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid transaction ID"}).encode('utf-8')+ b"\n")
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Internal Server Error", "details": str(e)}).encode('utf-8')+ b"\n")
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