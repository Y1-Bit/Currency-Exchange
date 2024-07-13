from database.db_manager import DatabaseManager
from database.repo.requests import RequestsRepo


def create_tables(repo: RequestsRepo):
    with repo.db_manager.transaction() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Currencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                sign TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ExchangeRates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base_currency_id INTEGER NOT NULL,
                target_currency_id INTEGER NOT NULL,
                rate NUMERIC(10, 6) NOT NULL,
                FOREIGN KEY (base_currency_id) REFERENCES Currencies (id),
                FOREIGN KEY (target_currency_id) REFERENCES Currencies (id),
                UNIQUE (base_currency_id, target_currency_id)
            )
            """
        )
        if repo.db_manager.conn is not None:
            repo.db_manager.conn.commit()

def insert_test_data(repo: RequestsRepo):
    with repo.db_manager.transaction() as cursor:
        currencies = [
            ("USD", "United States dollar", "$"),
            ("EUR", "Euro", "€"),
            ("AUD", "Australian dollar", "A$"),
        ]

        cursor.executemany(
            "INSERT INTO Currencies (code, name, sign) VALUES (?, ?, ?)", currencies
        )

        exchange_rates = [
            (1, 2, 0.99),  # USD to EUR
            (1, 3, 1.45),  # USD to AUD
            (2, 3, 1.60),  # EUR to AUD
        ]

        cursor.executemany(
            "INSERT INTO ExchangeRates (base_currency_id, target_currency_id, rate) VALUES (?, ?, ?)",
            exchange_rates,
        )

        if repo.db_manager.conn is not None:
            repo.db_manager.conn.commit()

def main() -> None:
    db_manager = DatabaseManager('database.db')
    repo = RequestsRepo(db_manager)
    create_tables(repo)
    insert_test_data(repo)

if __name__ == "__main__":
    main()