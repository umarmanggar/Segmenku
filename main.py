# File: main.py
# Deskripsi: File utama untuk menjalankan aplikasi web Streamlit.
# Mengintegrasikan semua modul lain untuk menyediakan fungsionalitas penuh.
# Relevan dengan seluruh SRS dan Test Case.

# import streamlit as st
# import pandas as pd
# import time
# from io import BytesIO
# import base64

# # --- Impor Modul Aplikasi ---
# from user_management import UserManagement, UserRole
# from dataload import DataProcessor
# from clustering import SegmentasiNasabah
# from visualisasi import VisualisasiData
# from rekomendasi import SistemRekomendasi

# # --- Inisialisasi State Aplikasi ---
# def initialize_session_state():
#     """Inisialisasi session state jika belum ada."""
#     if 'user_mgmt' not in st.session_state:
#         st.session_state.user_mgmt = UserManagement()
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False
#     if 'user_info' not in st.session_state:
#         st.session_state.user_info = None
#     if 'df_processed' not in st.session_state:
#         st.session_state.df_processed = None
#     if 'df_clustered' not in st.session_state:
#         st.session_state.df_clustered = None

# # --- Fungsi Utilitas ---
# def get_table_download_link(df, filename, text):
#     """Membuat link download untuk DataFrame."""
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

# # --- Halaman & Komponen UI ---

# # Skenario: Login (TS.Log.004)
# def show_login_page():
#     """Menampilkan form login."""
#     st.set_page_config(page_title="Login - Segmentasi Nasabah", layout="centered")
#     st.title("Sistem Segmentasi & Rekomendasi Nasabah")

#     with st.form("login_form"):
#         username = st.text_input("Username", key="login_user")
#         password = st.text_input("Password", type="password", key="login_pass")
#         submitted = st.form_submit_button("Login")

#         if submitted:
#             success, message, user_info = st.session_state.user_mgmt.login(username, password)
#             if success:
#                 st.session_state.logged_in = True
#                 st.session_state.user_info = user_info
#                 st.success(message)
#                 time.sleep(1)
#                 st.rerun()
#             else:
#                 st.error(message)

# # Skenario: Navigasi Menu Utama
# def main_sidebar():
#     """Menampilkan sidebar dan menu navigasi berdasarkan peran pengguna."""
#     user_role = st.session_state.user_info['role']
#     st.sidebar.title(f"Menu - {user_role.capitalize()}")

#     # Opsi menu berdasarkan peran dari SRS 2.3
#     if user_role == UserRole.ADMIN.value:
#         options = ["Dashboard", "Manajemen Data", "Manajemen Pengguna"]
#     elif user_role == UserRole.MARKETING.value:
#         options = ["Dashboard", "Segmentasi Nasabah", "Rekomendasi Produk"]
#     elif user_role == UserRole.MANAGEMENT.value:
#         options = ["Dashboard", "Laporan & Visualisasi"]
#     else:
#         options = ["Dashboard"]

#     choice = st.sidebar.radio("Navigasi", options)

#     st.sidebar.markdown("---")
#     if st.sidebar.button("Logout"):
#         for key in list(st.session_state.keys()):
#             del st.session_state[key]
#         st.success("Anda telah berhasil logout.")
#         time.sleep(1)
#         st.rerun()

#     return choice

# # Halaman: Dashboard
# def show_dashboard():
#     st.title(f"👋 Halo, {st.session_state.user_info['full_name']}!")
#     st.markdown("Selamat datang di Dashboard Sistem Segmentasi Nasabah.")

#     st.subheader("Ringkasan Data")
#     if st.session_state.df_clustered is not None:
#         df = st.session_state.df_clustered
#         col1, col2 = st.columns(2)
#         col1.metric("Jumlah Nasabah", f"{df.shape[0]:,}")
#         col2.metric("Jumlah Segmen", df['Klaster'].nunique())

#         st.write("Distribusi Nasabah per Segmen:")
#         # Menggunakan VisualisasiData untuk membuat chart
#         visualizer = VisualisasiData(df)
#         success, chart, msg = visualizer.buat_pie_chart_klaster()
#         if success:
#             st.image(BytesIO(base64.b64decode(chart)), use_column_width=True)
#         else:
#             st.warning(msg)
#     else:
#         st.info("Data belum diproses. Silakan mulai dari halaman 'Manajemen Data'.")

