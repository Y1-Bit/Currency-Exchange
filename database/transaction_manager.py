from sqlite3 import Connection, Cursor


class TransactionManager:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.cursor: Cursor | None = None

    def __enter__(self) -> Cursor:
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: BaseException | None,
    ) -> None:
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        if self.cursor:
            self.cursor.close()
