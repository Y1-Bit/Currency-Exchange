from dataclasses import dataclass

from model.currency import Currency


@dataclass
class Exchange:
    id: int
    base_currency: Currency
    target_currency: Currency
    rate: float
