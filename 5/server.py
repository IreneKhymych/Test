import http.server
import os
from http.server import HTTPServer, CGIHTTPRequestHandler

PORT = 8000

class CustomHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_name = "localhost"  # ✅ Додаємо `server_name`

class MyHandler(CGIHTTPRequestHandler):
    cgi_directories = ["/cgi-bin"]

with CustomHTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
