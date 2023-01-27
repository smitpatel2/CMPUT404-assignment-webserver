#  coding: utf-8 

import os
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Smit Patel
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/



class CustomWebServer(socketserver.BaseRequestHandler):
    def init(self):
        self.file_paths = []
        self.folder_paths = []
        for root, dirs, files in os.walk("www"):
            for file in files:
                self.file_paths.append(os.path.join(root, file)[3:])
            for folder in dirs:
                self.folder_paths.append(os.path.join(root, folder)[3:])

    def process_request(self):
        request_data = self.request.recv(1024).strip()
        print(f"Received request: {request_data}\n")
        tokens = str(request_data).split()
        if tokens[0] != "b'GET":
            response = b'HTTP/1.1 405 Method Not Allowed\r\n'
            b'Connection: close\r\n'
        else:
            requested_path = tokens[1]
            if requested_path[-1] == "/":
                requested_path += "index.html"
            if requested_path not in self.file_paths:
                if requested_path not in self.folder_paths:
                    response = b'HTTP/1.1 404 Not Found\r\n'
                    b'Connection: close\r\n'
                else:
                    response = b'HTTP/1.1 301 Moved Permanently\r\n'
                    response += b'Location: http://127.0.0.1:8080' + bytes(requested_path, 'utf-8') + b'/\r\n'
            else:
                file_ext = requested_path.split(".")[-1]
                if file_ext == "css":
                    response = b'HTTP/1.1 200 OK\r\n'
                    response += b'Content-Type: text/css; charset=utf-8\r\n'
                    response += b'\r\n'
                elif file_ext == "html":
                    response = b'HTTP/1.1 200 OK\r\n'
                    response += b'Content-Type: text/html; charset=utf-8\r\n'
                    response += b'\r\n'
                else:
                    response = b'HTTP/1.1 200 OK\r\n'
                    response += b'Content-Type: application/octet-stream; charset=utf-8\r\n'
                    response += b'\r\n'
                with open("www" + requested_path, 'rb') as f:
                    response += f.read()
        self.request.sendall(response)

    def handle(self):
        self.process_request()

if __name__ == "__main__":
    ADDR, PORT_NUM = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
        # Create the server, binding to localhost on port 8080

    web_server = socketserver.TCPServer((ADDR, PORT_NUM), CustomWebServer)
    # Activate the server; this will keep running until you r
    # interrupt the program with Ctrl-C
    web_server.serve_forever()
