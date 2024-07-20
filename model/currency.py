import json
from dataclasses import asdict, dataclass


@dataclass
class Currency:
    id: int | None
    code: str
    name: str
    sign: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class CurrencyList:
    currencies: list[Currency]

    def to_json(self) -> str:
        return json.dumps([currency.to_dict() for currency in self.currencies])
