import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "instant": "order_count",
        "cnt": "Totalcust"
    }, inplace=True)
    
    return daily_orders_df

def create_season_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().sort_values(ascending=False).reset_index()
    return byseason_df

def create_byyr_df(df):
    byyr_df = df.groupby(by="yr").instant.nunique().reset_index()
    byyr_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
def create_byyr_season_df(df):
    byyr_season_df = df.groupby(by=["season", "yr"]).cnt.sum().sort_values(ascending=False).reset_index()
    return byyr_season_df

def create_bymnth_df(df):
    bymnth_df = df.groupby(by="mnth").instant.nunique().reset_index()
    bymnth_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return bymnth_df
def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byweathersit_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return byweathersit_df

# belum by windspeed, hum temp

all_df = pd.read_csv("https://raw.githubusercontent.com/Azfat/proyek_akhir_kelas/main/day_data.csv")

# Menampilkan nama-nama kolom di DataFrame

all_df.sort_values(by="dteday", inplace=True)
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

# Membuat filter berdasarkan tanggal
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
byseason_df = create_season_df(all_df)
byyr_season_df = create_byyr_season_df(all_df)
mnth_df = create_bymnth_df(main_df)
yr_df = create_byyr_df(main_df)
weathersit_df = create_byweathersit_df(main_df)

st.header('Bike Sharing Dataset University of Porto Portugal :sparkles:')

# Membuat visualisasi penyewa sepeda harian berdasarkan filter
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    banyak_hari = daily_orders_df.order_count.sum()
    st.metric("Banyak hari", value=banyak_hari)
 
with col2:
    total_tenant = daily_orders_df.Totalcust.sum()
    st.metric("Total Tenant", value=total_tenant)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["Totalcust"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Membuat visualisasi tren harian pengguna sepeda

st.subheader("Grafik tren penyewa sepeda harian")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    all_df["dteday"],
    all_df["cnt"], 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# visualiasi banyaknya penyewa sepeda berdasarkan musim keseluruhan
st.subheader("Penyewa sepeda berdasarkan musim")
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax = plt.subplots(figsize=(35, 15))

sns.barplot(
    y="cnt", 
    x="season",
    data=byseason_df.sort_values(by="cnt", ascending=False),
    palette=colors
)

plt.title("Banyak penyewa berdasarkan musim", loc="center", fontsize=50)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# visualisasi banyaknya penyewa sepeda berdasarkan musim pertahunnya

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="season", y="cnt", data=byyr_season_df[byyr_season_df["yr"] == 0], palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Musim", fontsize=30)
ax[0].set_title("Data Tahun 2011", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="season", y="cnt", data=byyr_season_df[byyr_season_df["yr"] == 1], palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Musim", fontsize=30)
ax[1].set_title("Data Tahun 2012", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

# menampilkan visualisasi korelasi antara banyaknya peminjam sepeda dengan temperatur

st.subheader("Korelasi tingkat penyewa sepeda dengan temperatur lingkungan")
korelasi = all_df["temp"].corr(all_df["cnt"])
st.write(f"Nilai korelasi antara temperatur dan banyak penyewa sepeda: {korelasi}")

fig, ax = plt.subplots(figsize=(20, 15))

sns.regplot(
    y="cnt", 
    x="temp",
    data=all_df
)

plt.title("Korelasi temperatur dan penyewa sepeda", loc="center", fontsize=50)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# menampilkan visualisasi korelasi antara banyaknya peminjam sepeda dengan temperatur

st.subheader("Korelasi tingkat penyewa sepeda dengan temperatur yang dirasa")
korelasi_atemp = all_df["atemp"].corr(all_df["cnt"])
st.write(f"Nilai korelasi antara temperatur yang dirasa dan banyak penyewa sepeda: {korelasi_atemp}")

fig, ax = plt.subplots(figsize=(20, 15))

sns.regplot(
    y="cnt", 
    x="atemp",
    data=all_df
)

plt.title("Korelasi temperatur yang dirasa dan penyewa sepeda", loc="center", fontsize=50)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# menampilkan visualisasi korelasi antara banyaknya peminjam sepeda dengan kelembapan udara

st.subheader("Korelasi tingkat penyewa sepeda dengan kelembapan udara")
korelasi_hum = all_df["hum"].corr(all_df["cnt"])
st.write(f"Nilai korelasi antara kelembapan udara dan banyak penyewa sepeda: {korelasi_hum}")

fig, ax = plt.subplots(figsize=(20, 15))

sns.regplot(
    y="cnt", 
    x="hum",
    data=all_df
)

plt.title("Korelasi kelembapan udara dan penyewa sepeda", loc="center", fontsize=50)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# menampilkan visualisasi korelasi antara banyaknya peminjam sepeda dengan kecepatan angin

st.subheader("Korelasi tingkat penyewa sepeda dengan kecepatan angin")
korelasi_windspeed = all_df["windspeed"].corr(all_df["cnt"])
st.write(f"Nilai korelasi antara kecepatan angin dan banyak penyewa sepeda: {korelasi_windspeed}")

fig, ax = plt.subplots(figsize=(20, 15))

sns.regplot(
    y="cnt", 
    x="windspeed",
    data=all_df
)

plt.title("Korelasi windspeed dan penyewa sepeda", loc="center", fontsize=50)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)

st.pyplot(fig)
