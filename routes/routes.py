from controller.controller import RequestHandler
from database.repo.requests import RequestsRepo
from routes.router import Router


router = Router()


@router.get("/currencies")
def get_currencies(handler: RequestHandler, query, repo: RequestsRepo) -> None:
    currencies = repo.currency.get_all_currencies()
    response = currencies.to_json()
    handler.send_response_with_body(200, response)


@router.get("/currency/")
def get_currency(handler: RequestHandler, query, repo: RequestsRepo) -> None: ...


@router.get("/exchangeRates")
def handle_get_exchange_rates(handler, query, repo: RequestsRepo): ...


@router.post("/currencies")
def handle_post_currency(handler, form_data, repo: RequestsRepo): ...
