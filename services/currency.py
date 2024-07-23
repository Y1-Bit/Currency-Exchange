from database.db_manager import connection_maker
from database.repo.currency import CurrencyRepo
from database.transaction_manager import TransactionManager


def get_all_currencies() -> str:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currencies = repo.get_all_currencies()
    return currencies.to_json()


def get_currency_by_code(code: str) -> str | None:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currency = repo.get_currency_by_code(code)
    if not currency:
        return None
    return currency.to_json()


def add_currency(code: str, name: str, sign: str) -> str:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currency = repo.add_currency(code, name, sign)
    return currency.to_json()