# # Halaman: Manajemen Data (Skenario PD-001)
# def show_data_management():
#     st.title("Manajemen Data")
#     st.markdown("Unggah, validasi, dan proses data nasabah di sini.")

#     # Test Case PD-001-01
#     uploaded_file = st.file_uploader("Unggah file bank.csv", type=["csv"])
#     if uploaded_file:
#         processor = DataProcessor(uploaded_file)
#         success_load, df, msg_load = processor.load_data()

#         if success_load:
#             st.success(msg_load)
#             st.dataframe(df.head())

#             # Kolom yang diharapkan untuk validasi dan fitur
#             expected_cols = ['age', 'balance', 'duration', 'campaign']

#             # Test Case PD-001-02, PD-001-03
#             success_val, msg_val = processor.validate_data_structure(expected_cols)
#             if not success_val:
#                 st.error(msg_val)
#                 return

#             # Test Case PD-001-04, PD-001-06
#             if st.button("Proses Data (Pembersihan & Transformasi)"):
#                 with st.spinner("Membersihkan data..."):
#                     success_pre, df_pre, msg_pre = processor.preprocess_data()
#                     if not success_pre:
#                         st.error(msg_pre)
#                         return

#                 with st.spinner("Melakukan transformasi data..."):
#                     processor.data = df_pre # Update data di prosesor
#                     success_trans, df_trans, msg_trans = processor.transform_data()

#                 if success_trans:
#                     st.session_state.df_processed = df_trans
#                     st.success("Data berhasil diproses dan siap untuk segmentasi!")
#                     st.write("Data setelah transformasi:")
#                     st.dataframe(st.session_state.df_processed.head())
#                 else:
#                     st.error(msg_trans)
#         else:
#             st.error(msg_load)

# # Halaman: Segmentasi (Skenario SN-01)
# def show_segmentation():
#     st.title("Segmentasi Nasabah")
#     if st.session_state.df_processed is None:
#         st.warning("Data belum diproses. Silakan proses data di halaman 'Manajemen Data'.")
#         return

#     st.subheader("Parameter K-Means")
#     # REQ-1.2: Administrator dapat mengonfigurasi jumlah cluster
#     n_clusters = st.slider("Pilih Jumlah Klaster (Segmen)", min_value=2, max_value=8, value=4, step=1)

#     # Test Case SN-01-01
#     if st.button("Jalankan Segmentasi"):
#         with st.spinner("Melakukan proses clustering..."):
#             # Gunakan hanya kolom numerik untuk K-Means
#             numeric_df = st.session_state.df_processed.select_dtypes(include=np.number)
#             segmenter = SegmentasiNasabah(numeric_df, n_clusters)
#             success, df_result, message = segmenter.jalankan_segmentasi()

#         if success:
#             st.session_state.df_clustered = pd.concat([st.session_state.df_processed, df_result['Klaster']], axis=1)
#             st.success(message)

#             # Test Case SN-01-02
#             st.subheader("Hasil Segmentasi")
#             st.dataframe(st.session_state.df_clustered.head())
#             st.markdown(get_table_download_link(st.session_state.df_clustered, "hasil_segmentasi.csv", "Unduh Hasil Segmentasi (CSV)"), unsafe_allow_html=True)

#         else:
#             st.error(message)

# # Halaman: Rekomendasi (Skenario RP-01)
# def show_recommendation():
#     st.title("Rekomendasi Produk")
#     if st.session_state.df_clustered is None:
#         st.warning("Data belum disegmentasi. Silakan jalankan segmentasi terlebih dahulu.")
#         return

#     df = st.session_state.df_clustered
#     recommender = SistemRekomendasi(df)

#     # Test Case RP-01-01
#     success_rec, df_rec, msg_rec = recommender.buat_rekomendasi()
#     if success_rec:
#         st.success(msg_rec)

#         # Test Case RP-01-04
#         st.subheader("Filter Rekomendasi")
#         kategori_unik = ['Semua'] + list(df_rec['Kategori_Produk'].unique())
#         pilihan_kategori = st.selectbox("Filter berdasarkan Kategori Produk", options=kategori_unik)

#         if pilihan_kategori == 'Semua':
#             st.dataframe(df_rec)
#         else:
#             success_filter, df_filtered, msg_filter = recommender.filter_rekomendasi(pilihan_kategori)
#             if success_filter:
#                 st.dataframe(df_filtered)
#             else:
#                 st.error(msg_filter)

