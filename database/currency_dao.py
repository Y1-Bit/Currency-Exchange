from model import CurrencyDTO

from .db_manager import get_db_connection


class CurrencyDAO:
    @staticmethod
    def get_all_currencies() -> list[CurrencyDTO]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, name, sign FROM Currencies")
            rows = cursor.fetchall()
        return [CurrencyDTO(*row) for row in rows]

    @staticmethod
    def get_currency_by_code(code: str) -> CurrencyDTO | None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, name, sign FROM Currencies WHERE code = ?", (code,))
            row = cursor.fetchone()
        return CurrencyDTO(*row) if row else None
    
    
    @staticmethod
    def add_currency(name: str, code: str, sign: str) -> CurrencyDTO:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Currencies (code, name, sign) VALUES (?, ?, ?)", (code, name, sign))
            conn.commit()
            currency_id = cursor.lastrowid
            return CurrencyDTO(currency_id, code, name, sign)