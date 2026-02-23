import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

@st.cache_data
def load_data():
    product_sales_df = pd.read_csv("all_data.csv")
    customers_df = pd.read_csv("customers_dataset.csv")
    geolocation_df = pd.read_csv("geolocation_dataset.csv")
    return product_sales_df, customers_df, geolocation_df

product_sales_df, customers_df, geolocation_df = load_data()


st.title("Dashboard Analisis E-Commerce Olist")

with st.sidebar:
    st.title("Olist E-Commerce")
    st.write("Dashboard ini menganalisis performa penjualan produk dan demografi pelanggan di Brazil.")
    st.caption("Dibuat oleh: Salvathore Verrer Vijaya Lim")

st.subheader("Performa Penjualan Kategori Produk")
category_sales = product_sales_df.groupby("category_name")["order_id"].nunique().sort_values(ascending=False).reset_index()
category_sales.columns = ["category_name", "sales_count"]
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

sns.barplot(x="sales_count", y="category_name", data=category_sales.head(5), palette=colors, ax=ax[0], hue="category_name", legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Terjual", fontsize=15)
ax[0].set_title("5 Kategori Produk Paling Laris", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

bottom_5_categories = category_sales.sort_values(by="sales_count", ascending=True).head(5)
sns.barplot(x="sales_count", y="category_name", data=bottom_5_categories, palette=colors, ax=ax[1], hue="category_name", legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Terjual", fontsize=15)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("5 Kategori Produk Paling Sedikit Terjual", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
st.pyplot(fig)


st.markdown("---")
st.subheader("Demografi Persebaran Lokasi Pelanggan Olist E-Commerce")
bystate_df = customers_df.groupby(by="customer_state")['customer_unique_id'].nunique().reset_index()
bystate_df.columns = ['negara_bagian', 'jumlah_pelanggan']
bystate_df = bystate_df.sort_values(by="jumlah_pelanggan", ascending=False)
bycity_df = customers_df.groupby(by="customer_city")['customer_unique_id'].nunique().reset_index()
bycity_df.columns = ['kota', 'jumlah_pelanggan']
bycity_df = bycity_df.sort_values(by="jumlah_pelanggan", ascending=False)

fig2, ax2 = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors2 = ["#72BCD4"] + ["#D3D3D3"] * 9

sns.barplot(x="jumlah_pelanggan", y="negara_bagian", data=bystate_df.head(10), palette=colors2, ax=ax2[0], hue="negara_bagian", legend=False)
ax2[0].set_ylabel(None)
ax2[0].set_xlabel("Jumlah Pelanggan", fontsize=15)
ax2[0].set_title("Top 10 Negara Bagian (State)", loc="center", fontsize=18)

sns.barplot(x="jumlah_pelanggan", y="kota", data=bycity_df.head(10), palette=colors2, ax=ax2[1], hue="kota", legend=False)
ax2[1].set_ylabel(None)
ax2[1].set_xlabel("Jumlah Pelanggan", fontsize=15)
ax2[1].invert_xaxis()
ax2[1].yaxis.set_label_position("right")
ax2[1].yaxis.tick_right()
ax2[1].set_title("Top 10 Kota (City)", loc="center", fontsize=18)
st.pyplot(fig2)

st.markdown("---")
st.subheader("Geospatial Analysis: Peta Kepadatan Pelanggan")
geo_brazil = geolocation_df[
    (geolocation_df['geolocation_lat'] <= 5.27438888) &
    (geolocation_df['geolocation_lat'] >= -33.75116944) &
    (geolocation_df['geolocation_lng'] <= -34.79314722) &
    (geolocation_df['geolocation_lng'] >= -73.98283055)
]
geo_sample = geo_brazil.sample(n=10000, random_state=42)
brazil_map = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles='OpenStreetMap')
heat_data = [[row['geolocation_lat'], row['geolocation_lng']] for index, row in geo_sample.iterrows()]
HeatMap(heat_data, radius=15, blur=10).add_to(brazil_map)
st_folium(brazil_map, width=1000, height=500)