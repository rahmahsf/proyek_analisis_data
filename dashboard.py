import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (pastikan merged_df sudah tersedia)
@st.cache_data
def load_data():
    return pd.read_csv("main_data.csv")

df = load_data()

# Judul Aplikasi
st.title("Analisis Peminjaman Sepeda")
st.subheader("Distribusi Peminjaman Sepeda Per Jam vs Total Harian")

# Visualisasi Data
fig, ax1 = plt.subplots(figsize=(10,5))

sns.lineplot(x=df['hr'], y=df['cnt_hourly'], marker='o', label='Peminjaman Per Jam', ax=ax1, color='b')
ax2 = ax1.twinx()
sns.lineplot(x=df['hr'], y=df['cnt_day'], marker='o', label='Total Peminjaman Harian', ax=ax2, color='r')

ax1.set_xlabel("Jam")
ax1.set_ylabel("Jumlah Peminjaman Per Jam", color='b')
ax2.set_ylabel("Total Peminjaman Harian", color='r')
ax1.set_xticks(range(0, 24))
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
st.pyplot(fig)
