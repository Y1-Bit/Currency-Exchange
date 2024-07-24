from database.db_manager import connection_maker
from database.repo.currency import CurrencyRepo
from database.transaction_manager import TransactionManager
from model import Currency, CurrencyList


def get_all_currencies() -> CurrencyList:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currencies = repo.get_all_currencies()
    return currencies


def get_currency_by_code(code: str) -> Currency:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currency = repo.get_currency_by_code(code)
    return currency


def add_currency(code: str, name: str, sign: str) -> Currency:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currency = repo.add_currency(code, name, sign)
    return currency
