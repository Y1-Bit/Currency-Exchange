from functools import partial
from http.server import HTTPServer

from controller.controller import RequestHandler
from database.db_manager import DatabaseManager
from database.repo.requests import RequestsRepo
from routes.routes import router


def run(handler_class, server_class=HTTPServer, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()


def main() -> None:
    db_manager = DatabaseManager("database.db")
    repo = RequestsRepo(db_manager)
    handler_class = partial(RequestHandler, repo=repo, router=router)
    run(handler_class=handler_class)


if __name__ == "__main__":
    main()
