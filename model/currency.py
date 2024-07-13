import json
from dataclasses import asdict, dataclass


@dataclass
class Currency:
    id: int | None
    code: str
    name: str
    sign: str

    def to_dict(self):
        return asdict(self)
   
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4) 
    

@dataclass
class ListCurrency:
    currencies: list[Currency]

    def to_json(self):
        return json.dumps([currency.to_dict() for currency in self.currencies], indent=4)