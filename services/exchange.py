from decimal import Decimal

from database.db_manager import connection_maker
from database.repo.currency import CurrencyRepo
from database.repo.exchange import ExchangeRepo
from database.transaction_manager import TransactionManager
from exceptions import ExchangeRateNotFoundException
from model.exchange import Exchange, ExchangeList, ExchangeResult


def get_all_exchange_rates() -> ExchangeList:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = ExchangeRepo(cursor)
            exchange_rates = repo.get_all_exchanges()
    return exchange_rates

def get_exchange_rate_by_pair(pair: str) -> Exchange:
    base_currency_code = pair[:3]
    target_currency_code = pair[3:]

    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)

            exchange_repo = ExchangeRepo(cursor)
            exchange_rate = exchange_repo.get_exchange_by_pair(
                base_currency, target_currency
            )

    return exchange_rate

def add_exchange_rate(
    base_currency_code: str, target_currency_code: str, rate: str
) -> Exchange:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)

            exchange_repo = ExchangeRepo(cursor)
            exchange_rate = exchange_repo.add_exchange(
                base_currency, target_currency, float(rate)
            )

    return exchange_rate

def update_exchange_rate(
    base_currency_code: str, target_currency_code: str, rate: str
) -> Exchange:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)

            exchange_repo = ExchangeRepo(cursor)
            exchange_rate = exchange_repo.get_exchange_by_pair(
                base_currency, target_currency
            )
            exchange_rate = exchange_repo.update_exchange(exchange_rate, float(rate))

    return exchange_rate

def get_exchange(base_currency_code: str, target_currency_code: str, amount: str) -> ExchangeResult:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)

            exchange_repo = ExchangeRepo(cursor)
            try:
                exchange_rate = exchange_repo.get_exchange_by_pair(base_currency, target_currency)
                rate = Decimal(exchange_rate.rate)
            except ExchangeRateNotFoundException:
                try:
                    reverse_exchange_rate = exchange_repo.get_exchange_by_pair(target_currency, base_currency)
                    rate = Decimal(1) / Decimal(reverse_exchange_rate.rate)
                except ExchangeRateNotFoundException:
                    usd_currency = currency_repo.get_currency_by_code("USD")
                    base_to_usd = exchange_repo.get_exchange_by_pair(base_currency, usd_currency)
                    usd_to_target = exchange_repo.get_exchange_by_pair(usd_currency, target_currency)

                    rate = Decimal(base_to_usd.rate) * Decimal(usd_to_target.rate)

            converted_amount = (Decimal(amount) * rate).quantize(Decimal("0.01"))

    return ExchangeResult(base_currency, target_currency, rate, Decimal(amount), converted_amount)