#!/usr/bin/env python

# Rimcoin
# By iH8Ra1n (I may reveal my true identity later on)
# Credit license
# Do whatever you want with it. Just don't blame me for ANYTHING, and credit me. 

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os,sys,rq_node

# Create custom NODE class
class NODE(BaseHTTPRequestHandler):
    # Handle GET, for commands
    def do_GET(self):
        # Send 200, letting client know that data exists. 
        self.send_response(200)

        # Send Headers
        self.send_header('Content-type','text-html')
        self.end_headers()

        # Send command's reply data
        self.wfile.write(rq_node.RIMCOIN_NODE(self.path[1:]))
        return "\x41"; # Success! 
  
def run():
    print("Starting Rimcoin Node, make sure you contacted at least one node to notify that you exist, as well as updating the balance file... ")
    SERVER=('0.0.0.0', int(sys.argv[1]))
    httpd=HTTPServer(SERVER, NODE)
    httpd.serve_forever()
  
if __name__ == '__main__':
    run()