#         # Test Case RP-01-05
#         st.markdown(get_table_download_link(df_rec, "hasil_rekomendasi.csv", "Unduh Semua Rekomendasi (CSV)"), unsafe_allow_html=True)
#     else:
#         st.error(msg_rec)

# # Halaman: Laporan & Visualisasi (Skenario VD-01)
# def show_visualization():
#     st.title("Laporan dan Visualisasi")
#     if st.session_state.df_clustered is None:
#         st.warning("Data belum disegmentasi.")
#         return

#     df = st.session_state.df_clustered
#     visualizer = VisualisasiData(df)

#     st.subheader("Distribusi Nasabah per Segmen")
#     # Test Case VD-01-01
#     success_pie, pie_chart, msg_pie = visualizer.buat_pie_chart_klaster()
#     if success_pie:
#         st.image(BytesIO(base64.b64decode(pie_chart)))
#     else:
#         st.error(msg_pie)

#     st.subheader("Analisis Fitur per Segmen")
#     # Test Case VD-01-02
#     fitur_numerik = df.select_dtypes(include=np.number).columns.tolist()
#     fitur_pilihan = st.selectbox("Pilih fitur untuk dianalisis", options=fitur_numerik)

#     if fitur_pilihan:
#         success_bar, bar_chart, msg_bar = visualizer.buat_bar_chart(fitur_pilihan)
#         if success_bar:
#             st.image(BytesIO(base64.b64decode(bar_chart)))
#         else:
#             st.error(msg_bar)

# # Halaman: Manajemen Pengguna (Skenario MU-01)
# def show_user_management():
#     st.title("Manajemen Pengguna")

#     # Test Case MU-01-01: Verifikasi akses admin
#     if st.session_state.user_info['role'] != UserRole.ADMIN.value:
#         st.error("Hanya Admin yang dapat mengakses halaman ini.")
#         return

#     st.subheader("Daftar Pengguna")
#     df_users = st.session_state.user_mgmt.get_user_list_df()
#     st.dataframe(df_users)

#     st.subheader("Fitur Manajemen")
#     st.warning("Fitur tambah, edit, dan hapus pengguna sedang dalam pengembangan.")


# # --- Logika Utama Aplikasi ---
# def main():
#     """Fungsi utama untuk menjalankan alur aplikasi."""
#     initialize_session_state()

#     if not st.session_state.logged_in:
#         show_login_page()
#     else:
#         st.set_page_config(page_title="Dashboard - Segmentasi Nasabah", layout="wide")
#         choice = main_sidebar()

#         if choice == "Dashboard":
#             show_dashboard()
#         elif choice == "Manajemen Data":
#             show_data_management()
#         elif choice == "Segmentasi Nasabah":
#             show_segmentation()
#         elif choice == "Rekomendasi Produk":
#             show_recommendation()
#         elif choice == "Laporan & Visualisasi":
#             show_visualization()
#         elif choice == "Manajemen Pengguna":
#             show_user_management()

# if __name__ == "__main__":
#     main()


# DIUBAH: Mengimplementasikan UI untuk Tambah, Edit, dan Hapus Pengguna di halaman Manajemen Pengguna.

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict
from io import BytesIO
import base64

# --- Impor Modul Aplikasi ---
from user_management import UserManagement, UserRole
from dataload import DataProcessor
from clustering import Segmenter
from visualisasi import VisualisasiData
from rekomendasi import SistemRekomendasi, RekomendasiIndividual

# --- Inisialisasi State Aplikasi ---
def initialize_session_state():
    # User Management
    if 'user_mgmt' not in st.session_state: st.session_state.user_mgmt = UserManagement()
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if 'user_info' not in st.session_state: st.session_state.user_info = None

    # Data Processing
    if 'processor' not in st.session_state: st.session_state.processor = DataProcessor()
    if 'processing_step' not in st.session_state: st.session_state.processing_step = '1_upload'
    if 'final_data' not in st.session_state: st.session_state.final_data = None

    # Segmentation
    if 'clustered_data' not in st.session_state: st.session_state.clustered_data = None
    if 'segmenter_instance' not in st.session_state: st.session_state.segmenter_instance = None

    # Individual Recommendation
    if 'rekomendasi_individual' not in st.session_state: st.session_state.rekomendasi_individual = RekomendasiIndividual()
    if 'last_recommendation' not in st.session_state: st.session_state.last_recommendation = None

def get_table_download_link(df, filename, text):
    if df is None: return ""
    csv = df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

