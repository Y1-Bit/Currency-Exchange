from .currency_dto import CurrencyDTO


class ExchangeDTO:
    def __init__(self, id: int, base_currency: CurrencyDTO, target_currency: CurrencyDTO, rate: float) -> None:
        self.id = id 
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.rate = rate 
    