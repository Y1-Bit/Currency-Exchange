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