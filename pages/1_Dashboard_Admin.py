import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import os
import requests

if "role" not in st.session_state or st.session_state.role != "admin":
    st.warning("Akses Ditolak. Halaman ini khusus Administrator.")
    st.stop()

st.title("🗺️ Panel Administrator Fortex")

@st.cache_data(show_spinner=False)
def load_real_data(uploaded_file=None):
    if uploaded_file is not None:
        try: return pd.read_csv(uploaded_file)
        except: return pd.DataFrame()
    file_path = "data/Rekap_Kesusilaan_Lengkap_dengan_Korban_FINAL_BALANCED.csv"
    if os.path.exists(file_path):
        try: return pd.read_csv(file_path)
        except: return pd.DataFrame()
    return pd.DataFrame()

st.markdown("### 📊 Peta Keadilan & Disparitas")
with st.expander("⚙️ Konfigurasi Data Sumber", expanded=False):
    file_manual = st.file_uploader("Unggah Dataset Evaluasi (.csv)", type=["csv"])

df = load_real_data(file_manual)

if not df.empty:
    st.sidebar.subheader("🎛️ Filter Data")
    prov_opts = sorted(df["Provinsi"].dropna().unique())
    klas_opts = sorted(df["Klasifikasi_Tindak_Pidana"].dropna().unique())

    provinsi_filter = st.sidebar.multiselect("Provinsi:", prov_opts, default=prov_opts)
    klasifikasi_filter = st.sidebar.multiselect("Klasifikasi Perkara:", klas_opts, default=klas_opts[:3])

    df_filtered = df[(df["Provinsi"].isin(provinsi_filter)) & (df["Klasifikasi_Tindak_Pidana"].isin(klasifikasi_filter))]
    total_kasus = len(df_filtered)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Putusan", f"{total_kasus:,}")
    m2.metric("Locus Terbanyak", df_filtered["Provinsi"].mode()[0] if total_kasus > 0 else "-")
    m3.metric("Modus Dominan", df_filtered["Klasifikasi_Tindak_Pidana"].mode()[0] if total_kasus > 0 else "-")

    if total_kasus > 0:
        prov_count = df_filtered['Provinsi'].value_counts().reset_index()
        prov_count.columns = ['Provinsi', 'Jumlah Kasus']

        try:
            geojson_url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.json"
            @st.cache_data
            def get_geojson(): return requests.get(geojson_url).json()
            geojson_id = get_geojson()

            fig_map = px.choropleth(prov_count, geojson=geojson_id, locations='Provinsi', featureidkey='properties.Propinsi', color='Jumlah Kasus', color_continuous_scale='Reds', title="Kepadatan Kasus Nasional")
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
        except:
            fig_bar = px.bar(prov_count, x='Provinsi', y='Jumlah Kasus', color='Jumlah Kasus', color_continuous_scale='Reds')
            st.plotly_chart(fig_bar, use_container_width=True)

        tab_disparitas, tab_profil = st.tabs(["⚖️ Disparitas Vonis", "👥 Profil Korban"])
        with tab_disparitas:
            if 'Lama_Kurungan' in df_filtered.columns:
                fig_box = px.box(df_filtered, x='Provinsi', y='Lama_Kurungan', color='Klasifikasi_Tindak_Pidana')
                st.plotly_chart(fig_box, use_container_width=True)
        with tab_profil:
            if 'Umur_Korban' in df_filtered.columns:
                fig_hist = px.histogram(df_filtered, x='Umur_Korban', color='Klasifikasi_Tindak_Pidana', nbins=20)
                st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.error("Data sistem kosong.")

st.markdown("---")
st.markdown("### 🧠 Kilas Perkara AI")
API_KEY = st.text_input("Gemini API Key:", type="password")
teks_hukum = st.text_area("Teks Putusan Hukum:", height=150)

if st.button("Analisis Kasus"):
    if API_KEY and teks_hukum:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"Ekstrak ke 3 poin: Kronologi, Relasi Kuasa, Motif.\n\nTeks: {teks_hukum}")
            st.success("Selesai!")
            st.info(res.text)
        except Exception as e:
            st.error(f"Gagal: {e}")
    else:
        st.warning("Isi API Key dan Teks.")
        # ==========================================
# BAGIAN C: MANAJEMEN LAPORAN MASUK
# ==========================================
st.markdown("---")
st.markdown("### 📥 Kotak Masuk Laporan Warga")
st.write("Pantau laporan darurat dan bukti dokumen yang diunggah oleh masyarakat.")

file_laporan = "laporan_anonim.csv"

# Cek apakah file CSV laporan sudah terbuat
if os.path.exists(file_laporan):
    try:
        # Baca data laporan
        df_laporan = pd.read_csv(file_laporan)

        # Tampilkan dalam bentuk tabel interaktif
        st.dataframe(df_laporan, use_container_width=True)

        # Berikan informasi lokasi file fisik
        st.caption("📁 Catatan: File bukti lampiran fisik (PDF/Gambar) tersimpan secara lokal di dalam folder `uploads/` pada server.")

    except Exception as e:
        st.error(f"Gagal membaca pangkalan data laporan: {e}")
else:
    st.info("Belum ada laporan darurat yang masuk dari sistem Safe Space.")
