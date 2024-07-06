import sqlite3

from model.model import Currency


class DatabaseConnection:
    def __enter__(self) -> sqlite3.Cursor:
        self.conn = sqlite3.connect("db.sqlite3")
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class CurrencyService:
    @staticmethod
    def get_all_currencies() -> list:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT id, code, full_name, sign FROM Currencies")
            rows = cursor.fetchall()
        return [Currency(*row) for row in rows]
