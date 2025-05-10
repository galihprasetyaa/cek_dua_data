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
        # Ambil nilai dan hitung frekuensi
        df1_counts = df1[col1_name].dropna().astype(str).value_counts()
        df2_counts = df2[col2_name].dropna().astype(str).value_counts()

        common_values = sorted(set(df1_counts.index) & set(df2_counts.index))

        st.subheader("🔗 Nilai yang Sama dan Jumlah Kemunculannya")
        if common_values:
            data = []
            for val in common_values:
                data.append({
                    "Nilai": val,
                    f"Jumlah di {col1_name} (CSV 1)": df1_counts[val],
                    f"Jumlah di {col2_name} (CSV 2)": df2_counts[val],
                })

            result_df = pd.DataFrame(data)
            st.dataframe(result_df)

            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Unduh Hasil", csv, "nilai_sama_dengan_jumlah.csv", "text/csv")
        else:
            st.warning("Tidak ditemukan nilai yang sama di kolom yang dipilih.")
