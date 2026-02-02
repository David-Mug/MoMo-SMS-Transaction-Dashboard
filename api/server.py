# Import required libraries

from http.server import BaseHTTPRequestHandler, HTTPServer
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

    def do_GET(self):
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
    def do_POST(self):
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