# Multi-DBMS E-Commerce Analytics Dashboard

Aplikasi web analitik interaktif yang dibangun menggunakan Python dan Streamlit untuk mengintegrasikan, memproses, dan memvisualisasikan data dari dua arsitektur database yang berbeda (DBMS Relasional dan DBMS NoSQL/Log) secara real-time.

---

## 1. Identitas Mahasiswa
- Nama: Lengkap: Devy Muzahidyn
- NIM: 230660121172
- Kelas: IF-VIIB

---

## 2. Daftar Tautan Utama
- URL Live Web Application: https://tugas-visualisasi-datagit-bxwbzsnz95dftoj5fhh4af.streamlit.app
- URL Repositori GitHub: https://github.com/devymzhdyn029/tugas-visualisasi-data
- Sumber Data Asli: Custom Synthetic E-Commerce Dataset — Dataset sampel tiruan terstruktur yang di-generate secara lokal menggunakan skrip inisialisasi Python (database/seed_data.py) ke dalam database SQLite (store_main.db) dan dokumen log JSON (activity_logs.json).
- URL Referensi Kode & Dokumentasi:
  - Dokumentasi Resmi Streamlit: https://docs.streamlit.io
  - Dokumentasi Plotly Express Python: https://plotly.com/python/plotly-express/
  - Dokumentasi Pandas DataFrame Merge: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html

---

## 3. Ringkasan Arsitektur Sistem
Proyek ini menerapkan pola arsitektur Multi-DBMS Data Pipeline yang memisahkan penyimpanan data transaksional terstruktur dengan data log aktivitas pelanggan yang bersifat semi-terstruktur.

1. DBMS 1 — Relational Database (SQLite)
   - File / Skema: store_main.db & database/schema.sql
   - Fungsi: Menyimpan data master produk (products) dan catatan transaksi penjualan (transactions).
   - Engine: SQLite (diakses melalui modul standar sqlite3 Python) untuk menjaga konsistensi skema tabel dan integritas referensial melalui relasi Primary Key dan Foreign Key (product_id).

2. DBMS 2 — NoSQL / Document Store (JSON Log)
   - File: activity_logs.json
   - Fungsi: Menyimpan catatan log aktivitas pengguna, ulasan teks (user_log), serta skor penilaian (rating) tiap transaksi.
   - Engine: Penyimpanan dokumen berbasis JSON yang merepresentasikan karakteristik database NoSQL berorientasi dokumen yang fleksibel tanpa skema tabel kaku.

---

## 4. Alur Integrasi (Data Pipeline)
Penggabungan data lintas DBMS dilakukan di sisi aplikasi menggunakan pustaka Pandas:
- Extract (Ekstraksi): Mengambil tabel products dan transactions dari DBMS SQLite menggunakan kueri SQL (pd.read_sql), serta memuat dokumen JSON dari activity_logs.json ke dalam struktur DataFrame.
- Transform & Join (Transformasi & Penggabungan): Melakukan inner join (pd.merge) antara tabel transaksi dan produk berdasarkan kunci product_id, menghitung metrik turunan total_sales (quantity * price), serta melakukan left join dengan log NoSQL berdasarkan kunci transaction_id untuk menyatukan data transaksi dengan ulasan pelanggan.
- Load & Visualize (Pemuatan & Visualisasi): Data terintegrasi di-cache menggunakan @st.cache_data dan disajikan ke antarmuka dashboard interaktif.

---

## 5. Fitur Interaktivitas Antarmuka Visualisasi
- Navigasi Multi-Tab: Membagi tampilan analitik menjadi 4 tab terstruktur (Ringkasan Eksekutif, Analisis Produk & Kategori, Log Kepuasan & Performa, dan Eksplorasi Data Mentah).
- Panel Kontrol & Filter Dinamis: Sidebar interaktif untuk menyaring data secara real-time berdasarkan Kategori Produk dan Rating Minimal Pelanggan.
- KPI Metrics Cards: Menampilkan ringkasan metrik utama (Total Pendapatan, Unit Terjual, Rata-rata Rating, dan Total Transaksi).
- Visualisasi Grafik Interaktif (Plotly): Area chart untuk tren harian, horizontal bar chart untuk perbandingan produk, donut chart untuk pangsa pasar, serta histogram dan scatter plot untuk analisis korelasi.
- Ekspor Laporan Data: Fitur pengunduhan langsung hasil filter tabel terintegrasi ke dalam format CSV dan JSON.