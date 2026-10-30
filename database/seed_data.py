import sqlite3
import json

def init_dbs():
    # Membuat DBMS 1 (SQLite - Relasional)
    conn = sqlite3.connect('store_main.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT, price REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (transaction_id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER, transaction_date TEXT)''')
    
    # Masukkan data contoh produk & transaksi
    cursor.executemany('INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)', [
        (1, 'Laptop Gaming', 'Electronics', 15000000),
        (2, 'Mechanical Keyboard', 'Accessories', 750000),
        (3, 'Office Chair', 'Furniture', 2000000),
        (4, 'Wireless Mouse', 'Accessories', 300000)
    ])
    
    cursor.executemany('INSERT OR REPLACE INTO transactions VALUES (?, ?, ?, ?)', [
        (101, 1, 2, '2026-05-01'),
        (102, 2, 5, '2026-05-02'),
        (103, 3, 1, '2026-05-03'),
        (104, 4, 10, '2026-05-03'),
        (105, 1, 1, '2026-05-04')
    ])
    conn.commit()
    conn.close()

    # Membuat DBMS 2 (Simulasi NoSQL / JSON Log untuk Ulasan)
    reviews_data = [
        {"product_id": 1, "rating": 4.8, "user_log": "Sangat cepat dan mulus"},
        {"product_id": 2, "rating": 4.5, "user_log": "Empuk tombolnya"},
        {"product_id": 3, "rating": 4.2, "user_log": "Nyaman buat kerja lama"},
        {"product_id": 4, "rating": 4.6, "user_log": "Responsif"}
    ]
    with open('activity_logs.json', 'w') as f:
        json.dump(reviews_data, f)

if __name__ == '__main__':
    init_dbs()
    print("Database & Data Berhasil Dibuat!")