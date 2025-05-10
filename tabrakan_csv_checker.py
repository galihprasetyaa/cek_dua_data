import streamlit as st
import pandas as pd

st.set_page_config(page_title="🔁 Tabraan Data CSV", layout="wide")

st.title("🧮 Pencocokan Baris Antar Dua File CSV")
st.markdown("Unggah dua file CSV, lalu cari apakah ada **baris identik** di antara keduanya.")

# Upload file
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Unggah CSV Pertama", type="csv", key="csv1")
with col2:
    file2 = st.file_uploader("Unggah CSV Kedua", type="csv", key="csv2")

if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    st.subheader("📋 Pratinjau Data")
    st.write("CSV 1:")
    st.dataframe(df1.head())
    st.write("CSV 2:")
    st.dataframe(df2.head())

    # Samakan urutan kolom dan tipe
    try:
        df1_sorted = df1[sorted(df1.columns)].astype(str)
        df2_sorted = df2[sorted(df2.columns)].astype(str)

        # Gabungkan kolom jadi satu string untuk tiap baris
        df1_rows = df1_sorted.apply(lambda row: "|".join(row.values), axis=1)
        df2_rows = df2_sorted.apply(lambda row: "|".join(row.values), axis=1)

        # Cari baris yang sama
        common_rows = df1_rows[df1_rows.isin(df2_rows)].unique()

        st.subheader(f"✅ Ditemukan {len(common_rows)} baris yang sama persis:")
        if len(common_rows) > 0:
            result_df = pd.DataFrame([row.split("|") for row in common_rows], columns=sorted(df1.columns))
            st.dataframe(result_df)
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Unduh Hasil", csv, "baris_sama.csv", "text/csv")
        else:
            st.info("Tidak ada baris yang identik ditemukan.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membandingkan: {e}")
else:
    st.info("Silakan unggah dua file CSV.")
