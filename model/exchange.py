from dataclasses import dataclass

from .currency import Currency


@dataclass
class Exchange:
    id: int
    base_currency: Currency
    target_currency: Currency
    rate: float
