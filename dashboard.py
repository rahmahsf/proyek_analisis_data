import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Analisis Peminjaman Sepeda", page_icon="🚴")

# Load dataset (pastikan merged_df sudah tersedia)
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])  # Konversi kolom tanggal
    return df

merged_df = load_data()

# Judul Aplikasi
st.title("📊 Analisis Peminjaman Sepeda 🚴")

# Sidebar untuk filter interaktif
st.sidebar.header("🔍 Filter Data")

# Filter tanggal
min_date = merged_df["dteday"].min()
max_date = merged_df["dteday"].max()
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

season_mapping = {1:"Spring", 2:"Summer", 3:"Fall",4:"Winter"}
selected_season = st.sidebar.multiselect("Pilih Musim", options=season_mapping.keys(), format_func=lambda x: season_mapping[x], default=list(season_mapping.keys()))

# Filter dataset berdasarkan input pengguna
filtered_df = merged_df[(merged_df["dteday"] >= pd.to_datetime(date_range[0])) & 
                        (merged_df["dteday"] <= pd.to_datetime(date_range[1])) &
                        (merged_df["season"].isin(selected_season))]

# Analisis kontribusi peminjaman per jam
filtered_df['hourly_ratio'] = filtered_df['cnt_hourly'] / filtered_df['cnt_day']
hourly_avg_ratio = filtered_df.groupby('hr')['hourly_ratio'].mean()


st.subheader("📈 Rata-rata Kontribusi Peminjaman Sepeda per Jam terhadap Total Harian")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hourly_avg_ratio.index, y=hourly_avg_ratio.values, marker="o", color="b", ax=ax1)
ax1.set_xticks(range(0, 24))
ax1.set_title("Rata-rata Kontribusi Peminjaman Sepeda per Jam terhadap Total Harian")
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rasio Peminjaman terhadap Total Harian")
ax1.grid()
st.pyplot(fig1)

st.subheader("🌦️ Total Peminjaman Sepeda Berdasarkan musim")

filtered_seasons = sorted(filtered_df["season"].unique())  
filtered_labels = [season_mapping[s] for s in filtered_seasons]


fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(
    x=filtered_df["season"], 
    y=filtered_df["cnt_day"], 
    hue=filtered_df["season"], 
    palette="coolwarm", 
    dodge=False, 
    ax=ax2,
    order=filtered_seasons  
)

ax2.set_xticklabels(filtered_labels)

ax2.set_title("Total Peminjaman Sepeda Berdasarkan musim")
ax2.set_xlabel("Musim")
ax2.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig2)
# Footer
st.markdown("""
---
 **Bike Sharing Analysis** | © 2025 Rahmah Sary Fadiyah  
""")
