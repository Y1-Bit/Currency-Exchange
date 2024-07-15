from database.repo.base import BaseRepo
from model.currency import Currency, ListCurrency
from database.transaction_manager import TransactionManager



class CurrencyRepo(BaseRepo):
     def get_all_currencies(self) -> ListCurrency:
        with TransactionManager(self.connection) as cursor:
            cursor.execute("SELECT id, code, name, sign FROM Currencies")
            rows = cursor.fetchall()
        currencies = [Currency(*row) for row in rows] 
        return ListCurrency(currencies)