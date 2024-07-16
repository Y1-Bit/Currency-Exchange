from functools import partial
from http.server import HTTPServer

from controller.controller import RequestHandler
from routes.routes import router


def run(handler_class, server_class=HTTPServer, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()


def main() -> None:
    handler_class = partial(RequestHandler, router=router)
    run(handler_class=handler_class)


if __name__ == "__main__":
    main()
