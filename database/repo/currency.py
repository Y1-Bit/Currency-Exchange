from database.repo.base import BaseRepo
from model.currency import Currency, CurrencyList


class CurrencyRepo(BaseRepo):
    def get_all_currencies(self) -> CurrencyList:
        self.cursor.execute("SELECT id, code, name, sign FROM Currencies")
        rows = self.cursor.fetchall()
        currencies = [Currency(*row) for row in rows]
        return CurrencyList(currencies)

    def get_currency_by_code(self, code: str) -> Currency | None:
        self.cursor.execute(
            "SELECT id, code, name, sign FROM Currencies WHERE code = ?", (code,)
        )
        row = self.cursor.fetchone()
        return Currency(*row) if row else None

    def add_currency(self, code: str, name: str, sign: str) -> Currency:
        self.cursor.execute(
            "INSERT INTO Currencies (code, name, sign) VALUES (?, ?, ?)",
            (code, name, sign),
        )
        return Currency(None, code, name, sign)
