import http.server
import socketserver
import atexit


class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

server = socketserver.TCPServer(('', 8000), HTTPRequestHandler)

def cleanup_handler():
    print('shutting down python server...')
    server.shutdown()

atexit.register(cleanup_handler)
print('Starting python server on http://localhost:8000...')
server.serve_forever()

