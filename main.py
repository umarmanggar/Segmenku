# import streamlit as st
# from datetime import datetime
# import logging
# from enum import Enum, auto
# import pandas as pd
# import time
# import base64
# from io import BytesIO


# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Enums untuk User Management
# class UserRole(Enum):
#     ADMIN = 'admin'
#     USER = 'user'
#     MARKETING = 'marketing'
#     MANAGEMENT = 'management'

# class UserStatus(Enum):
#     ACTIVE = 'active'
#     PENDING = 'pending'
#     REJECTED = 'rejected'
#     SUSPENDED = 'suspended'

# # Class User Management (sederhana)
# class User:
#     def __init__(self, username, password, role=UserRole.USER, status=UserStatus.PENDING, **kwargs):
#         self.username = username
#         self.password = password
#         self.role = role
#         self.status = status
#         self.full_name = kwargs.get('full_name', '')
#         self.email = kwargs.get('email', '')
#         self.phone = kwargs.get('phone', '')
#         self.created_at = datetime.now().isoformat()

# class UserManagement:
#     def __init__(self):
#         self.users = {}
#         self.current_user = None
#         # Tambah admin default
#         self._add_default_admin()

#     def _add_default_admin(self):
#         if 'admin' not in self.users:
#             self.users['admin'] = User(
#                 username='admin',
#                 password='admin123',
#                 role=UserRole.ADMIN,
#                 status=UserStatus.ACTIVE,
#                 full_name='Admin Sistem',
#                 email='admin@bank.com'
#             )

#     def login(self, username, password):
#         if username in self.users:
#             user = self.users[username]
#             if user.password == password:
#                 if user.status == UserStatus.ACTIVE:
#                     self.current_user = username
#                     return True, "Login berhasil", self._get_user_info(user)
#                 return False, "Akun belum aktif", None
#         return False, "Username atau password salah", None

#     def logout(self):
#         self.current_user = None

#     def get_current_user_info(self):
#         if self.current_user and self.current_user in self.users:
#             return self._get_user_info(self.users[self.current_user])
#         return None

#     def _get_user_info(self, user):
#         return {
#             'username': user.username,
#             'full_name': user.full_name,
#             'email': user.email,
#             'phone': user.phone,
#             'role': user.role.value,
#             'status': user.status.value,
#             'created_at': user.created_at
#         }

#     def get_daftar_pengguna(self):
#         """Get list of users as DataFrame"""
#         try:
#             users_data = []
#             for username, user in self.users.items():
#                 users_data.append({
#                     'Username': user.username,
#                     'Nama Lengkap': user.full_name,
#                     'Email': user.email,
#                     'Role': user.role.value,
#                     'Status': user.status.value,
#                     'Dibuat': user.created_at
#                 })
#             df = pd.DataFrame(users_data)
#             return True, df, "Data pengguna berhasil dimuat"
#         except Exception as e:
#             return False, None, f"Error: {str(e)}"

# class MainApplication:
#     def __init__(self):
#         if 'user_mgmt' not in st.session_state:
#             st.session_state.user_mgmt = UserManagement()
#         if 'page' not in st.session_state:
#             st.session_state.page = 'login'
#         if 'show_register' not in st.session_state:
#             st.session_state.show_register = False

#     def run(self):
#         st.set_page_config(
#             page_title="Sistem Rekomendasi Produk Bank",
#             page_icon="🏦",
#             layout="wide"
#         )

# # Initialize session state
# def initialize_session_state():
#     """Initialize session state variables"""
#     if 'user_mgmt' not in st.session_state:
#         st.session_state.user_mgmt = UserManagement()
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False
#     if 'user_data' not in st.session_state:
#         st.session_state.user_data = {}
#     if 'current_page' not in st.session_state:
#         st.session_state.current_page = 'Dashboard'
#     # Initialize visualisasi globally or pass it as an argument
#     if 'visualisasi_object' not in st.session_state:
#         st.session_state['visualisasi_object'] = None

# # Fungsi utilitas
# def to_excel(df):
#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         df.to_excel(writer, index=False)
#     processed_data = output.getvalue()
#     return processed_data

