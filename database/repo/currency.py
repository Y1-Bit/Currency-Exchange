from database.repo.base import BaseRepo
from model.currency import Currency, ListCurrency


class CurrencyRepo(BaseRepo):
      def get_all_currencies(self) -> ListCurrency:
        self.cursor.execute("SELECT id, code, name, sign FROM Currencies")
        rows = self.cursor.fetchall()
        currencies = [Currency(*row) for row in rows] 
        return ListCurrency(currencies)
      
      def get_currency_by_code(self, code: str) -> Currency | None:
         self.cursor.execute("SELECT id, code, name, sign FROM Currencies WHERE code = ?", (code,))
         row = self.cursor.fetchone()
         return Currency(*row) if row else None