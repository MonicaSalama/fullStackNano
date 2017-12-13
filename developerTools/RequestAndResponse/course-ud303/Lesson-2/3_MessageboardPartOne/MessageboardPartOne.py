#!/usr/bin/env python3
#
# Step one in building the messageboard server:
# An echo server for POST requests.
#
# Instructions:
#
# This server should accept a POST request and return the value of the
# "message" field in that request.
#
# You'll need to add three things to the do_POST method to make it work:
#
# 1. Find the length of the request data.
# 2. Read the correct amount of request data.
# 3. Extract the "message" field from the request data.
#
# When you're done, run this server and test it from your browser using the
# Messageboard.html form.  Then run the test.py script to check it.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs


class MessageHandler(BaseHTTPRequestHandler):
    form = """<!DOCTYPE html>
              <title>Message Board</title>
              <form method="POST" action="http://localhost:8000/">
                <textarea name="message"></textarea>
                <br>
                <button type="submit">Post it!</button>
              </form>
        """

    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Now, write the response body.
        self.wfile.write(self.form.encode())

    def do_POST(self):
        # 1. How long was the message? (Use the Content-Length header.)
        content_length = int(self.headers.get('content-length', 0))
        # 2. Read the correct amount of data from the request.
        body = self.rfile.read(content_length).decode()

        # 3. Extract the "message" field from the request data.
        message = parse_qs(body).get('message', '')

        # Send the "message" field back as the response.
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message[0].encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
