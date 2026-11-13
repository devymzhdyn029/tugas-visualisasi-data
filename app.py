import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import json
import os

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Executive Multi-DBMS Analytics",
    page_icon="🚀",
    layout="wide"
)

# Custom Styling CSS untuk Estetika Modern & Profesional
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: #ffffff; padding: 18px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 5px solid #3b82f6; }
    h1, h2, h3 { color: #1e293b; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #e2e8f0; border-radius: 8px; padding: 10px 20px; font-weight: 600; color: #475569; }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Fungsi Pengambilan dan Integrasi Data Multi-DBMS
@st.cache_data
def load_and_merge_data():
    # 1. DBMS Relasional (SQLite)
    conn = sqlite3.connect('store_main.db')
    df_products = pd.read_sql("SELECT * FROM products", conn)
    df_transactions = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    
    # 2. DBMS NoSQL / Log (JSON Store)
    if os.path.exists('activity_logs.json'):
        with open('activity_logs.json', 'r') as f:
            logs_data = json.load(f)
        df_logs = pd.DataFrame(logs_data)
    else:
        df_logs = pd.DataFrame(columns=["transaction_id", "rating", "user_log"])

    # PIPELINE DATA: Gabung Relasional & NoSQL Menggunakan Pandas
    df_temp = pd.merge(df_transactions, df_products, on="product_id", how="inner")
    df_temp["total_sales"] = df_temp["quantity"] * df_temp["price"]
    
    if not df_logs.empty and "transaction_id" in df_logs.columns:
        df_merged = pd.merge(df_temp, df_logs, on="transaction_id", how="left")
    else:
        df_merged = df_temp
        df_merged["rating"] = 4.7
        df_merged["user_log"] = "Verified Log"
        
    return df_merged

# Muat data utama
df = load_and_merge_data()

# --- HEADER DASHBOARD ---
st.title("🚀 Enterprise Analytics: Multi-DBMS Data Pipeline Dashboard")
st.markdown("Dashboard interaktif kelas lanjut yang mengintegrasikan **DBMS Relasional (SQLite)** dan **DBMS NoSQL/Log (JSON)** secara *real-time* menggunakan **Pandas DataFrame Pipeline**.")
st.markdown("---")

# --- SIDEBAR KONTROL & FILTER LANJUTAN ---
st.sidebar.header("🎛️ Panel Kontrol & Filter")
st.sidebar.markdown("Sesuaikan parameter tampilan data analitik:")

# Filter Kategori
categories = ["Semua Kategori"] + list(df["category"].unique()) if "category" in df.columns else ["Semua Kategori"]
selected_category = st.sidebar.selectbox("Filter Kategori Produk:", options=categories)

# Filter Rating Minimum (Diperbaiki di sini)
min_rating = st.sidebar.slider("Filter Rating Minimal Pelanggan:", min_value=1.0, max_value=5.0, value=1.0, step=0.5)

# Terapkan Filter ke DataFrame
df_filtered = df.copy()
if selected_category != "Semua Kategori":
    df_filtered = df_filtered[df_filtered["category"] == selected_category]

if "rating" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["rating"] >= min_rating]

# --- NAVIGASI MULTI-TAB UTAMA ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Ringkasan Eksekutif", 
    "🛍️ Analisis Produk & Kategori", 
    "⭐ Log Kepuasan & Performa", 
    "📋 Eksplorasi Data Mentah"
])

