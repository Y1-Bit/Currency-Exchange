import json
from model.exchange import Exchange
from model.currency import Currency


class CurrencyView:
    @staticmethod
    def show_currencies(currencies: list[Currency]) -> str:
        return json.dumps([currency.__dict__ for currency in currencies])

    @staticmethod
    def show_currency(currency: Currency) -> str:
        return json.dumps(currency.__dict__)


class ExchangeView:
    @staticmethod
    def currency_to_dict(currency: Currency) -> dict:
        return {
            "id": currency.id,
            "code": currency.code,
            "name": currency.name,
            "sign": currency.sign
        }

    @staticmethod
    def exchange_to_dict(exchange: Exchange) -> dict:
        return {
            "id": exchange.id,
            "baseCurrency": ExchangeView.currency_to_dict(exchange.base_currency),
            "targetCurrency": ExchangeView.currency_to_dict(exchange.target_currency),
            "rate": exchange.rate
        }

    @staticmethod
    def show_exchanges(exchanges: list[Exchange]) -> str:
        return json.dumps([ExchangeView.exchange_to_dict(exchange) for exchange in exchanges], indent=4)