import sqlite3

def insert_test_data():
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()

        currencies = [
            ('USD', 'United States Dollar', '$'),
            ('EUR', 'Euro', '€'),
            ('JPY', 'Japanese Yen', '¥')
        ]
        cursor.executemany("INSERT INTO Currencies (code, full_name, sign) VALUES (?, ?, ?)", currencies)

        cursor.execute("SELECT id FROM Currencies WHERE code = 'USD'")
        usd_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM Currencies WHERE code = 'EUR'")
        eur_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM Currencies WHERE code = 'JPY'")
        jpy_id = cursor.fetchone()[0]

        exchange_rates = [
            (usd_id, eur_id, 0.85),
            (usd_id, jpy_id, 110.01),
            (eur_id, jpy_id, 129.53)
        ]
        cursor.executemany("INSERT INTO ExchangeRates (base_currency_id, target_currency_id, rate) VALUES (?, ?, ?)", exchange_rates)

        conn.commit()

if __name__ == "__main__":
    insert_test_data()