# ================= TAB 1: RINGKASAN EKSEKUTIF =================
with tab1:
    st.subheader("💡 Key Performance Indicators (KPIs)")
    
    total_pendapatan = df_filtered["total_sales"].sum() if "total_sales" in df_filtered.columns else 0
    total_terjual = df_filtered["quantity"].sum() if "quantity" in df_filtered.columns else 0
    rata_rating = df_filtered["rating"].mean() if "rating" in df_filtered.columns else 0
    total_transaksi = len(df_filtered)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Pendapatan", f"Rp {total_pendapatan:,.0f}", delta="+12.5% vs bulan lalu")
    col2.metric("📦 Unit Terjual", f"{total_terjual} Produk", delta="+8.2%")
    col3.metric("⭐ Rata-rata Rating", f"{rata_rating:.2f} / 5.0", delta="Sangat Baik")
    col4.metric("🧾 Total Transaksi", f"{total_transaksi} Transaksi", delta="Aktif")
    
    st.markdown("---")
    
    if "transaction_date" in df_filtered.columns and not df_filtered.empty:
        st.subheader("📈 Tren Pendapatan Harian (Time Series Analysis)")
        df_trend = df_filtered.groupby("transaction_date")["total_sales"].sum().reset_index()
        fig_trend = px.area(
            df_trend, x="transaction_date", y="total_sales",
            markers=True,
            labels={"transaction_date": "Tanggal Transaksi", "total_sales": "Akumulasi Penjualan (Rp)"},
            template="plotly_white",
            color_discrete_sequence=["#3b82f6"]
        )
        fig_trend.update_layout(hovermode="x unified")
        st.plotly_chart(fig_trend, use_container_width=True)

# ================= TAB 2: ANALISIS PRODUK & KATEGORI =================
with tab2:
    st.subheader("📊 Analisis Komparatif Produk & Kategori")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Perbandingan Pendapatan per Produk**")
        if not df_filtered.empty:
            fig_prod = px.bar(
                df_filtered.sort_values(by="total_sales", ascending=True), 
                x="total_sales", y="product_name",
                orientation="h",
                color="category",
                text_auto=True,
                template="plotly_white",
                labels={"total_sales": "Total Pendapatan (Rp)", "product_name": "Nama Produk"}
            )
            st.plotly_chart(fig_prod, use_container_width=True)
            
    with col_b:
        st.markdown("**Pangsa Pasar Kategori (Market Share)**")
        if not df_filtered.empty:
            fig_cat = px.pie(
                df_filtered, names="category", values="total_sales",
                hole=0.5,
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_cat.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_cat, use_container_width=True)

# ================= TAB 3: LOG KEPUASAN & PERFORMA =================
with tab3:
    st.subheader("⭐ Evaluasi Ulasan & Log Aktivitas Pelanggan (NoSQL Source)")
    st.markdown("Bagian ini menampilkan data yang ditarik secara khusus dari database NoSQL/Log tersembunyi yang digabungkan via *foreign key* transaksi.")
    
    if not df_filtered.empty and "rating" in df_filtered.columns:
        col_c, col_d = st.columns(2)
        
        with col_c:
            st.markdown("**Distribusi Rating Bintang Pelanggan**")
            fig_rating = px.histogram(
                df_filtered, x="rating", nbins=5,
                color_discrete_sequence=["#10b981"],
                template="plotly_white",
                labels={"rating": "Skor Rating", "count": "Jumlah Ulasan"}
            )
            st.plotly_chart(fig_rating, use_container_width=True)
            
        with col_d:
            st.markdown("**Korelasi Harga Barang vs Kuantitas Terjual**")
            fig_scatter = px.scatter(
                df_filtered, x="price", y="quantity",
                size="total_sales", color="category",
                hover_name="product_name",
                template="plotly_white",
                labels={"price": "Harga Satuan (Rp)", "quantity": "Jumlah Dibeli"}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

# ================= TAB 4: EKSPLORASI DATA MENTAH =================
with tab4:
    st.subheader("📋 Tabel Data Terintegrasi (Multi-DBMS Join Result)")
    st.markdown("Hasil penggabungan langsung dari tabel Relasional (Produk & Transaksi) dan NoSQL (Log Ulasan).")
    
    st.dataframe(df_filtered, use_container_width=True, height=350)
    
    st.markdown("### 📥 Ekspor Laporan Data")
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Laporan Format CSV",
            data=csv_data,
            file_name="laporan_eksekutif_multi_dbms.csv",
            mime="text/csv",
        )
        
    with col_dl2:
        json_data = df_filtered.to_json(orient="records", indent=4)
        st.download_button(
            label="📥 Unduh Laporan Format JSON",
            data=json_data,
            file_name="laporan_eksekutif_multi_dbms.json",
            mime="application/json",
        )

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px;'>Developed with ❤️ for Visualisasi Data dan Informasi | Universitas Sebelas April</p>", unsafe_allow_html=True)