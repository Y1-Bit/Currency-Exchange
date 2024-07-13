from controller.router import router
from controller import RequestHandler
from service.service import CurrencyService, ExchangeDAO
from view import CurrencyView, ExchangeView


@router.get("/currencies")
def get_currencies(handler: RequestHandler, query):
    currencies = CurrencyService.get_all_currencies()
    response = CurrencyView.show_currencies(currencies)
    handler.send_response_with_body(200, response)

@router.get("/currency/")
def get_currency(handler: RequestHandler, query) -> None:
    code = handler.path.split("/")[-1]
    currency = CurrencyService.get_currency(code)
    if currency:
        response = CurrencyView.show_currency(currency)
        handler.send_response_with_body(200, response)
    else:
        response = "Currency not found"
        handler.send_response_with_body(404, response)

@router.get("/exchangeRates")
def handle_get_exchange_rates(handler, query):
    exchanges = ExchangeDAO.get_all_exchanges()
    response = ExchangeView.show_exchanges(exchanges)
    handler.send_response_with_body(200, response)

@router.post("/currencies")
def handle_post_currency(handler, form_data):
    name = form_data.get('name', [None])[0]
    code = form_data.get('code', [None])[0]
    sign = form_data.get('sign', [None])[0]

    if not name or not code or not sign:
        handler.send_response_with_body(400, "Missing required form field")
        return

    try:
        currency = CurrencyService.add_currency(name, code, sign)
        response = CurrencyView.show_currency(currency)
        handler.send_response_with_body(201, response)
    except ValueError as e:
        handler.send_response_with_body(409, str(e))
    except Exception as e:
        handler.send_response_with_body(500, f"Internal Server Error: {e}")
