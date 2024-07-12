from functools import partial
from http.server import HTTPServer

from controller import RequestHandler, RouteInitializer, Router


def run(handler_class, server_class=HTTPServer, port=8000) -> None:
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}")
    httpd.serve_forever()


def main() -> None:
    router = Router()
    initializer = RouteInitializer(router)
    initializer.init_routes()

    handler_class = partial(RequestHandler, router=router)
    run(handler_class=handler_class)


if __name__ == "__main__":
    main()
