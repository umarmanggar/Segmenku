# import streamlit as st
# import pandas as pd
# import time
# from io import BytesIO
# import base64
# import numpy as np
# import database as db

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
#                     with st.spinner("Menyimpan data ke database..."):
#                         db.save_dataframe(df_trans, 'processed_data')

#                     st.success("Data berhasil diproses dan disimpan ke database untuk diakses peran lain!")
#                     st.write("Data setelah transformasi:")
#                     st.dataframe(df_trans.head())
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

#     df_processed = db.load_dataframe('processed_data')
#     if df_processed is None or df_processed.empty:
#         st.warning("Data belum diolah dan disimpan oleh Admin. Silakan hubungi Admin untuk memproses data terlebih dahulu.")
#         return

#     st.info("Data yang telah diproses oleh Admin berhasil dimuat.")

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
#     if 'df_clustered' in st.session_state and st.session_state.df_clustered is not None:
#         df = st.session_state.df_clustered
#         st.info("Menampilkan data dari sesi segmentasi saat ini.")
#     else:
#         df = db.load_dataframe('clustered_data')
#         if df is None or df.empty:
#             st.warning("Data belum disegmentasi. Silakan jalankan proses di halaman 'Segmentasi Nasabah'.")
#             return
#         st.info("Berhasil memuat data segmentasi terakhir dari database.")

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
#     db.init_db()  # Inisialisasi database
#     initialize_session_state()

#     if not st.session_state.get('logged_in'):
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

# File: main.py
# Deskripsi: File utama untuk menjalankan aplikasi web Streamlit.
# VERSI DIUBAH: Admin sekarang memiliki akses ke semua menu untuk menyederhanakan alur kerja.

import streamlit as st
import pandas as pd
import numpy as np
import time
from io import BytesIO
import base64

# --- Impor Modul Aplikasi ---
# Pastikan semua file .py ini berada di direktori yang sama
from user_management import UserManagement, UserRole
from dataload import DataProcessor
from clustering import SegmentasiNasabah
from visualisasi import VisualisasiData
from rekomendasi import SistemRekomendasi

# --- Inisialisasi State Aplikasi ---
def initialize_session_state():
    """Inisialisasi session state jika belum ada."""
    if 'user_mgmt' not in st.session_state:
        st.session_state.user_mgmt = UserManagement()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    # Kita akan menggunakan satu DataFrame utama yang diperbarui di setiap langkah
    if 'app_data' not in st.session_state:
        st.session_state.app_data = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None


# --- Fungsi Utilitas ---
def get_table_download_link(df, filename, text):
    """Membuat link download untuk DataFrame."""
    if df is None:
        return ""
    csv = df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

# --- Halaman & Komponen UI ---

