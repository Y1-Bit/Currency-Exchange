from controller import RequestHandler
from database import ExchangeDAO
from view import ExchangeView


def handle_get_exchange_rates(handler: RequestHandler, query) -> None:
    exchanges = ExchangeDAO.get_all_exchanges()
    response = ExchangeView.show_exchanges(exchanges)
    handler.send_response_with_body(200, response)
