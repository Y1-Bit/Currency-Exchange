from model import Currency

from .db_manager import get_db_connection


class CurrencyDAO:
    @staticmethod
    def get_all_currencies() -> list[Currency]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, name, sign FROM Currencies")
            rows = cursor.fetchall()
        return [Currency(*row) for row in rows]

    @staticmethod
    def get_currency_by_code(code: str) -> Currency | None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, name, sign FROM Currencies WHERE code = ?", (code,))
            row = cursor.fetchone()
        return Currency(*row) if row else None
    
    
    @staticmethod
    def add_currency(name: str, code: str, sign: str) -> Currency:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Currencies (code, name, sign) VALUES (?, ?, ?)", (code, name, sign))
            conn.commit()
            currency_id = cursor.lastrowid
            return Currency(currency_id, code, name, sign)
        
    @staticmethod
    def get_currency_by_id(currency_id: int) -> Currency | None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, name, sign FROM Currencies WHERE id = ?", (currency_id,))
            row = cursor.fetchone()
        return Currency(*row) if row else None