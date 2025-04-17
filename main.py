from http.server import HTTPServer
from NHLDataRequestHandler import NHLDataRequestHandler


def run(server_class=HTTPServer, handler_class=NHLDataRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
