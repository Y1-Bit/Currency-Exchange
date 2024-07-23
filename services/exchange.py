import json
from decimal import Decimal
from sqlite3 import IntegrityError

from database.db_manager import connection_maker
from database.repo.currency import CurrencyRepo
from database.repo.exchange import ExchangeRepo
from database.transaction_manager import TransactionManager


def get_all_exchange_rates() -> tuple[int, str]:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = ExchangeRepo(cursor)
            exchange_rates = repo.get_all_exchanges()
    return 200, exchange_rates.to_json()


def get_exchange_rate_by_pair(pair: str) -> tuple[int, str]:
    base_currency_code = pair[:3]
    target_currency_code = pair[3:]

    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)

            if not base_currency or not target_currency:
                return 404, "Currency pair not found"

            exchange_repo = ExchangeRepo(cursor)
            exchange_rate = exchange_repo.get_exchange_by_pair(
                base_currency, target_currency
            )

            if not exchange_rate:
                return 404, "Exchange rate not found"

    return 200, exchange_rate.to_json()


def add_exchange_rate(
    base_currency_code: str, target_currency_code: str, rate: str
) -> tuple[int, str]:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)

            if not base_currency or not target_currency:
                return 404, "Currency not found"

            exchange_repo = ExchangeRepo(cursor)

            try:
                exchange_rate = exchange_repo.add_exchange(
                    base_currency, target_currency, float(rate)
                )
            except IntegrityError:
                return 409, "Exchange rate already exists"

    return 201, exchange_rate.to_json()


def update_exchange_rate(
    base_currency_code: str, target_currency_code: str, rate: str
) -> tuple[int, str]:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)

            if not base_currency or not target_currency:
                return 404, "Currency not found"

            exchange_repo = ExchangeRepo(cursor)
            exchange_rate = exchange_repo.get_exchange_by_pair(
                base_currency, target_currency
            )

            if not exchange_rate:
                return 404, "Exchange rate not found"

            exchange_rate = exchange_repo.update_exchange(exchange_rate, float(rate))

    return 200, exchange_rate.to_json()


def get_exchange(base_currency_code: str, target_currency_code: str, amount: str) -> tuple[int, str]:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)
            if not base_currency or not target_currency:
                return 404, "Currency not found"

            exchange_repo = ExchangeRepo(cursor)
            exchange_rate = exchange_repo.get_exchange_by_pair(base_currency, target_currency)
            if exchange_rate:
                rate = Decimal(exchange_rate.rate)
            else:
                reverse_exchange_rate = exchange_repo.get_exchange_by_pair(target_currency, base_currency)
                if reverse_exchange_rate:
                    rate = Decimal(1) / Decimal(reverse_exchange_rate.rate)
                else:
                    usd_currency = currency_repo.get_currency_by_code("USD")
                    if not usd_currency:
                        return 404, "USD currency not found"

                    base_to_usd = exchange_repo.get_exchange_by_pair(base_currency, usd_currency)
                    usd_to_target = exchange_repo.get_exchange_by_pair(usd_currency, target_currency)
                    if not base_to_usd or not usd_to_target:
                        return 404, "Exchange rate not found"

                    rate = Decimal(base_to_usd.rate) * Decimal(usd_to_target.rate)
            
            converted_amount = (Decimal(amount) * rate).quantize(Decimal("0.01"))

    response = {
        "baseCurrency": base_currency.to_json(),
        "targetCurrency": target_currency.to_json(),
        "rate": str(rate),
        "amount": str(amount),
        "convertedAmount": str(converted_amount),
    }
    response = json.dumps(response)
    return 200, response
