import json

from model import CurrencyDTO


class CurrencyView:
    @staticmethod
    def show_currencies(currencies: list[CurrencyDTO]) -> str:
        return json.dumps([currency.__dict__ for currency in currencies])

    @staticmethod
    def show_currency(currency: CurrencyDTO) -> str:
        return json.dumps(currency.__dict__)