import streamlit as st
import pandas as pd

st.set_page_config(page_title="🔍 Perbandingan Kolom CSV", layout="wide")
st.title("📊 Cek Kesamaan Nilai di Kolom CSV")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("📁 Unggah CSV Pertama", type="csv", key="csv1")
with col2:
    file2 = st.file_uploader("📁 Unggah CSV Kedua", type="csv", key="csv2")

if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    st.subheader("📋 Pratinjau Data")
    st.write("CSV 1:", df1.head())
    st.write("CSV 2:", df2.head())

    col1_name = st.selectbox("Pilih kolom dari CSV 1", df1.columns, key="col1")
    col2_name = st.selectbox("Pilih kolom dari CSV 2", df2.columns, key="col2")

    if col1_name and col2_name:
        values1 = df1[col1_name].dropna().astype(str).unique()
        values2 = df2[col2_name].dropna().astype(str).unique()

        common_values = sorted(set(values1) & set(values2))

        st.subheader("🔗 Nilai yang Sama di Kedua Kolom")
        if common_values:
            st.success(f"Ditemukan {len(common_values)} nilai yang sama.")
            st.write(common_values)
            csv = pd.DataFrame(common_values, columns=["Nilai Sama"]).to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Unduh Hasil", csv, "nilai_sama.csv", "text/csv")
        else:
            st.warning("Tidak ditemukan nilai yang sama di kolom yang dipilih.")
