# Multi-DBMS Data Pipeline & Web Visualization

## Arsitektur Sistem
* **DBMS 1 (SQLite):** Menyimpan data master produk dan transaksi penjualan.
* **DBMS 2 (JSON Log):** Menyimpan data ulasan dan rating pengguna.
* **Data Pipeline:** Menggunakan Pandas untuk menggabungkan tabel relasional dan data log berdasarkan `product_id`.

## Cara Menjalankan
1. Install library: `pip install -r requirements.txt`
2. Generate database: `python database/seed_data.py`
3. Jalankan aplikasi: `streamlit run app.py`