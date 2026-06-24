import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fortex | Ruang Aman & Keadilan", page_icon="🛡️", layout="wide")


# ==========================================
# MEMUAT CSV ASLI DARI FOLDER DATA (TUGAS CINTA)
# ==========================================
@st.cache_data
def load_real_data():
    # Membaca dari struktur folder data/ sesuai rancangan tim
    try:
        return pd.read_csv("data/Rekap_Kesusilaan_Lengkap_dengan_Korban_FINAL_BALANCED.csv")
    except FileNotFoundError:
        st.error("File CSV tidak ditemukan di folder 'data/'. Pastikan file dataset sudah ditaruh di sana!")
        return pd.DataFrame()


df = load_real_data()

# ==========================================
# NAVIGASI SIDEBAR
# ==========================================
st.sidebar.title("🛡️ Fortex")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Pilar Navigasi:",
                        ["Peta Keadilan (Data)", "Kilas Perkara (Analisis AI)", "Safe Space & SOS (Aksi)"])

# ==========================================
# PILAR DATA: PETA KEADILAN (TUGAS UTAMA CINTA)
# ==========================================
if menu == "Peta Keadilan (Data)":
    st.title("🗺️ Peta Keadilan")
    st.markdown("Transparansi data sebaran kasus pelanggaran kesusilaan di Indonesia.")

    if not df.empty:
        # 1. BARIS FILTER
        col1, col2 = st.columns(2)
        with col1:
            provinsi_filter = st.multiselect("Filter Provinsi Kejadian:", options=df["Provinsi"].dropna().unique(),
                                             default=df["Provinsi"].dropna().unique()[:3])
        with col2:
            klasifikasi_filter = st.multiselect("Filter Klasifikasi Kejahatan:",
                                                options=df["Klasifikasi_Tindak_Pidana"].dropna().unique(),
                                                default=df["Klasifikasi_Tindak_Pidana"].dropna().unique()[:3])

        # Filter Dataframe berdasarkan pilihan user
        df_filtered = df[
            (df["Provinsi"].isin(provinsi_filter)) & (df["Klasifikasi_Tindak_Pidana"].isin(klasifikasi_filter))]

        # 2. METRIK DESKRIPTIF STATISTIK
        st.markdown("### 📊 Ringkasan Deskriptif")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Total Putusan yang Diekstrak", value=len(df_filtered))
        m2.metric(label="Locus Delicti Terbanyak",
                  value=df_filtered["Provinsi"].mode()[0] if not df_filtered.empty else "-")
        m3.metric(label="Modus Kasus Dominan",
                  value=df_filtered["Klasifikasi_Tindak_Pidana"].mode()[0] if not df_filtered.empty else "-")

        # 3. INTERAKTIF PLOTLY TABS
        st.markdown("---")
        tab1, tab2 = st.tabs(["🔴 Analisis Disparitas Wilayah", "📈 Korelasi Demografi & Hukuman"])

        with tab1:
            st.markdown("#### Sebaran Konsentrasi Kasus Berdasarkan Wilayah")
            prov_count = df_filtered['Provinsi'].value_counts().reset_index()
            prov_count.columns = ['Provinsi', 'Jumlah Kasus']

            # Penggunaan Treemap interaktif untuk menyoroti tingkat kerawanan wilayah
            fig_tree = px.treemap(
                prov_count,
                path=['Provinsi'],
                values='Jumlah Kasus',
                color='Jumlah Kasus',
                color_continuous_scale='Reds',
                title='Peta Kepadatan Kasus Kesusilaan Tingkat Provinsi'
            )
            st.plotly_chart(fig_tree, use_container_width=True)

        with tab2:
            st.markdown("#### Analisis Disparitas Vonis Kurungan berdasarkan Umur Korban")
            # Menghitung scatter korelasi umur vs masa hukuman hakim
            if 'Umur_Korban' in df_filtered.columns and 'Lama_Kurungan' in df_filtered.columns:
                # Membersihkan teks kurungan ke angka jika diperlukan
                fig_scatter = px.scatter(
                    df_filtered,
                    x='Umur_Korban',
                    y='Lama_Kurungan',
                    color='Klasifikasi_Tindak_Pidana',
                    hover_data=['Nomor_Putusan', 'Hubungan_Terdakwa_Korban'],
                    title='Sebaran Titik Koordinat Korelasi Umur Korban dan Lama Hukuman (Tahun)'
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.warning("Kolom analisis demografi (Umur_Korban/Lama_Kurungan) tidak lengkap.")
    else:
        st.warning("Data kosong. Silakan periksa file CSV di folder data.")

elif menu == "Kilas Perkara (Analisis AI)":
    st.title("🧠 Kilas Perkara & Profiling")
    st.info("Bagian Backend & Prompt AI sedang dikerjakan oleh Enzy di cabang sebelah.")

elif menu == "Safe Space & SOS (Aksi)":
    st.title("🚨 Safe Space & SOS")
    st.info("Desain dan layout menu ini sedang dikerjakan oleh Ghina di cabang sebelah.")