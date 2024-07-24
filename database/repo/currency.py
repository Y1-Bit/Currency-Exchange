from database.repo.base import BaseRepo
from model.currency import Currency, CurrencyList
from exceptions import CurrencyNotFoundException, CurrencyAlreadyExistsException


class CurrencyRepo(BaseRepo):
    def get_all_currencies(self) -> CurrencyList:
        self.cursor.execute("SELECT id, code, name, sign FROM Currencies")
        rows = self.cursor.fetchall()
        currencies = [Currency(*row) for row in rows]
        return CurrencyList(currencies)

    def get_currency_by_code(self, code: str) -> Currency:
        self.cursor.execute(
            "SELECT id, code, name, sign FROM Currencies WHERE code = ?", (code,)
        )
        row = self.cursor.fetchone()
        if row is None:
            raise CurrencyNotFoundException(f"Currency with code {code} not found")
        return Currency(*row)

    def add_currency(self, code: str, name: str, sign: str) -> Currency:
        self.cursor.execute("SELECT COUNT(*) FROM Currencies WHERE code = ?", (code,))
        if self.cursor.fetchone()[0] > 0:
            raise CurrencyAlreadyExistsException(
                f"Currency with code {code} already exists."
            )

        self.cursor.execute(
            "INSERT INTO Currencies (code, name, sign) VALUES (?, ?, ?)",
            (code, name, sign),
        )
        return Currency(None, code, name, sign)
