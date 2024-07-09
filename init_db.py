import sqlite3

def create_tables():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Currencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        sign TEXT NOT NULL
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ExchangeRates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_currency_id INTEGER NOT NULL,
            target_currency_id INTEGER NOT NULL,
            rate NUMERIC(10, 6) NOT NULL,
            FOREIGN KEY (base_currency_id) REFERENCES Currencies (id),
            FOREIGN KEY (target_currency_id) REFERENCES Currencies (id),
            UNIQUE (base_currency_id, target_currency_id)
        )
        """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