# Skenario: Login (TS.Log.004)
def show_login_page():
    """Menampilkan form login."""
    st.set_page_config(page_title="Login - Segmentasi Nasabah", layout="centered")
    st.title("Sistem Segmentasi & Rekomendasi Nasabah")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_user", value="admin")
        password = st.text_input("Password", type="password", key="login_pass", value="admin123")
        submitted = st.form_submit_button("Login")

        if submitted:
            user_mgmt = st.session_state.user_mgmt
            success, message, user_info = user_mgmt.login(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_info = user_info
                st.success(message)
                time.sleep(1)
                st.rerun()
            else:
                st.error(message)

# Skenario: Navigasi Menu Utama
def main_sidebar():
    """Menampilkan sidebar dan menu navigasi berdasarkan peran pengguna."""
    user_info = st.session_state.user_info
    user_role = user_info['role']
    st.sidebar.title(f"Menu - {user_role.capitalize()}")

    # --- PERUBAHAN UTAMA ADA DI SINI ---
    # Logika baru: Admin mendapatkan akses ke semua menu.
    if user_role == UserRole.ADMIN.value:
        # DIUBAH: Admin kini memiliki semua menu untuk alur kerja yang lengkap
        options = [
            "Dashboard",
            "Manajemen Data",
            "Segmentasi Nasabah",
            "Rekomendasi Produk",
            "Laporan & Visualisasi",
            "Manajemen Pengguna"
        ]
    elif user_role == UserRole.MARKETING.value:
        options = ["Dashboard", "Segmentasi Nasabah", "Rekomendasi Produk"]
    elif user_role == UserRole.MANAGEMENT.value:
        options = ["Dashboard", "Laporan & Visualisasi"]
    else:
        options = ["Dashboard"] # Fallback untuk peran lain

    choice = st.sidebar.radio("Navigasi", options)

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        # Hapus semua state untuk sesi yang bersih saat login kembali
        keys_to_keep = ['user_mgmt'] # Jaga instance UserManagement
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
        initialize_session_state() # Inisialisasi ulang state dasar
        st.rerun()

    return choice

# Halaman: Dashboard
def show_dashboard():
    st.title(f"👋 Halo, {st.session_state.user_info['full_name']}!")
    st.markdown("Selamat datang di Dashboard Sistem Segmentasi Nasabah.")

    st.subheader("Ringkasan Data Terakhir")
    if st.session_state.app_data is not None:
        df = st.session_state.app_data
        col1, col2 = st.columns(2)
        col1.metric("Jumlah Nasabah", f"{df.shape[0]:,}")

        if 'Klaster' in df.columns:
            col2.metric("Jumlah Segmen Ditemukan", df['Klaster'].nunique())
            st.write("Distribusi Nasabah per Segmen:")
            visualizer = VisualisasiData(df)
            success, chart, msg = visualizer.buat_pie_chart_klaster()
            if success:
                st.image(BytesIO(base64.b64decode(chart)), use_column_width=True)
            else:
                st.warning(msg)
    else:
        st.info("Data belum diproses. Silakan mulai dari halaman 'Manajemen Data'.")

# Halaman: Manajemen Data (Skenario PD-001)
def show_data_management():
    st.title("Шаг 1: Manajemen dan Proses Data")
    st.markdown("Unggah file `bank.csv` untuk memulai analisis.")

    uploaded_file = st.file_uploader("Unggah file CSV nasabah", type=["csv"])
    if uploaded_file:
        processor = DataProcessor(uploaded_file)
        success_load, df, msg_load = processor.load_data()

        if success_load:
            st.success(msg_load)
            st.dataframe(df.head())

            # Simpan data mentah ke session state untuk diproses
            st.session_state.raw_data = df

            expected_cols = ['age', 'balance', 'duration', 'campaign']
            success_val, msg_val = processor.validate_data_structure(expected_cols)
            if not success_val:
                st.error(msg_val)
                return

            if st.button("Proses Data (Pembersihan & Transformasi)"):
                with st.spinner("Membersihkan dan mentransformasi data..."):
                    processor.preprocess_data()
                    success_trans, df_trans, msg_trans = processor.transform_data()

                if success_trans:
                    st.session_state.processed_data = df_trans
                    st.success("Data berhasil diproses! Silakan lanjut ke 'Segmentasi Nasabah'.")
                    st.write("Contoh Data Setelah Transformasi:")
                    st.dataframe(st.session_state.processed_data.head())
                else:
                    st.error(msg_trans)
        else:
            st.error(msg_load)


# Halaman: Segmentasi (Skenario SN-01)
def show_segmentation():
    st.title("Шаг 2: Segmentasi Nasabah")
    if st.session_state.processed_data is None:
        st.warning("Data belum diproses. Silakan kembali ke halaman 'Manajemen Data'.")
        return

    st.subheader("Parameter K-Means")
    n_clusters = st.slider("Pilih Jumlah Klaster (Segmen)", min_value=2, max_value=8, value=4, step=1)

    if st.button("Jalankan Segmentasi"):
        with st.spinner("Melakukan proses clustering..."):
            segmenter = SegmentasiNasabah(st.session_state.processed_data, n_clusters)
            success, df_result, message = segmenter.jalankan_segmentasi()

        if success:
            st.session_state.app_data = df_result # Update data utama dengan hasil cluster
            st.success(message)
            st.subheader("Hasil Segmentasi")
            st.dataframe(df_result.head())
            st.markdown(get_table_download_link(df_result, "hasil_segmentasi.csv", "Unduh Hasil Segmentasi (CSV)"), unsafe_allow_html=True)
            st.info("Segmentasi selesai. Anda dapat melanjutkan ke 'Rekomendasi Produk' atau 'Laporan & Visualisasi'.")
        else:
            st.error(message)

# Halaman: Rekomendasi (Skenario RP-01)
def show_recommendation():
    st.title("Шаг 3: Rekomendasi Produk")
    if st.session_state.app_data is None or 'Klaster' not in st.session_state.app_data.columns:
        st.warning("Data belum disegmentasi. Silakan jalankan proses di halaman 'Segmentasi Nasabah'.")
        return

    df = st.session_state.app_data
    recommender = SistemRekomendasi(df)

    success_rec, df_rec, msg_rec = recommender.buat_rekomendasi()
    if success_rec:
        st.session_state.app_data = df_rec # Update lagi dengan kolom rekomendasi
        st.success(msg_rec)
        st.dataframe(df_rec)
        st.markdown(get_table_download_link(df_rec, "hasil_rekomendasi.csv", "Unduh Semua Rekomendasi (CSV)"), unsafe_allow_html=True)
    else:
        st.error(msg_rec)

# Halaman: Laporan & Visualisasi (Skenario VD-01)
def show_visualization():
    st.title("Шаг 4: Laporan dan Visualisasi")
    if st.session_state.app_data is None or 'Klaster' not in st.session_state.app_data.columns:
        st.warning("Data belum disegmentasi. Silakan jalankan proses di halaman 'Segmentasi Nasabah'.")
        return

    df = st.session_state.app_data
    visualizer = VisualisasiData(df)

    st.subheader("Distribusi Nasabah per Segmen")
    success_pie, pie_chart, msg_pie = visualizer.buat_pie_chart_klaster()
    if success_pie:
        st.image(BytesIO(base64.b64decode(pie_chart)))
    else:
        st.error(msg_pie)

    st.subheader("Analisis Fitur per Segmen")
    fitur_numerik = df.select_dtypes(include=np.number).columns.tolist()
    # Hapus 'Klaster' dari pilihan jika ada
    fitur_numerik = [f for f in fitur_numerik if 'Klaster' not in f]
    fitur_pilihan = st.selectbox("Pilih fitur untuk dianalisis", options=fitur_numerik)

    if fitur_pilihan:
        success_bar, bar_chart, msg_bar = visualizer.buat_bar_chart(fitur_pilihan)
        if success_bar:
            st.image(BytesIO(base64.b64decode(bar_chart)))
        else:
            st.error(msg_bar)

# Halaman: Manajemen Pengguna (Skenario MU-01)
def show_user_management():
    st.title("Manajemen Pengguna")
    if st.session_state.user_info['role'] != UserRole.ADMIN.value:
        st.error("Hanya Admin yang dapat mengakses halaman ini.")
        return

    st.subheader("Daftar Pengguna")
    df_users = st.session_state.user_mgmt.get_user_list_df()
    st.dataframe(df_users)
    st.info("Fitur tambah, edit, dan hapus pengguna dapat dikembangkan lebih lanjut di modul `user_management.py`.")


# --- Logika Utama Aplikasi ---
def main():
    """Fungsi utama untuk menjalankan alur aplikasi."""
    initialize_session_state()

    if not st.session_state.logged_in:
        show_login_page()
    else:
        st.set_page_config(page_title="Dashboard - Segmentasi Nasabah", layout="wide")
        choice = main_sidebar()

        if choice == "Dashboard":
            show_dashboard()
        elif choice == "Manajemen Data":
            show_data_management()
        elif choice == "Segmentasi Nasabah":
            show_segmentation()
        elif choice == "Rekomendasi Produk":
            show_recommendation()
        elif choice == "Laporan & Visualisasi":
            show_visualization()
        elif choice == "Manajemen Pengguna":
            show_user_management()

if __name__ == "__main__":
    main()