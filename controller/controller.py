from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from database.repo.requests import RequestsRepo
from router.router import router

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, repo: RequestsRepo, **kwargs):
        self.repo = repo
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def handle_request(self, method):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        self.repo.db_manager.connect()

        handler = router.find_handler(method, path)
        if handler:
            if method == "POST":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length).decode("utf-8")
                form_data = {k: v[0] for k, v in parse_qs(post_data).items()}
                handler(self, form_data, self.repo)
            elif method == "GET":
                handler(self, query, self.repo)
        else:
            self.not_found()

        self.repo.db_manager.close()

    def send_response_with_body(self, code, body):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def not_found(self):
        response = "Not Found"
        self.send_response_with_body(404, response)
