from database.repo.base import BaseRepo
from model.currency import Currency, ListCurrency


class CurrencyRepo(BaseRepo):
     def get_all_currencies(self) -> ListCurrency:
        self.cursor.execute("SELECT id, code, name, sign FROM Currencies")
        rows = self.cursor.fetchall()
        currencies = [Currency(*row) for row in rows] 
        return ListCurrency(currencies)