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
      
      def add_currency(self, form_data: dict) -> Currency:
          code = form_data["code"]
          name = form_data["name"]
          sign = form_data["sign"]
          self.cursor.execute("INSERT INTO Currencies (code, name, sign) VALUES (?, ?, ?)", (code, name, sign))
          return Currency(None, code, name, sign)
       
      