
#!/usr/bin/env python3
"""An example HTTP server with GET and POST endpoints."""
import argparse
import os
import pickle
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import picker
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time

class _RequestHandler(BaseHTTPRequestHandler):
    # Borrowing from https://gist.github.com/nitaku/10d0662536f37a087e1b
    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        filename = "nba-player.csv"
        with open(os.path.join(".", "data", filename), "rb") as f:
            ratings = pd.read_csv(f,names=("player","salary","team","position","team-agaisnt","ceiling","floor","points"))
        model = picker.NBAPicker()
        team = model.pick(ratings)
        result = team.to_json()
        parsed = json.loads(result)
        self._set_headers()
        self.wfile.write(json.dumps(parsed).encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        message['date_ms'] = int(time.time()) * 1000
        _g_posts.append(message)
        self._set_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

    def do_OPTIONS(self):
        # Send allow-origin header for preflight POST XHRs.
        self.send_response(HTTPStatus.NO_CONTENT.value)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()


def run_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()