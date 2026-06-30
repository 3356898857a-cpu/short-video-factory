#!/usr/bin/env python3
"""Local CORS Proxy - Run this on your Mac, keep it running.
   Browser calls localhost:8765 → forwards to TikHub → returns data to browser.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json

class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length else b'{}'
        target_url = self.path.lstrip('/')
        if not target_url:
            self.send_json(400, {'error': 'Missing URL in path'})
            return

        req = urllib.request.Request(target_url, data=body, method='POST')
        for key, val in self.headers.items():
            if key.lower() not in ('host', 'origin', 'referer'):
                req.add_header(key, val)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Headers', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass  # quiet

print('🔀 本地代理启动: http://localhost:8765')
print('   转发目标: TikHub API')
print('   保持此窗口打开，不要关闭')
print('   按 Ctrl+C 停止')
HTTPServer(('127.0.0.1', 8765), ProxyHandler).serve_forever()
