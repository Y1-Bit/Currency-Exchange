import json
from dataclasses import dataclass
from decimal import Decimal

from model.currency import Currency


@dataclass
class Exchange:
    id: int | None
    base_currency: Currency
    target_currency: Currency
    rate: float

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "baseCurrency": self.base_currency.to_dict(),
            "targetCurrency": self.target_currency.to_dict(),
            "rate": self.rate,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class ExchangeList:
    exchanges: list[Exchange]

    def to_json(self) -> str:
        return json.dumps([exchange.to_dict() for exchange in self.exchanges])


@dataclass
class ExchangeResult:
    baseCurrency: Currency
    targetCurrency: Currency
    rate: Decimal
    amount: Decimal
    convertedAmount: Decimal

    def to_dict(self) -> dict:
        return {
            "baseCurrency": self.baseCurrency.to_dict(),
            "targetCurrency": self.targetCurrency.to_dict(),
            "rate": str(self.rate),
            "amount": str(self.amount),
            "convertedAmount": str(self.convertedAmount),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
