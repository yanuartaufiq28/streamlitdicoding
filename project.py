import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    data = pd.read_csv("all_data.csv")
    data["order_purchase_timestamp"] = pd.to_datetime(data["order_purchase_timestamp"])
    return data

data = load_data()

# Sidebar for date filtering
st.sidebar.header("Filter Data Berdasarkan Tanggal")
default_start_date = pd.to_datetime("2017-01-01").date()
default_end_date = pd.to_datetime("2017-12-31").date()
start_date = st.sidebar.date_input("Tanggal Mulai", default_start_date)
end_date = st.sidebar.date_input("Tanggal Akhir", default_end_date)

# Filter data berdasarkan tanggal
filtered_data = data[(data["order_purchase_timestamp"].dt.date >= start_date) & (data["order_purchase_timestamp"].dt.date <= end_date)]

# Set up Streamlit app
st.title("Proyek Analisis Data: E-Commerce Public Dataset")

# Pertanyaan 1 : Kategori produk apa yang paling banyak dan paling sedikit terjual/dibeli?
st.header("Pertanyaan 1 : Kategori produk apa yang paling banyak dan paling sedikit terjual/dibeli?")
category_orders = filtered_data["product_category_name_english"].value_counts()

# 5 kategori produk dengan penjualan tertinggi
top_5_categories = category_orders.head(5)
# 5 kategori produk dengan penjualan terendah
bottom_5_categories = category_orders.tail(5).sort_values()

col1, col2 = st.columns(2)
with col1:
    st.subheader("5 Kategori produk tertinggi")
    fig, ax = plt.subplots()
    sns.barplot(x=top_5_categories.values, y=top_5_categories.index, palette="coolwarm", ax=ax)
    ax.set_title("5 kategori produk dengan penjualan tertinggi")
    ax.set_xlabel("Order Count")
    st.pyplot(fig)

with col2:
    st.subheader("5 Kategori produk terendah")
    fig, ax = plt.subplots()
    sns.barplot(x=bottom_5_categories.values, y=bottom_5_categories.index, palette="coolwarm", ax=ax)
    ax.set_title("5 kategori produk dengan penjualan terendah")
    ax.set_xlabel("Order Count")
    st.pyplot(fig)

# Question 2: Sales and Revenue Performance
st.header("Bagaimana Performa Penjualan dan Revenue Perusahaan?")

# Filter data untuk tahun yang dipilih
filtered_data["Month"] = filtered_data["order_purchase_timestamp"].dt.month
monthly_performance = filtered_data.groupby("Month").agg({"price": "sum", "payment_value": "sum"})

# Plot sales and revenue
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_performance.index, monthly_performance["price"], label="Sales", marker="o")
ax.plot(monthly_performance.index, monthly_performance["payment_value"], label="Revenue", marker="o", linestyle="--")
ax.set_xticks(range(1, 13))
ax.set_xticklabels([
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
], rotation=45)
ax.set_title("Sales and Revenue Performance")
ax.set_xlabel("Month")
ax.set_ylabel("Amount ($)")
ax.legend()
st.pyplot(fig)

st.write("Jumlah pesanan dan revenue mengalami perubahan berdasarkan rentang tanggal yang dipilih. Dengan analisis lebih lanjut, kita dapat menentukan pola atau tren yang muncul pada periode tertentu.")
