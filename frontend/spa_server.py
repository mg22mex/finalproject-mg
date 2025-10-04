#!/usr/bin/env python3
import http.server
import socketserver
import os
from urllib.parse import urlparse

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # If it's an API call, let it through
        if path.startswith('/api/'):
            super().do_GET()
            return
            
        # If it's a file that exists, serve it
        if os.path.exists('.' + path) and path != '/':
            super().do_GET()
            return
            
        # For all other routes, serve index.html (SPA routing)
        self.path = '/index.html'
        super().do_GET()

if __name__ == "__main__":
    PORT = 3000
    os.chdir('dist')
    with socketserver.TCPServer(("", PORT), SPAHandler) as httpd:
        print(f"SPA Server running on port {PORT}")
        httpd.serve_forever()
