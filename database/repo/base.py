from sqlite3 import Connection


class BaseRepo:
    def __init__(self, connection: Connection):
        self.connection = connection
