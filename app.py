import streamlit as st
import sqlite3
import json
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Multi-DBMS Dashboard", layout="wide")

@st.cache_data
def load_data():
    # 1. Ambil data dari DBMS 1 (SQLite)
    conn = sqlite3.connect('store_main.db')
    df_products = pd.read_sql("SELECT * FROM products", conn)
    df_transactions = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    
    # 2. Ambil data dari DBMS 2 (NoSQL / JSON Log)
    with open('activity_logs.json', 'r') as f:
        logs_data = json.load(f)
    df_logs = pd.DataFrame(logs_data)
    
    # 3. Data Pipeline / Integrasi (Join data menggunakan Pandas)
    df_merged = df_transactions.merge(df_products, on="product_id", how="left")
    df_final = df_merged.merge(df_logs, on="product_id", how="left")
    
    df_final['total_sales'] = df_final['quantity'] * df_final['price']
    return df_final

df = load_data()

st.title("📊 Dashboard Multi-DBMS E-Commerce")
st.markdown("Aplikasi ini menggabungkan data dari **DBMS Relasional (SQLite)** dan **DBMS NoSQL/Log (JSON)** menggunakan **Pandas**.")

# Filter di Sidebar
selected_category = st.sidebar.selectbox("Pilih Kategori", options=["Semua"] + list(df['category'].unique()))
filtered_df = df if selected_category == "Semua" else df[df['category'] == selected_category]

# Metrik Atas
col1, col2, col3 = st.columns(3)
col1.metric("Total Pendapatan", f"Rp {filtered_df['total_sales'].sum():,.0f}")
col2.metric("Total Terjual", int(filtered_df['quantity'].sum()))
col3.metric("Rata-rata Rating", round(filtered_df['rating'].mean(), 2))

st.divider()

# Grafik 1
st.subheader("📈 Pendapatan Berdasarkan Produk")
fig_sales = px.bar(filtered_df, x='product_name', y='total_sales', color='category', text_auto=True)
st.plotly_chart(fig_sales, use_container_width=True)

# Tabel Data Gabungan
st.subheader("📋 Tabel Data Hasil Integrasi Multi-DBMS")
st.dataframe(filtered_df)