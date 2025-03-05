import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (pastikan merged_df sudah tersedia)
@st.cache_data
def load_data():
    return pd.read_csv("main_data.csv")

merged_df = load_data()

# Judul Aplikasi
st.title("Analisis Peminjaman Sepeda")


merged_df['hourly_ratio'] = merged_df['cnt_hourly'] / merged_df['cnt_day']
hourly_avg_ratio = merged_df.groupby('hr')['hourly_ratio'].mean()

# Line Chart: Rata-rata kontribusi peminjaman sepeda per jam
st.subheader("Rata-rata Kontribusi Peminjaman Sepeda per Jam terhadap Total Harian")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hourly_avg_ratio.index, y=hourly_avg_ratio.values, marker="o", color="b", ax=ax1)
ax1.set_xticks(range(0, 24))
ax1.set_title("Rata-rata Kontribusi Peminjaman Sepeda per Jam terhadap Total Harian")
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rasio Peminjaman terhadap Total Harian")
ax1.grid()
st.pyplot(fig1)

# Bar Chart: Total peminjaman sepeda berdasarkan musim
st.subheader("Total Peminjaman Sepeda Berdasarkan Musim")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(x=merged_df["season"], y=merged_df["cnt_day"], hue=merged_df["season"], palette="coolwarm", dodge=False, ax=ax2)
ax2.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
ax2.set_xlabel("Musim")
ax2.set_ylabel("Jumlah Peminjaman")
ax2.set_xticks(ticks=[0,1,2,3])
ax2.set_xticklabels(["Cerah", "Kabut + Berawan", "Salju Ringan, Hujan Ringan", "Hujan Lebat + Butiran Es"], rotation=25)
st.pyplot(fig2)

st.markdown("""
---
© 2025 Bike Sharing Analysis.Rahmah Sary Fadiyah.
""")