from sqlite3 import Connection

from database.repo.currency import CurrencyRepo


class RequestsRepo:
    def __init__(self):
        self._connection = None

    def set_connection(self, connection: Connection):
        self._connection = connection   
    
    @property
    def connection(self) -> Connection:
        if self._connection is None:
            raise ValueError("Connection is not set")
        return self._connection

    @property
    def currency(self) -> CurrencyRepo:
        return CurrencyRepo(self.connection)