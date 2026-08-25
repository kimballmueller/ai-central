#!/usr/bin/env python3
"""Review server that never caches — so what you see is always what's on disk.
Usage:  python3 _build/serve.py [port]      (default 8901)"""
import sys, os, functools, http.server, socketserver

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()
    def log_message(self, *a): pass

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8901
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", port), functools.partial(NoCache, directory=ROOT)) as httpd:
    print(f"Sublime Personnel prototype -> http://localhost:{port}  (no-cache)")
    httpd.serve_forever()
