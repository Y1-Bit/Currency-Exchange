from controller import RequestHandler
from service import CurrencyService
from view import CurrencyView


def handle_get_currencies(handler: RequestHandler, query) -> None:
    currencies = CurrencyService.get_all_currencies()
    response = CurrencyView.show_currencies(currencies)
    handler.send_response_with_body(200, response)


def handle_get_currency(handler: RequestHandler, query) -> None:
    code = handler.path.split("/")[-1]
    currency = CurrencyService.get_currency(code)
    if currency:
        response = CurrencyView.show_currency(currency)
        handler.send_response_with_body(200, response)
    else:
        response = "Currency not found"
        handler.send_response_with_body(404, response)


def handle_post_currency(handler: RequestHandler, form_data: dict) -> None:
    name = form_data.get("name", [None])[0]
    code = form_data.get("code", [None])[0]
    sign = form_data.get("sign", [None])[0]
    if not name or not code or not sign:
        handler.send_response_with_body(400, "Missing required fields")
        return
    try:
        currency = CurrencyService.add_currency(name, code, sign)
        response = CurrencyView.show_currency(currency)
        handler.send_response_with_body(201, response)
    except ValueError as e:
        handler.send_response_with_body(400, str(e))
