"""
Patient Health Monitoring System - Web Dashboard Server
=======================================================
A lightweight local web server to run the interactive Patient Health Dashboard.
Uses Python standard library (http.server) — no extra dependencies needed!

Usage:
    python web_dashboard.py
    (Automatically opens http://127.0.0.1:5000 in your browser)
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time

PORT = 5000
HOST = "127.0.0.1"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable aggressive caching for live demo
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[{time.strftime('%H:%M:%S')}] HTTP: {format % args}\n")

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer((HOST, PORT), CustomHandler) as httpd:
        url = f"http://{HOST}:{PORT}/index.html"
        print("\n" + "=" * 60)
        print("  PATIENT HEALTH MONITORING SYSTEM — LIVE WEB DASHBOARD")
        print("=" * 60)
        print(f"  ✓ Local Server Active at : {url}")
        print(f"  ✓ Standalone HTML File   : index.html / dashboard.html")
        print("  ✓ Press Ctrl+C in terminal to stop server.")
        print("=" * 60 + "\n")
        
        # Open in default browser after 1 second
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Shutting down live web dashboard server.")

if __name__ == "__main__":
    run_server()
