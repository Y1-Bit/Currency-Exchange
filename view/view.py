import json
from model.exchange_dto import ExchangeDTO
from model.currency_dto import CurrencyDTO


class CurrencyView:
    @staticmethod
    def show_currencies(currencies: list[CurrencyDTO]) -> str:
        return json.dumps([currency.__dict__ for currency in currencies])

    @staticmethod
    def show_currency(currency: CurrencyDTO) -> str:
        return json.dumps(currency.__dict__)


class ExchangeView:
    @staticmethod
    def currency_to_dict(currency: CurrencyDTO) -> dict:
        return {
            "id": currency.id,
            "code": currency.code,
            "name": currency.name,
            "sign": currency.sign
        }

    @staticmethod
    def exchange_to_dict(exchange: ExchangeDTO) -> dict:
        return {
            "id": exchange.id,
            "baseCurrency": ExchangeView.currency_to_dict(exchange.base_currency),
            "targetCurrency": ExchangeView.currency_to_dict(exchange.target_currency),
            "rate": exchange.rate
        }

    @staticmethod
    def show_exchanges(exchanges: list[ExchangeDTO]) -> str:
        return json.dumps([ExchangeView.exchange_to_dict(exchange) for exchange in exchanges], indent=4)