# def get_table_download_link(df, filename):
#     val = to_excel(df)
#     b64 = base64.b64encode(val)
#     return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.xlsx">Download {filename}</a>'

# # Tampilan login
# def show_login():
#     st.title("Login Sistem Segmentasi Nasabah")

#     with st.form("login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         submitted = st.form_submit_button("Login")

#         if submitted:
#             success, message, user_data = st.session_state.user_mgmt.login(username, password)
#             if success:
#                 st.session_state['logged_in'] = True
#                 st.session_state['user_data'] = user_data
#                 st.success(message)
#                 time.sleep(1)
#                 st.rerun()
#             else:
#                 st.error(message)

# # Menu utama berdasarkan role
# def main_menu():
#     st.sidebar.title("Menu Utama")
#     user_data = st.session_state.get('user_data', {})

#     if user_data.get('role') == UserRole.ADMIN.value:
#         menu_options = ["Dashboard", "Manajemen Data", "Manajemen Pengguna", "Logout"]
#     elif user_data.get('role') == UserRole.MARKETING.value:
#         menu_options = ["Dashboard", "Segmentasi Nasabah", "Rekomendasi Produk", "Logout"]
#     else:  # MANAGEMENT or other roles
#         menu_options = ["Dashboard", "Laporan", "Visualisasi", "Logout"]

#     selected_menu = st.sidebar.radio("Pilihan Menu", menu_options)

#     if selected_menu == "Logout":
#         st.session_state.clear()
#         initialize_session_state()  # Re-initialize after clearing
#         st.success("Anda telah logout")
#         time.sleep(1)
#         st.rerun()

#     return selected_menu

# # Halaman dashboard
# def show_dashboard():
#     st.title("Dashboard Segmentasi Nasabah")
#     user_data = st.session_state.get('user_data', {})

#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader(f"Halo, {user_data.get('full_name', 'User')}")
#         st.write(f"Role: {user_data.get('role', '').capitalize()}")
#         st.write(f"Login terakhir: {pd.to_datetime('now').strftime('%Y-%m-%d %H:%M')}")

#     with col2:
#         st.subheader("Quick Actions")
#         if user_data.get('role') == UserRole.ADMIN.value:
#             if st.button("Manajemen Pengguna"):
#                 st.session_state['current_page'] = "Manajemen Pengguna"
#                 st.rerun()
#         elif user_data.get('role') == UserRole.MARKETING.value:
#             if st.button("Segmentasi Nasabah"):
#                 st.session_state['current_page'] = "Segmentasi Nasabah"
#                 st.rerun()

#     st.markdown("---")
#     st.subheader("Statistik Sistem")

#     # Tampilkan statistik sesuai role
#     if 'df' in st.session_state:
#         df = st.session_state['df']
#         if 'Klaster' in df.columns:
#             cluster_stats = df['Klaster'].value_counts()
#             st.write("Distribusi Klaster Nasabah:")
#             st.bar_chart(cluster_stats)

# # Halaman manajemen data
# def show_data_management():
#     st.title("Manajemen Data Nasabah")

#     try:
#         from dataload import DataProcessor
#     except ImportError:
#         st.error("Module 'dataload' tidak ditemukan. Pastikan file dataload.py ada di direktori yang sama.")
#         return

#     uploaded_file = st.file_uploader("Upload File CSV Nasabah", type=["csv"])

#     if uploaded_file is not None:
#         try:
#             # Proses data
#             data_processor = DataProcessor(uploaded_file)
#             success, df, message = data_processor.load_data()
#             if success:
#                 st.session_state['df'] = df
#                 st.success(message)

#                 # Validasi struktur data
#                 expected_columns = ['age', 'balance', 'duration', 'campaign']
#                 success_val, msg_val = data_processor.validate_data_structure(expected_columns)
#                 if success_val:
#                     st.success(msg_val)

#                     # Preprocessing
#                     success_pre, df_pre, msg_pre = data_processor.preprocess_data()
#                     if success_pre:
#                         st.session_state['df'] = df_pre
#                         st.success(msg_pre)

