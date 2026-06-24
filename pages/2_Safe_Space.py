import streamlit as st
import os
import csv
from datetime import datetime

# 1. Proteksi Halaman
if "role" not in st.session_state or st.session_state.role != "user":
    st.warning("Akses Ditolak. Halaman ini khusus Warga Sipil.")
    st.stop()

st.markdown("""
    <style>
    .btn-sos > .stButton>button {
        background-color: #FF3B30 !important; color: white !important;
        font-weight: bold !important; padding: 20px 0px !important; width: 100%; border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚨 Safe Space & SOS")
st.markdown("Jangan takut bersuara. Kami menyediakan ruang aman.")

st.markdown("---")
st.markdown("### 🔴 Bantuan Darurat")
st.markdown('<div class="btn-sos">', unsafe_allow_html=True)
if st.button("HUBUNGI BANTUAN SEKARANG"):
    st.warning("📞 Hotline SAPA: 129\n📱 WhatsApp: 08111-129-129")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📝 Form Lapor Anonim (Termasuk Bukti)")

# Pastikan folder uploads ada untuk menyimpan bukti
if not os.path.exists("uploads"):
    os.makedirs("uploads")

with st.form("form_anonim"):
    lokasi = st.text_input("Lokasi Kejadian:")
    kronologi = st.text_area("Kronologi Singkat:")

    # TAMBAHAN: Komponen upload file untuk warga
    bukti_file = st.file_uploader("Unggah Dokumen/Bukti Pendukung (Opsional)", type=["pdf", "png", "jpg", "jpeg", "csv"])

    submitted = st.form_submit_button("Kirim Laporan", use_container_width=True)

    if submitted:
        if lokasi and kronologi:
            file_laporan = "laporan_anonim.csv"
            file_exists = os.path.isfile(file_laporan)
            nama_file_bukti = "Tidak ada lampiran"

            # Logika untuk menyimpan file yang diunggah warga ke folder lokal
            if bukti_file is not None:
                # Tambahkan timestamp ke nama file agar unik dan tidak menimpa file orang lain
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nama_file_bukti = f"{timestamp}_{bukti_file.name}"
                path_simpan = os.path.join("uploads", nama_file_bukti)

                with open(path_simpan, "wb") as f:
                    f.write(bukti_file.getbuffer())

            # Catat laporan ke CSV, tambahkan kolom nama file bukti
            with open(file_laporan, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Timestamp', 'Lokasi', 'Kronologi', 'File_Bukti'])
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lokasi, kronologi, nama_file_bukti])

            st.success(f"Laporan berhasil dikirim dan dicatat secara anonim! (Lampiran: {nama_file_bukti})")
        else:
            st.warning("Mohon isi lokasi dan kronologi terlebih dahulu.")
