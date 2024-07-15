import sqlite3
from contextlib import closing, contextmanager


class DatabaseManager:
    def __init__(self, dbname: str):
        self.dbname = dbname
        self.conn = None

    def connect(self):
        if self.conn is None or self.conn:
            self.conn = sqlite3.connect(self.dbname)
        return self

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    @contextmanager
    def transaction(self):
        if self.conn is None:
            raise ValueError("Connection is not established.")

        with self.conn, closing(self.conn.cursor()) as cursor:
            yield cursor