#                         # Pilih fitur
#                         success_sel, df_sel, msg_sel = data_processor.select_features(expected_columns)
#                         if success_sel:
#                             st.session_state['df'] = df_sel
#                             st.success(msg_sel)

#                             # Transformasi data
#                             success_trans, df_trans, msg_trans = data_processor.transform_data()
#                             if success_trans:
#                                 st.session_state['df'] = df_trans
#                                 st.success(msg_trans)

#                                 # Tampilkan data
#                                 if st.checkbox("Tampilkan Data"):
#                                     st.dataframe(df_trans.head())

#                                 # Download data
#                                 st.markdown(get_table_download_link(df_trans, "data_nasabah_processed"), unsafe_allow_html=True)
#                 else:
#                     st.error(msg_val)
#             else:
#                 st.error(message)
#         except Exception as e:
#             st.error(f"Error processing data: {str(e)}")

# # Halaman segmentasi nasabah
# def show_segmentation():
#     st.title("Segmentasi Nasabah")

#     if 'df' not in st.session_state:
#         st.warning("Silakan upload data terlebih dahulu di menu Manajemen Data")
#         return

#     df = st.session_state['df']

#     st.subheader("Parameter Segmentasi")
#     n_clusters = st.slider("Jumlah Klaster", 2, 6, 4)

#     try:
#         from clustering import SegmentasiNasabah
#     except ImportError:
#         st.error("Module 'clustering' tidak ditemukan. Pastikan file clustering.py ada di direktori yang sama.")
#         return

#     if st.button("Jalankan Segmentasi"):
#         with st.spinner("Sedang memproses segmentasi..."):
#             segmentasi = SegmentasiNasabah(df, n_clusters)
#             success, df_result, message = segmentasi.jalankan_segmentasi()

#             if success:
#                 st.session_state['df'] = df_result
#                 st.success(message)

#                 # Tampilkan hasil
#                 st.subheader("Hasil Segmentasi")
#                 st.dataframe(df_result[['Klaster'] + segmentasi.fitur_numerik].head())

#                 # Visualisasi
#                 try:
#                     from visualisasi import VisualisasiData
#                     visualisasi = VisualisasiData(df_result)
#                     st.session_state['visualisasi_object'] = visualisasi # Store the object in session state
#                     success_viz, img_base64, msg_viz = visualisasi.buat_pie_chart_klaster()
#                     if success_viz:
#                         st.image(BytesIO(base64.b64decode(img_base64)), caption="Distribusi Klaster")
#                 except ImportError:
#                     st.warning("Module 'visualisasi' tidak ditemukan untuk menampilkan grafik.")

#                 # Simpan hasil
#                 if st.button("Simpan Hasil Segmentasi"):
#                     success_save, msg_save = segmentasi.simpan_hasil("hasil_segmentasi.csv")
#                     if success_save:
#                         st.success(msg_save)
#                     else:
#                         st.error(msg_save)
#             else:
#                 st.error(message)

# # Halaman rekomendasi produk
# def show_recommendation():
#     st.title("Rekomendasi Produk")

#     if 'df' not in st.session_state or 'Klaster' not in st.session_state['df'].columns:
#         st.warning("Silakan lakukan segmentasi terlebih dahulu")
#         return

#     df = st.session_state['df']

#     try:
#         from rekomendasi import SistemRekomendasi
#     except ImportError:
#         st.error("Module 'rekomendasi' tidak ditemukan. Pastikan file rekomendasi.py ada di direktori yang sama.")
#         return

#     st.subheader("Sistem Rekomendasi Produk")
#     sistem_rekomendasi = SistemRekomendasi(df)

#     # Buat rekomendasi
#     if st.button("Buat Rekomendasi"):
#         success, df_rekomendasi, message = sistem_rekomendasi.buat_rekomendasi()
#         if success:
#             st.session_state['df'] = df_rekomendasi
#             st.success(message)

