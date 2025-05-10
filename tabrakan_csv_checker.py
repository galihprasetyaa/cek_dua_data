import streamlit as st
import pandas as pd

st.set_page_config(page_title="🧮 Perbandingan Data CSV", layout="wide")
st.title("📊 Perbandingan Dua File CSV")

st.markdown("Unggah dua file CSV, lalu:")
st.markdown("- Temukan kolom yang sama")
st.markdown("- Cek apakah ada **baris identik**")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("📁 Unggah CSV Pertama", type="csv", key="csv1")
with col2:
    file2 = st.file_uploader("📁 Unggah CSV Kedua", type="csv", key="csv2")

if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    st.subheader("📋 Pratinjau Data")
    st.write("CSV 1:")
    st.dataframe(df1.head())
    st.write("CSV 2:")
    st.dataframe(df2.head())

    # Menampilkan kolom yang sama
    st.subheader("🧩 Kolom yang Sama di Kedua CSV")
    common_columns = list(set(df1.columns) & set(df2.columns))
    if common_columns:
        st.success(f"Ditemukan {len(common_columns)} kolom yang sama:")
        st.write(common_columns)
    else:
        st.warning("Tidak ada kolom yang sama ditemukan.")

    # Mencari baris identik
    st.subheader("🔁 Pencarian Baris Identik")
    try:
        df1_sorted = df1[sorted(df1.columns)].astype(str)
        df2_sorted = df2[sorted(df2.columns)].astype(str)

        df1_rows = df1_sorted.apply(lambda row: "|".join(row.values), axis=1)
        df2_rows = df2_sorted.apply(lambda row: "|".join(row.values), axis=1)

        common_rows = df1_rows[df1_rows.isin(df2_rows)].unique()

        st.markdown(f"✅ Ditemukan **{len(common_rows)}** baris yang identik:")
        if len(common_rows) > 0:
            result_df = pd.DataFrame([row.split("|") for row in common_rows], columns=sorted(df1.columns))
            st.dataframe(result_df)
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Unduh Hasil Baris Identik", csv, "baris_identik.csv", "text/csv")
        else:
            st.info("Tidak ada baris identik ditemukan.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membandingkan baris: {e}")
else:
    st.info("Silakan unggah dua file CSV terlebih dahulu.")
