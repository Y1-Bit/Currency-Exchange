from database import CurrencyDAO
from model import CurrencyDTO


class CurrencyService:
    @staticmethod
    def get_all_currencies() -> list[CurrencyDTO]:
        return CurrencyDAO.get_all_currencies()
    
    @staticmethod
    def get_currency(code: str) -> CurrencyDTO | None:
        return CurrencyDAO.get_currency_by_code(code)
    
    @staticmethod
    def add_currency(name: str, code: str, sign: str) -> CurrencyDTO:
        existing_currency = CurrencyDAO.get_currency_by_code(code)  
        if existing_currency:
            raise ValueError(f"Currency with code {code} already exists")
        return CurrencyDAO.add_currency(name, code, sign)   