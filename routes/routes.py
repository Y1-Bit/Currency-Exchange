from controller.controller import RequestHandler
from database.db_manager import connection_maker
from database.repo.currency import CurrencyRepo
from database.transaction_manager import TransactionManager
from routes.router import Router

router = Router()


@router.get("/currencies")
def get_currencies(handler: RequestHandler, query) -> dict:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currencies = repo.get_all_currencies()
    response = currencies.to_json()
    return {"status_code": 200, "body": response}


@router.get("/currency/")
def get_currency(handler: RequestHandler, query) -> None: ...


@router.get("/exchangeRates")
def handle_get_exchange_rates(handler, query): ...


@router.post("/currencies")
def handle_post_currency(handler, form_data): ...
