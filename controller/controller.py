from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from service.service import CurrencyService
from view import CurrencyView

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        try:
            if path == '/currencies':
                currencies = CurrencyService.get_all_currencies()
                response = CurrencyView.show_currencies(currencies)
                self.send_response_with_body(200, response)

            elif path.startswith('/currency/'):
                code = path.split('/')[-1]
                currency = CurrencyService.get_currency(code)
                if currency:
                    response = CurrencyView.show_currency(currency)
                    self.send_response_with_body(200, response)
                else:
                    response = "Currency not found"
                    self.send_response_with_body(404, response)

            else:
                response = "Not Found"
                self.send_response_with_body(404, response)

        except BrokenPipeError:
            self.log_error("BrokenPipeError: Client closed the connection before response could be sent.")
        except Exception as e:
            self.log_error(f"Exception: {e}")
            self.send_error(500, f"Internal Server Error: {e}")

    def send_response_with_body(self, code, body):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))