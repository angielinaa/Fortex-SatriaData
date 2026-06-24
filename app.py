import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# KONFIGURASI HALAMAN UTAMA (TUGAS GHINA)
# ==========================================
st.set_page_config(page_title="Fortex | Ruang Aman & Keadilan", page_icon="🛡️", layout="wide")

# ==========================================
# CUSTOM CSS (TUGAS UTAMA GHINA: UI/UX APPLE-ESQUE)
# ==========================================
st.markdown("""
    <style>
    /* Mengubah font dasar dan warna background menjadi minimalis modern */
    .stApp {
        background-color: #FAFAFA;
        font-family: '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', sans-serif;
    }

    /* Merapikan Sidebar dengan border tipis elegan */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EAEAEA;
    }

    /* Desain Tombol Umum agar sudutnya melengkung halus */
    .stButton>button {
        border-radius: 10px;
        border: 1px solid #EAEAEA;
        font-weight: 500;
        background-color: #FFFFFF;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #007AFF;
        color: #007AFF;
        background-color: #F5F5F7;
    }

    /* Tombol SOS Darurat Merah Menyala dengan Efek Shadow */
    .btn-sos > .stButton>button {
        background-color: #FF3B30 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 15px 0px !important;
        box-shadow: 0 4px 14px 0 rgba(255, 59, 48, 0.4);
    }
    .btn-sos > .stButton>button:hover {
        background-color: #D70015 !important;
        box-shadow: 0 6px 20px 0 rgba(255, 59, 48, 0.6);
    }

    /* Styling Teks Judul dan Subjudul */
    h1 {
        font-weight: 700 !important;
        color: #1D1D1F !important;
    }
    h3 {
        font-weight: 600 !important;
        color: #333333 !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# FUNGSI MEMUAT DATA DUMMY (UNTUK TESTING UI)
# ==========================================
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Provinsi": ["Jawa Timur", "Jawa Barat", "DKI Jakarta"],
        "Klasifikasi_Tindak_Pidana": ["Pencabulan", "Pemerkosaan", "Persetubuhan"]
    })


df = load_data()

# ==========================================
# NAVIGASI SIDEBAR
# ==========================================
st.sidebar.title("🛡️ Fortex")
st.sidebar.markdown("Kekuatan, Ketangguhan, dan Transparansi Hukum.")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Pilar Navigasi:",
                        ["Peta Keadilan (Data)", "Kilas Perkara (Analisis AI)", "Safe Space & SOS (Aksi)"])

if menu == "Peta Keadilan (Data)":
    st.title("🗺️ Peta Keadilan")
    st.markdown("Transparansi data sebaran kasus pelanggaran kesusilaan di Indonesia.")
    st.info("Bagian visualisasi data sedang dikerjakan oleh Cinta di cabang sebelah.")

elif menu == "Kilas Perkara (Analisis AI)":
    st.title("🧠 Kilas Perkara & Profiling")
    st.markdown("Fitur ekstraksi dokumen hukum otomatis berbasis AI.")
    st.info("Bagian Backend & Prompt AI sedang dikerjakan oleh Enzy di cabang sebelah.")

elif menu == "Safe Space & SOS (Aksi)":
    st.title("🚨 Safe Space & SOS")
    st.markdown("Jangan takut bersuara. Kami menyediakan ruang aman dan panduan hak-hak korban sesuai UU TPKS.")

    st.markdown("---")
    col_sos1, col_sos2, col_sos3 = st.columns([1, 2, 1])
    with col_sos2:
        st.error("### 🔴 TOMBOL DARURAT (SOS)")
        st.markdown("*Tekan tombol di bawah jika Anda berada dalam kondisi terancam atau butuh pendampingan segera.*")

        # PENERAPAN CUSTOM CSS SOS KHUSUS DARI GHINA
        st.markdown('<div class="btn-sos">', unsafe_allow_html=True)
        if st.button("🚨 HUBUNGI BANTUAN DARURAT SEKARANG", use_container_width=True):
            st.warning("Menghubungkan ke SAPA 129 (KemenPPPA)...")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📝 Form Lapor Anonim")
    with st.form("form_anonim"):
        lokasi = st.text_input("Lokasi Kejadian (Kota/Kecamatan):")
        kronologi = st.text_area("Ceritakan Kronologi Singkat:")
        submitted = st.form_submit_button("Kirim Laporan Anonim")
        if submitted:
            st.success("Laporan terkirim secara enkripsi anonim!")