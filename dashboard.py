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
st.subheader("Distribusi Peminjaman Sepeda Per Jam vs Total Harian")

# Visualisasi Data
merged_df['hourly_ratio'] = merged_df['cnt_hourly'] / merged_df['cnt_day']

hourly_avg_ratio = merged_df.groupby('hr')['hourly_ratio'].mean()

plt.figure(figsize=(10, 5))
sns.lineplot(x=hourly_avg_ratio.index, y=hourly_avg_ratio.values, marker="o", color="b")
plt.xticks(range(0, 24))
plt.title("Rata-rata Kontribusi Peminjaman Sepeda per Jam terhadap Total Harian")
plt.xlabel("Jam")
plt.ylabel("Rasio Peminjaman terhadap Total Harian")
plt.grid()
plt.show()
