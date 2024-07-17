from database.repo.base import BaseRepo
from model.exchange import Exchange, ExchangeList
from model.currency import Currency 


class ExchangeRepo(BaseRepo):
    def get_all_exchanges(self) -> ExchangeList:
        self.cursor.execute("SELECT id, base_currency_id, target_currency_id, rate FROM ExchangeRates")
        rows = self.cursor.fetchall()
        
        exchanges = []
        for row in rows:
            exchange_id, base_currency_id, target_currency_id, rate = row
            
            self.cursor.execute("SELECT id, code, name, sign FROM Currencies WHERE id = ?", (base_currency_id,))
            base_currency_data = self.cursor.fetchone()
            base_currency = Currency(*base_currency_data)
            
            self.cursor.execute("SELECT id, code, name, sign FROM Currencies WHERE id = ?", (target_currency_id,))
            target_currency_data = self.cursor.fetchone()
            target_currency = Currency(*target_currency_data)
            
            exchange = Exchange(exchange_id, base_currency, target_currency, rate)
            exchanges.append(exchange)
        
        return ExchangeList(exchanges)
    
    def get_exchange_by_pair(self, base_currency_code: str, target_currency_code: str) -> Exchange | None:
        self.cursor.execute("""
            SELECT 
                e.id, e.rate,
                bc.id, bc.code, bc.name, bc.sign,
                tc.id, tc.code, tc.name, tc.sign
            FROM ExchangeRates e
            JOIN Currencies bc ON e.base_currency_id = bc.id
            JOIN Currencies tc ON e.target_currency_id = tc.id
            WHERE bc.code = ? AND tc.code = ?
        """, (base_currency_code, target_currency_code))
        
        row = self.cursor.fetchone()
        if row:
            exchange_id, rate, bc_id, bc_code, bc_name, bc_sign, tc_id, tc_code, tc_name, tc_sign = row
            base_currency = Currency(bc_id, bc_code, bc_name, bc_sign)
            target_currency = Currency(tc_id, tc_code, tc_name, tc_sign)
            return Exchange(exchange_id, base_currency, target_currency, rate)
        return None