#             # Tampilkan rekomendasi
#             st.dataframe(df_rekomendasi[['Klaster', 'Produk_Rekomendasi', 'Kategori_Produk']].head())

#             # Filter berdasarkan kategori
#             kategori = st.selectbox("Filter berdasarkan kategori", ['Semua', 'Tabungan', 'Kredit', 'Investasi', 'Asuransi'])
#             if kategori != 'Semua':
#                 success_filter, df_filter, msg_filter = sistem_rekomendasi.filter_rekomendasi(kategori)
#                 if success_filter:
#                     st.dataframe(df_filter[['Klaster', 'Produk_Rekomendasi']])

#             # Detail produk
#             produk_terpilih = st.selectbox("Lihat detail produk",
#                                          list(set(df_rekomendasi['Produk_Rekomendasi'])))
#             if st.button("Tampilkan Detail"):
#                 success_detail, detail, msg_detail = sistem_rekomendasi.tampilkan_detail_produk(produk_terpilih)
#                 if success_detail:
#                     st.json(detail)

#             # Ekspor rekomendasi
#             if st.button("Ekspor Rekomendasi ke CSV"):
#                 success_export, filename, msg_export = sistem_rekomendasi.ekspor_rekomendasi_csv()
#                 if success_export:
#                     st.success(msg_export)
#                     st.markdown(f'<a href="data:file/csv;base64,{base64.b64encode(open(filename, "rb").read()).decode()}" download="{filename}">Download {filename}</a>', unsafe_allow_html=True)
#         else:
#             st.error(message)

# # Halaman manajemen pengguna (admin only)
# def show_user_management():
#     # Ensure user_mgmt is initialized
#     if 'user_mgmt' not in st.session_state:
#         st.session_state.user_mgmt = UserManagement()
#     user_mgmt = st.session_state.user_mgmt

#     st.title("Manajemen Pengguna")

#     if st.session_state.get('user_data', {}).get('role') != UserRole.ADMIN.value:
#         st.warning("Anda tidak memiliki akses ke halaman ini")
#         return

#     tab1, tab2, tab3 = st.tabs(["Daftar Pengguna", "Tambah Pengguna", "Edit Pengguna"])

#     with tab1:
#         st.subheader("Daftar Pengguna")
#         success, df_users, message = user_mgmt.get_daftar_pengguna()
#         if success:
#             st.dataframe(df_users)
#         else:
#             st.error(message)

#     with tab2:
#         st.subheader("Tambah Pengguna Baru")
#         with st.form("add_user_form"):
#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             full_name = st.text_input("Nama Lengkap")
#             email = st.text_input("Email")
#             role = st.selectbox("Role", [r.value for r in UserRole])
#             department = st.text_input("Departemen")

#             submitted = st.form_submit_button("Tambah Pengguna")
#             if submitted:
#                 # Add logic to add user to user_mgmt.users
#                 if username not in user_mgmt.users:
#                     user_mgmt.users[username] = User(
#                         username=username,
#                         password=password,
#                         role=UserRole(role),
#                         full_name=full_name,
#                         email=email
#                     )
#                     st.success(f"Pengguna {username} berhasil ditambahkan")
#                 else:
#                     st.error(f"Pengguna dengan username {username} sudah ada.")

#     with tab3:
#         st.subheader("Edit Pengguna")
#         # Implementasi edit pengguna
#         if user_mgmt.users: # Ensure there are users to select
#             username_to_edit = st.selectbox("Pilih Pengguna", list(user_mgmt.users.keys()))
#             user = user_mgmt.users[username_to_edit]
#             with st.form("edit_user_form"):
#                 new_password = st.text_input("Password Baru", type="password", value=user.password) # Pre-fill with current password
#                 new_full_name = st.text_input("Nama Lengkap", value=user.full_name)
#                 new_email = st.text_input("Email", value=user.email)
#                 new_role = st.selectbox("Role", [r.value for r in UserRole], index=list(UserRole).index(user.role))
#                 new_status = st.selectbox("Status", [s.value for s in UserStatus], index=list(UserStatus).index(user.status))

