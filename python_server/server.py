import json, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type
from uuid import uuid4


# Define the request handler class by extending BaseHTTPRequestHandler.
# This class will handle HTTP requests that the server receives.
class SimpleRequestHandler(BaseHTTPRequestHandler):
    user_list = [{
        'first_name': 'Michal',
        'last_name': 'Mucha',
        'role': 'instructor',
        'id': f'{uuid4()}'
    }]

    # Handle OPTIONS requests (used in CORS preflight checks).
    # CORS (Cross-Origin Resource Sharing) is a mechanism that allows restricted resources
    # on a web page to be requested from another domain outside the domain from which the resource originated.
    def do_OPTIONS(self):
        # Send a 200 OK response to acknowledge the request was processed successfully.
        self.send_response(200, "OK")

        # Set headers to indicate that this server allows any origin (*) to access its resources.
        # This is important for browsers when making cross-origin requests.
        self.send_header("Access-Control-Allow-Origin", "*")

        # Specify the allowed HTTP methods that can be used in the actual request.
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

        # Indicate what request headers are allowed (e.g., Content-Type for JSON requests).
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        # End headers and complete the response
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/":
            self.get_html()
        elif self.path == "/data":
            self.get_data()
        elif self.path == "/styles.css":
            self.get_css()
        elif self.path == "/logic.js":
            self.get_js()

    def get_html(self) -> None:
        filepath = os.path.join(os.path.dirname(__file__), '../nginx/ui_app/index.html')

        try:
            with open(filepath, 'r') as index_file:
                html_content = index_file.read().encode('utf-8')

            self.send_response(200)

            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(html_content)
        except:
            self.send_error(404, "File not found")

    def get_css(self) -> None:
        filepath = os.path.join(os.path.dirname(__file__), '../nginx/ui_app/styles.css')

        try:
            with open(filepath, 'rb') as index_file:
                css_content = index_file.read()

            self.send_response(200)

            self.send_header('Content-type', 'text/css')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(css_content)
        except:
            self.send_error(404, "File not found")

    def get_js(self) -> None:
        filepath = os.path.join(os.path.dirname(__file__), '../nginx/ui_app/logic.js')

        try:
            with open(filepath, 'rb') as index_file:
                js_content = index_file.read()

            self.send_response(200)

            self.send_header('Content-type', 'application/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(js_content)
        except:
            self.send_error(404, "File not found")

    def get_data(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(SimpleRequestHandler.user_list, default = str).encode('utf-8'))

    # Handle POST requests.
    # This method is called when the client sends a POST request.
    def do_POST(self) -> None:
        content_type = self.headers.get('Content-Type')
        if content_type == 'application/json':
            content_length = int(self.headers['Content-Length'])  # Get the size of data
            post_data = self.rfile.read(content_length)  # Read the POST data
            
            try:
                # Decode the JSON data
                received_data = json.loads(post_data.decode('utf-8'))

                privacy_policy_accepted = received_data["privacy_policy"] == "on"
                correct_role = received_data['role'] in ["Manager", "Development Lead", "Product Designer", "CTO"]
                
                if privacy_policy_accepted and correct_role:
                    SimpleRequestHandler.user_list.append({
                        'first_name': received_data["first_name"],
                        'last_name': received_data["last_name"],
                        'role': received_data["role"],
                        'id': str(uuid4())
                    })

                self.send_response(200)
                self.end_headers()
            
            except json.JSONDecodeError:
                # Handle JSON decoding error
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid JSON')
        else:
            # If content type is not JSON, send an error
            self.send_response(415)
            self.end_headers()
            self.wfile.write(b'Unsupported Media Type')

    def do_DELETE(self):
        # Delete a user based on the id from the URL (e.g., /delete/6aa9f6eb-f154-4153-bbd1-db16207c561b)
        try:
            user_id = self.path.split('/')[-1]  # Get the id from the URL
            if any(user.get('id', None) ==  user_id for user in SimpleRequestHandler.user_list):
                for user in SimpleRequestHandler.user_list:
                    if user.get('id', None) == user_id:
                        index = SimpleRequestHandler.user_list.index(user)
                        del SimpleRequestHandler.user_list[index]  # Remove the user at the specified id
                self.send_response(200)
            else:
                self.send_response(404)

        except ValueError:
            self.send_response(400)  # Invalid id format

        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

# Function to start the server.
# It takes parameters to specify the server class, handler class, and port number.
def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    # Define the server address.
    # '' means it will bind to all available network interfaces on the machine, and the port is specified.
    server_address: tuple = ('', port)

    # Create an instance of HTTPServer with the specified server address and request handler.
    httpd: HTTPServer = server_class(server_address, handler_class)

    # Print a message to the console indicating that the server is starting and which port it will listen on.
    print(f"Starting HTTP server on port {port}...")

    # Start the server and make it continuously listen for requests.
    # This method will block the program and keep running until interrupted.
    httpd.serve_forever()


# If this script is executed directly (not imported as a module), this block runs.
# It calls the `run()` function to start the server.
if __name__ == '__main__':
    run()