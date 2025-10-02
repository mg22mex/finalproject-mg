#!/usr/bin/env python3
import http.server
import socketserver
import os
import urllib.parse

class ReactRouterHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # If it's a file that exists, serve it normally
        if os.path.exists(path[1:]) and not path.endswith('/'):
            super().do_GET()
            return
        
        # For React Router routes, serve index.html
        if path.startswith('/vehicles') or path.startswith('/photos') or path.startswith('/facebook') or path.startswith('/settings'):
            self.path = '/index.html'
            super().do_GET()
            return
        
        # For root and other routes, serve index.html
        if path == '/' or not os.path.exists(path[1:]):
            self.path = '/index.html'
            super().do_GET()
            return
        
        # Default behavior for other files
        super().do_GET()

if __name__ == "__main__":
    PORT = 5173
    Handler = ReactRouterHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Serving React app with client-side routing on port {PORT}")
        print(f"📱 Frontend: http://localhost:{PORT}")
        print("🔄 Press Ctrl+C to stop")
        httpd.serve_forever()
