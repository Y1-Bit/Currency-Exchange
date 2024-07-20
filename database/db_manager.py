import sqlite3


class DatabaseConnection:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.connection = None

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: BaseException | None) -> None:
        if self.connection:
            self.connection.close()


def connection_maker() -> DatabaseConnection:
    db_path = "database.db"
    return DatabaseConnection(db_path)
