import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    data = pd.read_csv("all_data.csv")
    return data

data = load_data()

# Set up Streamlit app
st.title("Proyek Analisis Data: E-Commerce Public Dataset")

# Pertanyaan 1 : Kategori produk apa yang paling banyak dan paling sedikit terjual/dibeli?
st.header("Pertanyaan 1 : Kategori produk apa yang paling banyak dan paling sedikit terjual/dibeli?")
category_orders = data["product_category_name_english"].value_counts()

# 5 kategori produk dengan penjualan tertinggi
top_5_categories = category_orders.head(5)
# 5 kategori produk dengan penjualan terendah
bottom_5_categories = category_orders.tail(5).sort_values()

col1, col2 = st.columns(2)
with col1:
    st.subheader("5 Kategori product tertinggi")
    fig, ax = plt.subplots()
    sns.barplot(x=top_5_categories.values, y=top_5_categories.index, palette="coolwarm", ax=ax)
    ax.set_title("5 kategori produk dengan penjualan tertinggi")
    ax.set_xlabel("Order Count")
    st.pyplot(fig)

with col2:
    st.subheader("5 Kategori product terendah")
    fig, ax = plt.subplots()
    sns.barplot(x=bottom_5_categories.values, y=bottom_5_categories.index, palette="coolwarm", ax=ax)
    ax.set_title("5 kategori produk dengan penjualan terendah")
    ax.set_xlabel("Order Count")
    st.pyplot(fig)

# Question 2: Sales and Revenue Performance in 2017
st.header("Bagaimana Performa Penjualan dan Revenue Perusahaan pada tahun 2017? Apakah terdapat pola atau tren tertentu?")

# Use the correct column name for order dates
data["order_purchase_timestamp"] = pd.to_datetime(data["order_purchase_timestamp"])

# Filter data for 2017
data_2017 = data[data["order_purchase_timestamp"].dt.year == 2017]
data_2017["Month"] = data_2017["order_purchase_timestamp"].dt.month

# Group by month
monthly_performance = data_2017.groupby("Month").agg({"price": "sum", "payment_value": "sum"})

# Plot sales and revenue
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_performance.index, monthly_performance["price"], label="Sales", marker="o")
ax.plot(monthly_performance.index, monthly_performance["payment_value"], label="Revenue", marker="o", linestyle="--")
ax.set_xticks(range(1, 13))
ax.set_xticklabels([
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
], rotation=45)
ax.set_title("Sales and Revenue Performance (2017)")
ax.set_xlabel("Month")
ax.set_ylabel("Amount ($)")
ax.legend()
st.pyplot(fig)

st.write("Jumlah pesanan dan revenue pada tahun 2017 secara garis besar mengalami kenaikan. Penurunan pesanan hanya terjadi pada bulan April, Juni dan Desember, sedangkan untuk penurunan revenue terjadi pada bulan Aprl, Juni, dan Desember. Berdasarkan grafik diatas dapat disimpulkan bahwa penurunan jumlah pesanan dapat memengaruhi pendapatan (pendapatan juga ikut turun). Penurunan tersebut bisa terjadi kemungkinan karena faktor pasar maupun musim.")
