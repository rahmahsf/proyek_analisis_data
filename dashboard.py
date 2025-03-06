import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analisis Peminjaman Sepeda", page_icon="🚴")

# Load dataset
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
min_date = merged_df["dteday"].min()
max_date = merged_df["dteday"].max()
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

# Mapping musim
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
selected_season = st.sidebar.multiselect("Pilih Musim", options=season_mapping.keys(), format_func=lambda x: season_mapping[x], default=list(season_mapping.keys()))

# Filter dataset berdasarkan input pengguna
filtered_df = merged_df[
    (merged_df["dteday"] >= pd.to_datetime(date_range[0])) &
    (merged_df["dteday"] <= pd.to_datetime(date_range[1])) &
    (merged_df["season"].isin(selected_season))
]
total_filtered_data = filtered_df.shape[0]

filtered_df['hourly_ratio'] = filtered_df['cnt_hourly'] / filtered_df['cnt_day']
hourly_avg_ratio = filtered_df.groupby('hr')['hourly_ratio'].mean()

st.subheader("📈 Rata-rata Kontribusi Peminjaman Sepeda per Jam terhadap Total Harian")
st.write(f"Total data yang digunakan: **{total_filtered_data}**")

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hourly_avg_ratio.index, y=hourly_avg_ratio.values, marker="o", color="#2a9df4", ax=ax1)
ax1.set_xticks(range(0, 24))
ax1.set_title("Rata-rata Kontribusi Peminjaman Sepeda per Jam terhadap Total Harian")
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rasio Peminjaman terhadap Total Harian")
ax1.grid()
st.pyplot(fig1)

st.subheader("🌦️ Total Peminjaman Sepeda Berdasarkan Musim")

# Hitung total peminjaman per musim
season_counts = filtered_df.groupby("season")["cnt_day"].sum().reset_index()
season_counts = season_counts.sort_values(by="cnt_day")

# Mapping warna baru
season_colors = ["#2a9df4", "#187bcd", "#1167b1", "#03254c"]
color_map_new = {season: season_colors[i] for i, season in enumerate(season_counts["season"])}

# Visualisasi total peminjaman per musim
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(
    x=season_counts["season"], 
    y=season_counts["cnt_day"], 
    hue=season_counts["season"],  
    palette=color_map_new,
    dodge=False, 
    ax=ax2
)

ax2.set_xticklabels([season_mapping[s] for s in season_counts["season"]])
ax2.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
ax2.set_xlabel("Musim")
ax2.set_ylabel("Jumlah Peminjaman")

for p, total in zip(ax2.patches, season_counts["cnt_day"]):
    ax2.annotate(f"{int(total)}", 
                  (p.get_x() + p.get_width() / 2, p.get_height()), 
                  ha='center', va='bottom', fontsize=12, fontweight="bold")

st.pyplot(fig2)

# Footer
st.markdown("""
---
 **Bike Sharing Analysis** | © 2025 Rahmah Sary Fadiyah  
""")