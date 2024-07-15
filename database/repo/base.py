from database.db_manager import DatabaseManager


class BaseRepo:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