#                 submitted = st.form_submit_button("Simpan Perubahan")
#                 if submitted:
#                     # Implementasi simpan perubahan
#                     user.password = new_password
#                     user.full_name = new_full_name
#                     user.email = new_email
#                     user.role = UserRole(new_role)
#                     user.status = UserStatus(new_status)
#                     st.success(f"Pengguna {username_to_edit} berhasil diperbarui")
#         else:
#             st.info("Tidak ada pengguna untuk diedit.")

# # Halaman visualisasi
# def show_visualization():
#     try:
#         from visualisasi import VisualisasiData
#     except ImportError:
#         st.error("Module 'visualisasi' tidak ditemukan. Pastikan file visualisasi.py ada di direktori yang sama.")
#         return

#     st.title("Visualisasi Data")

#     if 'df' not in st.session_state or 'Klaster' not in st.session_state['df'].columns:
#         st.warning("Silakan lakukan segmentasi terlebih dahulu")
#         return

#     df = st.session_state['df']

#     # Use the visualisasi object from session state, or create it if not present
#     if st.session_state['visualisasi_object'] is None or st.session_state['visualisasi_object'].df is not df:
#         st.session_state['visualisasi_object'] = VisualisasiData(df)
#     visualisasi = st.session_state['visualisasi_object']


#     st.subheader("Visualisasi Segmentasi")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.write("Distribusi Klaster")
#         success_pie, img_pie, msg_pie = visualisasi.buat_pie_chart_klaster()
#         if success_pie:
#             st.image(BytesIO(base64.b64decode(img_pie)))
#         else:
#             st.error(msg_pie)

#     with col2:
#         st.write("Distribusi Usia per Klaster")
#         success_bar, img_bar, msg_bar = visualisasi.buat_bar_chart_usia()
#         if success_bar:
#             st.image(BytesIO(base64.b64decode(img_bar)))
#         else:
#             st.error(msg_bar)

#     st.subheader("Filter Visualisasi")
#     # Ensure 'df' is available and has columns for filtering
#     if 'df' in st.session_state and not st.session_state['df'].empty:
#         fitur_filter = st.selectbox("Pilih Fitur untuk Filter", df.columns)
#         if fitur_filter: # Check if a feature is selected
#             nilai_filter = st.selectbox("Pilih Nilai Filter", df[fitur_filter].unique())

#             if st.button("Terapkan Filter"):
#                 success_filter, hasil_filter, msg_filter = visualisasi.filter_dan_update_grafik(fitur_filter, nilai_filter)
#                 if success_filter:
#                     st.image(BytesIO(base64.b64decode(hasil_filter['pie_chart'])), caption=f"Distribusi Klaster (Filtered by {fitur_filter}: {nilai_filter})")
#                     st.image(BytesIO(base64.b64decode(hasil_filter['bar_chart'])), caption=f"Distribusi Usia per Klaster (Filtered by {fitur_filter}: {nilai_filter})")
#                 else:
#                     st.error(msg_filter)
#         else:
#             st.warning("Tidak ada fitur yang tersedia untuk filter.")
#     else:
#         st.warning("Tidak ada data untuk difilter.")

# # Aplikasi utama
# def main():
#     initialize_session_state() # Call initialization at the very beginning
#     if not st.session_state.get('logged_in'):
#         show_login()
#     else:
#         selected_menu = main_menu()

#         if selected_menu == "Dashboard":
#             show_dashboard()
#         elif selected_menu == "Manajemen Data":
#             show_data_management()
#         elif selected_menu == "Segmentasi Nasabah":
#             show_segmentation()
#         elif selected_menu == "Rekomendasi Produk":
#             show_recommendation()
#         elif selected_menu == "Manajemen Pengguna":
#             show_user_management()
#         elif selected_menu == "Visualisasi":
#             show_visualization()

# if __name__ == "__main__":
#     main()

# File: main.py
# Deskripsi: File utama untuk menjalankan aplikasi web Streamlit.
# Mengintegrasikan semua modul lain untuk menyediakan fungsionalitas penuh.
# Relevan dengan seluruh SRS dan Test Case.