class MainApplication:
    def __init__(self):
        st.set_page_config(page_title="Sistem Segmentasi Bank", page_icon="🏦", layout="wide")
        initialize_session_state()

    def run(self):
        if not st.session_state.logged_in:
            self.show_login_page()
        else:
            self.show_main_app()

    def show_login_page(self):
        st.title("Sistem Segmentasi & Rekomendasi Nasabah")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                success, _, user_info = st.session_state.user_mgmt.login(username, password)
                if success:
                    st.session_state.logged_in = True; st.session_state.user_info = user_info; st.rerun()
                else: st.error("Username atau password salah.")

    def show_main_app(self):
        user_info = st.session_state.user_info
        st.sidebar.title(f"Menu - {user_info['role'].capitalize()}")

        options = ["Proses Data", "Segmentasi", "Laporan & Rekomendasi Segmen", "Simulasi Rekomendasi", "Manajemen Pengguna"]

        choice = st.sidebar.radio("Navigasi", options)
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                if key != 'user_mgmt': del st.session_state[key]
            initialize_session_state(); st.rerun()

        page_map = {
            "Proses Data": self.page_proses_data,
            "Segmentasi": self.page_segmentasi,
            "Laporan & Rekomendasi Segmen": self.page_laporan_segmen,
            "Simulasi Rekomendasi": self.page_simulasi_rekomendasi,
            "Manajemen Pengguna": self.page_manajemen_pengguna,
        }
        page_function = page_map.get(choice)
        if page_function:
            page_function()

    def page_proses_data(self):
        st.title("Proses Data dan Pemilihan Fitur")
        processor = st.session_state.processor
        with st.sidebar:
            st.header("Log Proses (PD-005)")
            log_content = '\n'.join(processor.audit_log) if processor.audit_log else "Belum ada proses."
            st.code(log_content)

        # LANGKAH 1: UPLOAD
        if st.session_state.processing_step == '1_upload':
            st.subheader("1. Unggah Data (PD-001)")
            uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])
            if uploaded_file and st.button("Proses File"):
                success, msg = processor.load_data(uploaded_file)
                if success: st.success(msg); st.session_state.processing_step = '2_cleaning'; st.rerun()
                else: st.error(msg)

        # LANGKAH 2: CLEANING
        elif st.session_state.processing_step == '2_cleaning':
            st.subheader("2. Pembersihan Data (PD-002)"); st.dataframe(processor.raw_data.head())
            col1, col2 = st.columns(2)
            missing_val = col1.radio("Metode Nilai Kosong:", ['Isi dengan Mean/Modus', 'Hapus Baris'])
            outlier = col2.radio("Metode Outlier:", ['Tidak Ada', 'Hapus Outlier (IQR)'])
            if st.button("Terapkan & Lanjutkan"):
                success, msg = processor.clean_data(missing_val, outlier)
                if success: st.success(msg); st.session_state.processing_step = '3_feature_selection'; st.rerun()
                else: st.error(msg)

        # LANGKAH 3: PEMILIHAN FITUR
        elif st.session_state.processing_step == '3_feature_selection':
            st.subheader("3. Pemilihan Fitur (PD-003)"); st.dataframe(processor.processed_data.head())
            all_cols = processor.processed_data.columns.tolist()
            selected = st.multiselect("Pilih fitur untuk analisis:", options=all_cols, default=all_cols)
            if st.button("Simpan Fitur & Lanjutkan"):
                success, msg = processor.select_features(selected)
                if success: st.success(msg); st.session_state.processing_step = '4_transform'; st.rerun()
                else: st.error(msg)

        # LANGKAH 4: TRANSFORMASI
        elif st.session_state.processing_step == '4_transform':
            st.subheader("4. Transformasi Data (PD-004)"); st.dataframe(processor.processed_data.head())
            scaler = st.radio("Metode Scaling:", ['StandardScaler (Z-score)', 'MinMaxScaler'])
            if st.button("Selesaikan Proses"):
                success, msg = processor.transform_data(scaler)
                if success:
                    st.success(msg); st.session_state.final_data = processor.processed_data
                    st.session_state.processing_step = '5_done'; st.balloons(); st.rerun()
                else: st.error(msg)

        # LANGKAH 5: SELESAI
        elif st.session_state.processing_step == '5_done':
            st.header("✅ Proses Data Selesai"); st.dataframe(st.session_state.final_data.head())
            if st.button("Ulangi Proses"):
                st.session_state.processor = DataProcessor(); st.session_state.processing_step = '1_upload'
                st.session_state.final_data = None; st.rerun()

    def page_segmentasi(self):
        st.title("Segmentasi Nasabah")
        if st.session_state.final_data is None:
            st.warning("Data belum diproses. Selesaikan di halaman 'Proses Data'."); return

        st.subheader("Pengaturan Metode Segmentasi (SN-001)")
        metode = st.radio("Pilih Metode:", ("K-Means", "DBSCAN"))

        params = {}
        if metode == "K-Means":
            params['n_clusters'] = st.number_input("Jumlah Cluster (SN-002):", min_value=2, value=3, step=1)

        if st.button("Jalankan Segmentasi (SN-003)"):
            segmenter = Segmenter(data_asli=st.session_state.processor.raw_data.loc[st.session_state.final_data.index], data_proses=st.session_state.final_data)
            with st.spinner(f"Menjalankan {metode}..."):
                success, df_result, message, score = segmenter.jalankan_segmentasi(metode, params)
            if success:
                st.session_state.clustered_data = df_result; st.session_state.segmenter_instance = segmenter
                st.success(message)
                # SN-005: Evaluasi Hasil
                if score is not None:
                    st.metric(label="Silhouette Score", value=f"{score:.4f}")
                    if score < 0.3: st.warning("Kualitas segmentasi mungkin kurang optimal (Skor < 0.3).")
            else: st.error(f"Gagal: {message}")

        if st.session_state.clustered_data is not None:
            st.subheader("Hasil Segmentasi (SN-004)")
            st.dataframe(st.session_state.clustered_data)
            st.markdown(get_table_download_link(st.session_state.clustered_data, "hasil_segmentasi.csv", "Unduh Hasil (CSV)"), unsafe_allow_html=True)
            st.markdown("---")
            # Fitur lihat detail anggota
            st.subheader("Lihat Detail Anggota per Segmen")
            segmenter = st.session_state.get('segmenter_instance')
            if segmenter:
                cluster_ids_choice = [c for c in sorted(st.session_state.clustered_data['Klaster'].unique()) if c != -1]
                if cluster_ids_choice:
                    selected_cluster = st.selectbox("Pilih Klaster:", options=cluster_ids_choice)
                    detail_df = segmenter.dapatkan_detail_klaster(selected_cluster)
                    st.dataframe(detail_df)

    def page_laporan(self):
        st.title("Laporan Visual & Rekomendasi per Segmen")
        if st.session_state.clustered_data is None:
            st.warning("Data belum disegmentasi. Lakukan di halaman 'Segmentasi'."); return

        df_laporan = st.session_state.clustered_data.copy()

        st.header("Visualisasi Interaktif (VD-001 s/d VD-005)")
        visualizer = VisualisasiData(df_laporan)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Distribusi Segmen")
            pie_chart = visualizer.buat_pie_chart_klaster()
            if pie_chart: st.plotly_chart(pie_chart, use_container_width=True)
        with col2:
            st.subheader("Analisis Fitur")
            fitur_numerik = [f for f in df_laporan.select_dtypes(include=np.number).columns if f not in ['Klaster', 'ID']]
            fitur_pilihan = st.selectbox("Pilih fitur:", options=fitur_numerik)
            if fitur_pilihan:
                bar_chart = visualizer.buat_bar_chart(fitur_pilihan)
                if bar_chart: st.plotly_chart(bar_chart, use_container_width=True)
        st.info("Arahkan mouse ke grafik untuk detail (VD-004) dan gunakan tombol di pojok kanan atas grafik untuk ekspor (VD-003).")

        st.markdown("---")
        st.header("Rekomendasi Produk per Segmen")
        if 'Produk_Rekomendasi' not in df_laporan.columns:
            recommender = SistemRekomendasi(df_laporan)
            success, df_laporan, _ = recommender.buat_rekomendasi()
            if success: st.session_state.clustered_data = df_laporan
            else: st.error("Gagal membuat rekomendasi."); return

        for cluster_id in sorted([c for c in df_laporan['Klaster'].unique() if c != -1]):
            data_klaster = df_laporan[df_laporan['Klaster'] == cluster_id]
            info = data_klaster[['Produk_Rekomendasi', 'Alasan_Rekomendasi']].iloc[0]
            with st.expander(f"Segmen {cluster_id} ({len(data_klaster)} nasabah) -> Rekomendasi: {info['Produk_Rekomendasi']}"):
                st.markdown(f"**Alasan:** *{info['Alasan_Rekomendasi']}*")
                st.dataframe(data_klaster)

    def page_simulasi_rekomendasi(self):
        st.title("Simulasi Rekomendasi Individual (RP-001 s/d RP-005)")
        recommender = st.session_state.rekomendasi_individual
        with st.form("recommendation_form"):
            st.subheader("Input Parameter Nasabah (RP-001)")
            col1, col2 = st.columns(2)
            usia = col1.number_input("Usia", min_value=0, step=1)
            transaksi = col2.number_input("Jml Transaksi/Bulan", min_value=0, step=1)
            submitted = st.form_submit_button("Dapatkan Rekomendasi (RP-002)")
            if submitted:
                if usia == 0 or transaksi == 0:
                    st.error("Data tidak boleh kosong (RP-001-01).")
                else:
                    produk, skor = recommender.dapatkan_rekomendasi(usia, transaksi)
                    st.session_state.last_recommendation = {'produk': produk, 'skor': skor, 'usia': usia, 'transaksi': transaksi}

        if st.session_state.last_recommendation:
            rec = st.session_state.last_recommendation
            st.subheader("Hasil Rekomendasi (RP-003)")
            if rec['produk']:
                col1, col2 = st.columns(2)
                col1.metric("Produk Direkomendasikan", rec['produk'])
                col2.metric("Skor Kecocokan", f"{rec['skor']}/100")
                df_dl = pd.DataFrame([{'usia': rec['usia'], 'transaksi': rec['transaksi'], 'produk': rec['produk'], 'skor': rec['skor']}])
                st.markdown(get_table_download_link(df_dl, "rekomendasi.csv", "Simpan Rekomendasi (RP-004)"), unsafe_allow_html=True)
                st.markdown("---")
                st.subheader("Feedback User (RP-005)")
                rating_options = ("⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐")
                rating = st.radio("Rating Anda:", rating_options, key="rating", horizontal=True, index=None)
                if st.button("Kirim Feedback"):
                    if rating is None:
                        st.warning("Silakan beri rating terlebih dulu (RP-005-01).")
                    else:
                        recommender.simpan_feedback(rec['produk'], len(rating))
                        st.success("Terima kasih atas feedback Anda!")
            else:
                st.error("Tidak ada produk yang cocok untuk parameter ini (RP-003-01).")

    def page_manajemen_pengguna(self):
        st.title("Manajemen Pengguna (MU-001)")
        # ... (Sama seperti sebelumnya)
        user_mgmt = st.session_state.user_mgmt
        tab1, tab2, tab3 = st.tabs(["Daftar", "Tambah", "Edit & Hapus"])
        with tab1: st.dataframe(user_mgmt.get_user_list_df(), use_container_width=True)
        with tab2:
            with st.form("add_form", clear_on_submit=True):
                username = st.text_input("Username"); password = st.text_input("Password", type="password")
                full_name = st.text_input("Nama Lengkap"); email = st.text_input("Email")
                role = st.selectbox("Role", [r.value for r in UserRole])
                if st.form_submit_button("Tambah"):
                    success, msg = user_mgmt.add_user(username, password, UserRole(role), full_name, email)
                    if success: st.success(msg)
                    else: st.error(msg)
        with tab3:
            user_to_edit = st.selectbox("Pilih Pengguna", user_mgmt.get_all_usernames())
            if user_to_edit:
                user_obj = user_mgmt.get_user(user_to_edit)
                with st.form("edit_form"):
                    st.write(f"Mengedit: {user_obj.username}")
                    full_name = st.text_input("Nama Lengkap", value=user_obj.full_name)
                    email = st.text_input("Email", value=user_obj.email)
                    role = st.selectbox("Role", [r.value for r in UserRole], index=[r.value for r in UserRole].index(user_obj.role.value))
                    password = st.text_input("Password Baru (opsional)", type="password")
                    if st.form_submit_button("Simpan"):
                        data = {'full_name': full_name, 'email': email, 'role': role, 'password': password}
                        success, msg = user_mgmt.edit_user(user_to_edit, data)
                        if success: st.success(msg)
                        else: st.error(msg)
                if user_to_edit != 'admin':
                    if st.checkbox(f"Saya yakin ingin menghapus {user_to_edit}"):
                        if st.button("Hapus Pengguna"):
                            success, msg = user_mgmt.delete_user(user_to_edit, st.session_state.user_info['username'])
                            if success: st.success(msg); st.rerun()
                            else: st.error(msg)

if __name__ == "__main__":
    app = MainApplication()
    app.run()