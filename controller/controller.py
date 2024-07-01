from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from service.service import UserService
from view.view import show_user

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path.startswith('/user'):
            try:
                user_id = int(path.split('/')[-1])
                user_details = UserService.get_user_details(user_id)
                response = show_user(user_details)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
            except Exception as e:
                self.send_error(404, str(e))
        else:
            self.send_error(404, "Not Found")