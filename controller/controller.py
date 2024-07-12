from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from .router import Router


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, router: Router, **kwargs) -> None:
        self.router = router
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        self.handle_request("GET")

    def handle_get(self, handler, query) -> None:
        handler(self, query)

    def do_POST(self) -> None:
        self.handle_request("POST")

    def handle_post(self, handler) -> None:
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(post_data)
        handler(self, form_data)

    def handle_request(self, method) -> None:
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        handler = self.router.get_handler(path, method)
        if handler:
            try:
                if method == "GET":
                    self.handle_get(handler, query)
                elif method == "POST":
                    self.handle_post(handler)
            except BrokenPipeError:
                self.log_error(
                    "BrokenPipeError: Client closed the connection before response could be sent."
                )
            except Exception as e:
                self.log_error(f"Exception: {e}")
                self.send_error(500, f"Internal Server Error: {e}")
        else:
            self.not_found()

    def send_response_with_body(self, code, body) -> None:
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def not_found(self) -> None:
        response = "Not Found"
        self.send_response_with_body(404, response)