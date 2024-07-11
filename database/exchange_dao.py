from model import ExchangeDTO, CurrencyDTO
from .db_manager import get_db_connection

class ExchangeDAO:
    @staticmethod
    def get_all_exchanges() -> list[ExchangeDTO]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    e.id, e.rate,
                    bc.id, bc.code, bc.name, bc.sign,
                    tc.id, tc.code, tc.name, tc.sign
                FROM ExchangeRates e
                JOIN Currencies bc ON e.base_currency_id = bc.id
                JOIN Currencies tc ON e.target_currency_id = tc.id
            """)
            rows = cursor.fetchall()

        exchanges = []
        for row in rows:
            exchange_id, rate, \
            base_currency_id, base_currency_code, base_currency_name, base_currency_sign, \
            target_currency_id, target_currency_code, target_currency_name, target_currency_sign = row
            
            base_currency = CurrencyDTO(base_currency_id, base_currency_code, base_currency_name, base_currency_sign)
            target_currency = CurrencyDTO(target_currency_id, target_currency_code, target_currency_name, target_currency_sign)
            exchanges.append(ExchangeDTO(exchange_id, base_currency, target_currency, rate))

        return exchanges