from database import CurrencyDAO, ExchangeDAO
from model import Currency, Exchange


class CurrencyService:
    @staticmethod
    def get_all_currencies() -> list[Currency]:
        return CurrencyDAO.get_all_currencies()
    
    @staticmethod
    def get_currency(code: str) -> Currency | None:
        return CurrencyDAO.get_currency_by_code(code)
    
    @staticmethod
    def add_currency(name: str, code: str, sign: str) -> Currency:
        existing_currency = CurrencyDAO.get_currency_by_code(code)  
        if existing_currency:
            raise ValueError(f"Currency with code {code} already exists")
        return CurrencyDAO.add_currency(name, code, sign)   



class ExchangeService:
    @staticmethod
    def get_all_exchanges() -> list[Exchange]:
        return ExchangeDAO.get_all_exchanges()