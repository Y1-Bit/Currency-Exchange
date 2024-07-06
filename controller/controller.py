from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from service.service import CurrencyService
from view.view import show_currencies

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/currencies':
            currencies = CurrencyService.get_all_currencies()
            response = show_currencies(currencies)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_error(404, "Not Found")