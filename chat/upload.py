# backend/server.py

import http.server
import socketserver
import sys
import os
import cgi

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.gene_predict import run_prediction

PORT = 8000

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/predict':
            self.send_error(404, "Not Found")
            return

        # 解析 multipart/form-data 请求
        content_type = self.headers.get('Content-Type')
        if not content_type or not content_type.startswith('multipart/form-data'):
            self.send_error(400, "Invalid Content-Type")
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        gene_name = form.getvalue('geneName', '').strip()
        if not gene_name:
            self.send_error(400, "Missing or empty geneName")
            return
        if not all(c.isalnum() or c in {'-', '_'} for c in gene_name):
            self.send_error(400, "Invalid geneName format")
            return

        try:
            output = run_prediction(gene_name)
        except Exception as e:
            output = f"Prediction failed: {str(e)}"

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(output.encode('utf-8'))


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer is shutting down...")
            httpd.server_close()
