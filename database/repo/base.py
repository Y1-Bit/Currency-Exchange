from sqlite3 import Cursor


class BaseRepo:
    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor
