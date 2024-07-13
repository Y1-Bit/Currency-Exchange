from database.repo.base import BaseRepo
from model import Currency, ListCurrency


class CurrencyRepo(BaseRepo):
     def get_all_currencies(self) -> ListCurrency:
        with self.db_manager.transaction() as cursor:
            cursor.execute("SELECT id, code, name, sign FROM Currencies")
            rows = cursor.fetchall()
        currencies = [Currency(*row) for row in rows] 
        return ListCurrency(currencies)