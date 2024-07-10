from model import CurrencyDTO

from .db_manager import get_db_connection


class CurrencyDAO:
    @staticmethod
    def get_all_currencies() -> list[CurrencyDTO]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, full_name, sign FROM Currencies")
            rows = cursor.fetchall()
        return [CurrencyDTO(*row) for row in rows]

    @staticmethod
    def get_currency_by_code(code: str) -> CurrencyDTO | None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, code, full_name, sign FROM Currencies WHERE code = ?", (code,))
            row = cursor.fetchone()
        return CurrencyDTO(*row) if row else None