import streamlit as st
import pandas as pd
import time
from io import BytesIO
import base64
import numpy as np

# --- Impor Modul Aplikasi ---
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
    if 'df_processed' not in st.session_state:
        st.session_state.df_processed = None
    if 'df_clustered' not in st.session_state:
        st.session_state.df_clustered = None

# --- Fungsi Utilitas ---
def get_table_download_link(df, filename, text):
    """Membuat link download untuk DataFrame."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

# --- Halaman & Komponen UI ---

# Skenario: Login (TS.Log.004)
def show_login_page():
    """Menampilkan form login."""
    st.set_page_config(page_title="Login - Segmentasi Nasabah", layout="centered")
    st.title("Sistem Segmentasi & Rekomendasi Nasabah")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        submitted = st.form_submit_button("Login")

        if submitted:
            success, message, user_info = st.session_state.user_mgmt.login(username, password)
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
    user_role = st.session_state.user_info['role']
    st.sidebar.title(f"Menu - {user_role.capitalize()}")

    # Opsi menu berdasarkan peran dari SRS 2.3
    if user_role == UserRole.ADMIN.value:
        options = ["Dashboard", "Manajemen Data", "Manajemen Pengguna"]
    elif user_role == UserRole.MARKETING.value:
        options = ["Dashboard", "Segmentasi Nasabah", "Rekomendasi Produk"]
    elif user_role == UserRole.MANAGEMENT.value:
        options = ["Dashboard", "Laporan & Visualisasi"]
    else:
        options = ["Dashboard"]

    choice = st.sidebar.radio("Navigasi", options)

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Anda telah berhasil logout.")
        time.sleep(1)
        st.rerun()

    return choice

# Halaman: Dashboard
def show_dashboard():
    st.title(f"👋 Halo, {st.session_state.user_info['full_name']}!")
    st.markdown("Selamat datang di Dashboard Sistem Segmentasi Nasabah.")

    st.subheader("Ringkasan Data")
    if st.session_state.df_clustered is not None:
        df = st.session_state.df_clustered
        col1, col2 = st.columns(2)
        col1.metric("Jumlah Nasabah", f"{df.shape[0]:,}")
        col2.metric("Jumlah Segmen", df['Klaster'].nunique())

        st.write("Distribusi Nasabah per Segmen:")
        # Menggunakan VisualisasiData untuk membuat chart
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
    st.title("Manajemen Data")
    st.markdown("Unggah, validasi, dan proses data nasabah di sini.")

    # Test Case PD-001-01
    uploaded_file = st.file_uploader("Unggah file bank.csv", type=["csv"])
    if uploaded_file:
        processor = DataProcessor(uploaded_file)
        success_load, df, msg_load = processor.load_data()

        if success_load:
            st.success(msg_load)
            st.dataframe(df.head())

            # Kolom yang diharapkan untuk validasi dan fitur
            expected_cols = ['age', 'balance', 'duration', 'campaign']

            # Test Case PD-001-02, PD-001-03
            success_val, msg_val = processor.validate_data_structure(expected_cols)
            if not success_val:
                st.error(msg_val)
                return

            # Test Case PD-001-04, PD-001-06
            if st.button("Proses Data (Pembersihan & Transformasi)"):
                with st.spinner("Membersihkan data..."):
                    success_pre, df_pre, msg_pre = processor.preprocess_data()
                    if not success_pre:
                        st.error(msg_pre)
                        return

                with st.spinner("Melakukan transformasi data..."):
                    processor.data = df_pre # Update data di prosesor
                    success_trans, df_trans, msg_trans = processor.transform_data()

                if success_trans:
                    st.session_state.df_processed = df_trans
                    st.success("Data berhasil diproses dan siap untuk segmentasi!")
                    st.write("Data setelah transformasi:")
                    st.dataframe(st.session_state.df_processed.head())
                else:
                    st.error(msg_trans)
        else:
            st.error(msg_load)

# Halaman: Segmentasi (Skenario SN-01)
def show_segmentation():
    st.title("Segmentasi Nasabah")
    if st.session_state.df_processed is None:
        st.warning("Data belum diproses. Silakan proses data di halaman 'Manajemen Data'.")
        return

    st.subheader("Parameter K-Means")
    # REQ-1.2: Administrator dapat mengonfigurasi jumlah cluster
    n_clusters = st.slider("Pilih Jumlah Klaster (Segmen)", min_value=2, max_value=8, value=4, step=1)

    # Test Case SN-01-01
    if st.button("Jalankan Segmentasi"):
        with st.spinner("Melakukan proses clustering..."):
            # Gunakan hanya kolom numerik untuk K-Means
            numeric_df = st.session_state.df_processed.select_dtypes(include=np.number)
            segmenter = SegmentasiNasabah(numeric_df, n_clusters)
            success, df_result, message = segmenter.jalankan_segmentasi()

        if success:
            st.session_state.df_clustered = pd.concat([st.session_state.df_processed, df_result['Klaster']], axis=1)
            st.success(message)

            # Test Case SN-01-02
            st.subheader("Hasil Segmentasi")
            st.dataframe(st.session_state.df_clustered.head())
            st.markdown(get_table_download_link(st.session_state.df_clustered, "hasil_segmentasi.csv", "Unduh Hasil Segmentasi (CSV)"), unsafe_allow_html=True)

        else:
            st.error(message)

# Halaman: Rekomendasi (Skenario RP-01)
def show_recommendation():
    st.title("Rekomendasi Produk")
    if st.session_state.df_clustered is None:
        st.warning("Data belum disegmentasi. Silakan jalankan segmentasi terlebih dahulu.")
        return

    df = st.session_state.df_clustered
    recommender = SistemRekomendasi(df)

    # Test Case RP-01-01
    success_rec, df_rec, msg_rec = recommender.buat_rekomendasi()
    if success_rec:
        st.success(msg_rec)

        # Test Case RP-01-04
        st.subheader("Filter Rekomendasi")
        kategori_unik = ['Semua'] + list(df_rec['Kategori_Produk'].unique())
        pilihan_kategori = st.selectbox("Filter berdasarkan Kategori Produk", options=kategori_unik)

        if pilihan_kategori == 'Semua':
            st.dataframe(df_rec)
        else:
            success_filter, df_filtered, msg_filter = recommender.filter_rekomendasi(pilihan_kategori)
            if success_filter:
                st.dataframe(df_filtered)
            else:
                st.error(msg_filter)

        # Test Case RP-01-05
        st.markdown(get_table_download_link(df_rec, "hasil_rekomendasi.csv", "Unduh Semua Rekomendasi (CSV)"), unsafe_allow_html=True)
    else:
        st.error(msg_rec)

# Halaman: Laporan & Visualisasi (Skenario VD-01)
def show_visualization():
    st.title("Laporan dan Visualisasi")
    if st.session_state.df_clustered is None:
        st.warning("Data belum disegmentasi.")
        return

    df = st.session_state.df_clustered
    visualizer = VisualisasiData(df)

    st.subheader("Distribusi Nasabah per Segmen")
    # Test Case VD-01-01
    success_pie, pie_chart, msg_pie = visualizer.buat_pie_chart_klaster()
    if success_pie:
        st.image(BytesIO(base64.b64decode(pie_chart)))
    else:
        st.error(msg_pie)

    st.subheader("Analisis Fitur per Segmen")
    # Test Case VD-01-02
    fitur_numerik = df.select_dtypes(include=np.number).columns.tolist()
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

    # Test Case MU-01-01: Verifikasi akses admin
    if st.session_state.user_info['role'] != UserRole.ADMIN.value:
        st.error("Hanya Admin yang dapat mengakses halaman ini.")
        return

    st.subheader("Daftar Pengguna")
    df_users = st.session_state.user_mgmt.get_user_list_df()
    st.dataframe(df_users)

    st.subheader("Fitur Manajemen")
    st.warning("Fitur tambah, edit, dan hapus pengguna sedang dalam pengembangan.")


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