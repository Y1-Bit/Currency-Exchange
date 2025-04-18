from database.repo.base import BaseRepo
from model.exchange import Exchange, ExchangeList
from model.currency import Currency
from exceptions import ExchangeRateNotFoundException, ExchangeAlreadyExistsException


class ExchangeRepo(BaseRepo):
    def get_all_exchanges(self) -> ExchangeList:
        self.cursor.execute(
            "SELECT id, base_currency_id, target_currency_id, rate FROM ExchangeRates"
        )
        rows = self.cursor.fetchall()

        exchanges = []
        for row in rows:
            exchange_id, base_currency_id, target_currency_id, rate = row

            self.cursor.execute(
                "SELECT id, code, name, sign FROM Currencies WHERE id = ?",
                (base_currency_id,),
            )
            base_currency_data = self.cursor.fetchone()
            base_currency = Currency(*base_currency_data)

            self.cursor.execute(
                "SELECT id, code, name, sign FROM Currencies WHERE id = ?",
                (target_currency_id,),
            )
            target_currency_data = self.cursor.fetchone()
            target_currency = Currency(*target_currency_data)

            exchange = Exchange(exchange_id, base_currency, target_currency, rate)
            exchanges.append(exchange)

        return ExchangeList(exchanges)

    def get_exchange_by_pair(
        self, base_currency: Currency, target_currency: Currency
    ) -> Exchange:
        self.cursor.execute(
            "SELECT id, rate FROM ExchangeRates WHERE base_currency_id = ? AND target_currency_id = ?",
            (base_currency.id, target_currency.id),
        )
        row = self.cursor.fetchone()
        if not row:
            raise ExchangeRateNotFoundException(
                f"Exchange rate for pair {base_currency.code}{target_currency.code} not found"
            )
        exchange_id, rate = row
        return Exchange(exchange_id, base_currency, target_currency, rate)

    def add_exchange(
        self, base_currency: Currency, target_currency: Currency, rate: float
    ) -> Exchange:
        self.cursor.execute(
            "SELECT COUNT(*) FROM ExchangeRates WHERE base_currency_id = ? AND target_currency_id = ?",
            (base_currency.id, target_currency.id),
        )
        if self.cursor.fetchone()[0] > 0:
            raise ExchangeAlreadyExistsException(
                f"Exchange rate from {base_currency.code} to {target_currency.code} already exists."
            )

        self.cursor.execute(
            "INSERT INTO ExchangeRates (base_currency_id, target_currency_id, rate) VALUES (?, ?, ?)",
            (base_currency.id, target_currency.id, rate),
        )
        return Exchange(None, base_currency, target_currency, rate)

    def update_exchange(self, exchange: Exchange, rate: float) -> Exchange:
        self.cursor.execute(
            "UPDATE ExchangeRates SET rate = ? WHERE id = ?", (rate, exchange.id)
        )
        return Exchange(
            exchange.id, exchange.base_currency, exchange.target_currency, rate
        )
