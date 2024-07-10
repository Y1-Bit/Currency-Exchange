from database import CurrencyDAO
from model import CurrencyDTO


class CurrencyService:
    @staticmethod
    def get_all_currencies() -> list[CurrencyDTO]:
        return CurrencyDAO.get_all_currencies()
    
    @staticmethod
    def get_currency(code: str) -> CurrencyDTO | None:
        return CurrencyDAO.get_currency_by_code(code)