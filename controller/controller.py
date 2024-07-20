from http.server import BaseHTTPRequestHandler
from typing import Callable
from urllib.parse import parse_qs, urlparse

from routes.router import Router


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, router: Router, **kwargs) -> None:
        self.router = router
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        self.handle_request("GET")

    def do_POST(self) -> None:
        self.handle_request("POST")

    def do_PATCH(self) -> None:
        self.handle_request("PATCH")

    def do_OPTIONS(self) -> None:
        self.handle_options()

    def handle_request(self, method: str) -> None:
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        handler, path_params = self.router.find_handler(method, path)
        if handler:
            if method in ["POST", "PATCH"]:
                self.handle_with_body(handler, path_params)
            elif method == "GET":
                self.handle_get(handler, path_params, query)
        else:
            self.handle_not_found()

    def handle_options(self) -> None:
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def handle_get(
        self, handler: Callable, path_params: str | None, query: dict[str, list[str]]
    ) -> None:
        if path_params:
            response = handler(path_params)
        elif query:
            response = handler(query)
        else:
            response = handler()
        self.send_response_with_body(response["status_code"], response["body"])

    def handle_with_body(
        self, handler: Callable, path_params: str | None = None
    ) -> None:
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        form_data = {k: v[0] for k, v in parse_qs(post_data).items()}
        if path_params:
            response = handler(form_data, path_params)
        else:
            response = handler(form_data)
        self.send_response_with_body(response["status_code"], response["body"])

    def send_response_with_body(self, code: int, body: str) -> None:
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def handle_not_found(self) -> None:
        response = "Not Found"
        self.send_response_with_body(404, response)
