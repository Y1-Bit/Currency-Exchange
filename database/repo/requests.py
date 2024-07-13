from database.db_manager import DatabaseManager
from database.repo.currency import CurrencyRepo


class RequestsRepo:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    @property
    def currency(self) -> CurrencyRepo:
        return CurrencyRepo(self.db_manager)