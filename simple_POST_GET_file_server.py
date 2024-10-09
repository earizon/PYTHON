#!/usr/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import urlparse
from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()

    def do_GET(self):
        parsedQuery = urlparse(self.path)
        if parsedQuery.path != "/api/v1/state":
            self.send_error(404)
        self._set_headers()
        query = parsedQuery.query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        filepath = query_components["filepath"]
        with open(filepath) as f1:
          json = f1.read()   
        self.wfile.write(bytes(json, "utf-8"))

    def do_POST(self):
        parsedQuery = urlparse(self.path)
        if parsedQuery.path != "/api/v1/state":
            self.send_error(404)
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        query = parsedQuery.query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        filepath = query_components["filepath"]
        with open(filepath, 'w') as f1:
            f1.write(body)
        self._set_headers()
        self.wfile.write(bytes(body,'utf-8'))
        

httpd = HTTPServer(('localhost', 8002), SimpleHTTPRequestHandler)
httpd.serve_forever()
