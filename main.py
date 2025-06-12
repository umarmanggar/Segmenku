import streamlit as st
from datetime import datetime
import logging
from enum import Enum, auto
import pandas as pd
import time
import base64
from io import BytesIO


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enums untuk User Management
class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'

class UserStatus(Enum):
    ACTIVE = 'active'
    PENDING = 'pending'
    REJECTED = 'rejected'
    SUSPENDED = 'suspended'

# Class User Management (sederhana)
class User:
    def __init__(self, username, password, role=UserRole.USER, status=UserStatus.PENDING, **kwargs):
        self.username = username
        self.password = password
        self.role = role
        self.status = status
        self.full_name = kwargs.get('full_name', '')
        self.email = kwargs.get('email', '')
        self.phone = kwargs.get('phone', '')
        self.created_at = datetime.now().isoformat()

class UserManagement:
    def __init__(self):
        self.users = {}
        self.current_user = None
        # Tambah admin default
        self._add_default_admin()

    def _add_default_admin(self):
        if 'admin' not in self.users:
            self.users['admin'] = User(
                username='admin',
                password='admin123',
                role=UserRole.ADMIN,
                status=UserStatus.ACTIVE,
                full_name='Admin Sistem',
                email='admin@bank.com'
            )

    def login(self, username, password):
        if username in self.users:
            user = self.users[username]
            if user.password == password:
                if user.status == UserStatus.ACTIVE:
                    self.current_user = username
                    return True, "Login berhasil", self._get_user_info(user)
                return False, "Akun belum aktif", None
        return False, "Username atau password salah", None

    def logout(self):
        self.current_user = None

    def get_current_user_info(self):
        if self.current_user and self.current_user in self.users:
            return self._get_user_info(self.users[self.current_user])
        return None

    def _get_user_info(self, user):
        return {
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role.value,
            'status': user.status.value,
            'created_at': user.created_at
        }

class MainApplication:
    def __init__(self):
        if 'user_mgmt' not in st.session_state:
            st.session_state.user_mgmt = UserManagement()
        if 'page' not in st.session_state:
            st.session_state.page = 'login'
        if 'show_register' not in st.session_state:
            st.session_state.show_register = False

    def run(self):
        st.set_page_config(
            page_title="Sistem Rekomendasi Produk Bank",
            page_icon="🏦",
            layout="wide"
        )

# Fungsi utilitas
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df, filename):
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.xlsx">Download {filename}</a>'

# Tampilan login
def show_login():
    st.title("Login Sistem Segmentasi Nasabah")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            success, message, user_data = st.session_state.user_mgmt.login(username, password)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['user_data'] = user_data
                st.success(message)
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error(message)
# Menu utama berdasarkan role
def main_menu():
    st.sidebar.title("Menu Utama")
    user_data = st.session_state.get('user_data', {})

    if user_data['role'] == UserRole.ADMIN.value:
        menu_options = ["Dashboard", "Manajemen Data", "Manajemen Pengguna", "Logout"]
    elif user_data['role'] == UserRole.MARKETING.value:
        menu_options = ["Dashboard", "Segmentasi Nasabah", "Rekomendasi Produk", "Logout"]
    else:  # MANAGEMENT
        menu_options = ["Dashboard", "Laporan", "Visualisasi", "Logout"]

    selected_menu = st.sidebar.radio("Pilihan Menu", menu_options)

    if selected_menu == "Logout":
        st.session_state.clear()
        st.success("Anda telah logout")
        time.sleep(1)
        st.experimental_rerun()

    return selected_menu

# Halaman dashboard
def show_dashboard():
    st.title("Dashboard Segmentasi Nasabah")
    user_data = st.session_state.get('user_data', {})

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Halo, {user_data.get('full_name', 'User')}")
        st.write(f"Role: {user_data.get('role', '').capitalize()}")
        st.write(f"Login terakhir: {pd.to_datetime('now').strftime('%Y-%m-%d %H:%M')}")

    with col2:
        st.subheader("Quick Actions")
        if user_data['role'] == UserRole.ADMIN.value:
            if st.button("Manajemen Pengguna"):
                st.session_state['current_page'] = "Manajemen Pengguna"
                st.experimental_rerun()
        elif user_data['role'] == UserRole.MARKETING.value:
            if st.button("Segmentasi Nasabah"):
                st.session_state['current_page'] = "Segmentasi Nasabah"
                st.experimental_rerun()

    st.markdown("---")
    st.subheader("Statistik Sistem")

    # Tampilkan statistik sesuai role
    if 'df' in st.session_state:
        df = st.session_state['df']
        if 'Klaster' in df.columns:
            cluster_stats = df['Klaster'].value_counts()
            st.write("Distribusi Klaster Nasabah:")
            st.bar_chart(cluster_stats)

# Halaman manajemen data
def show_data_management():
    st.title("Manajemen Data Nasabah")

    from dataload import DataProcessor

    uploaded_file = st.file_uploader("Upload File CSV Nasabah", type=["csv"])

    if uploaded_file is not None:
        try:
            # Proses data
            data_processor = DataProcessor(uploaded_file)
            success, df, message = data_processor.load_data()
            if success:
                st.session_state['df'] = df
                st.success(message)

                # Validasi struktur data
                expected_columns = ['usia', 'saldo', 'pendapatan', 'frekuensi_transaksi']
                success_val, msg_val = data_processor.validate_data_structure(expected_columns)
                if success_val:
                    st.success(msg_val)

                    # Preprocessing
                    success_pre, df_pre, msg_pre = data_processor.preprocess_data()
                    if success_pre:
                        st.session_state['df'] = df_pre
                        st.success(msg_pre)

                        # Pilih fitur
                        success_sel, df_sel, msg_sel = data_processor.select_features(expected_columns)
                        if success_sel:
                            st.session_state['df'] = df_sel
                            st.success(msg_sel)

                            # Transformasi data
                            success_trans, df_trans, msg_trans = data_processor.transform_data()
                            if success_trans:
                                st.session_state['df'] = df_trans
                                st.success(msg_trans)

                                # Tampilkan data
                                if st.checkbox("Tampilkan Data"):
                                    st.dataframe(df_trans.head())

                                # Download data
                                st.markdown(get_table_download_link(df_trans, "data_nasabah_processed"), unsafe_allow_html=True)
                else:
                    st.error(msg_val)
            else:
                st.error(message)
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")# Halaman segmentasi nasabah
def show_segmentation():
    st.title("Segmentasi Nasabah")

    if 'df' not in st.session_state:
        st.warning("Silakan upload data terlebih dahulu di menu Manajemen Data")
        return

    df = st.session_state['df']

    st.subheader("Parameter Segmentasi")
    n_clusters = st.slider("Jumlah Klaster", 2, 6, 4)

    from clustering import SegmentasiNasabah
    if st.button("Jalankan Segmentasi"):
        with st.spinner("Sedang memproses segmentasi..."):
            global segmentasi
            segmentasi = SegmentasiNasabah(df, n_clusters)
            success, df_result, message = segmentasi.jalankan_segmentasi()

            if success:
                st.session_state['df'] = df_result
                st.success(message)

                # Tampilkan hasil
                st.subheader("Hasil Segmentasi")
                st.dataframe(df_result[['Klaster'] + segmentasi.fitur_numerik].head())

                # Visualisasi
                from visualisasi import VisualisasiData
                global visualisasi
                visualisasi = VisualisasiData(df_result)
                success_viz, img_base64, msg_viz = visualisasi.buat_pie_chart_klaster()
                if success_viz:
                    st.image(BytesIO(base64.b64decode(img_base64)), caption="Distribusi Klaster")

                # Simpan hasil
                if st.button("Simpan Hasil Segmentasi"):
                    success_save, msg_save = segmentasi.simpan_hasil("hasil_segmentasi.csv")
                    if success_save:
                        st.success(msg_save)
                    else:
                        st.error(msg_save)
            else:
                st.error(message)

# Halaman rekomendasi produk
def show_recommendation():
    st.title("Rekomendasi Produk")

    if 'df' not in st.session_state or 'Klaster' not in st.session_state['df'].columns:
        st.warning("Silakan lakukan segmentasi terlebih dahulu")
        return

    df = st.session_state['df']
    from rekomendasi import SistemRekomendasi
    import base64
    st.subheader("Sistem Rekomendasi Produk")
    global sistem_rekomendasi
    sistem_rekomendasi = SistemRekomendasi(df)

    # Buat rekomendasi
    if st.button("Buat Rekomendasi"):
        success, df_rekomendasi, message = sistem_rekomendasi.buat_rekomendasi()
        if success:
            st.session_state['df'] = df_rekomendasi
            st.success(message)

            # Tampilkan rekomendasi
            st.dataframe(df_rekomendasi[['Klaster', 'Produk_Rekomendasi', 'Kategori_Produk']].head())

            # Filter berdasarkan kategori
            kategori = st.selectbox("Filter berdasarkan kategori", ['Semua', 'Tabungan', 'Kredit', 'Investasi', 'Asuransi'])
            if kategori != 'Semua':
                success_filter, df_filter, msg_filter = sistem_rekomendasi.filter_rekomendasi(kategori)
                if success_filter:
                    st.dataframe(df_filter[['Klaster', 'Produk_Rekomendasi']])

            # Detail produk
            produk_terpilih = st.selectbox("Lihat detail produk",
                                         list(set(df_rekomendasi['Produk_Rekomendasi'])))
            if st.button("Tampilkan Detail"):
                success_detail, detail, msg_detail = sistem_rekomendasi.tampilkan_detail_produk(produk_terpilih)
                if success_detail:
                    st.json(detail)

            # Ekspor rekomendasi
            if st.button("Ekspor Rekomendasi ke CSV"):
                success_export, filename, msg_export = sistem_rekomendasi.ekspor_rekomendasi_csv()
                if success_export:
                    st.success(msg_export)
                    st.markdown(f'<a href="data:file/csv;base64,{base64.b64encode(open(filename, "rb").read()).decode()}" download="{filename}">Download {filename}</a>', unsafe_allow_html=True)
        else:
            st.error(message)

# Halaman manajemen pengguna (admin only)
def show_user_management():
    from user_management import UserManagement
    user_mgmt = UserManagement()

    st.title("Manajemen Pengguna")

    if st.session_state.get('user_data', {}).get('role') != UserRole.ADMIN.value:
        st.warning("Anda tidak memiliki akses ke halaman ini")
        return

    tab1, tab2, tab3 = st.tabs(["Daftar Pengguna", "Tambah Pengguna", "Edit Pengguna"])

    with tab1:
        st.subheader("Daftar Pengguna")
        success, df_users, message = user_mgmt.get_daftar_pengguna()
        if success:
            st.dataframe(df_users)
        else:
            st.error(message)

    with tab2:
        st.subheader("Tambah Pengguna Baru")
        with st.form("add_user_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            full_name = st.text_input("Nama Lengkap")
            email = st.text_input("Email")
            role = st.selectbox("Role", [r.value for r in UserRole])
            department = st.text_input("Departemen")

            submitted = st.form_submit_button("Tambah Pengguna")
            if submitted:
                # Implementasi tambah pengguna
                st.success(f"Pengguna {username} berhasil ditambahkan")

    with tab3:
        st.subheader("Edit Pengguna")
        # Implementasi edit pengguna
        with st.form("edit_user_form"):
            username = st.selectbox("Pilih Pengguna", list(user_mgmt.users.keys()))
            user = user_mgmt.users[username]
            new_password = st.text_input("Password Baru", type="password")
            new_full_name = st.text_input("Nama Lengkap", value=user.full_name)
            new_email = st.text_input("Email", value=user.email)
            new_role = st.selectbox("Role", [r.value for r in UserRole], index=list(UserRole).index(user.role))
            new_status = st.selectbox("Status", [s.value for s in UserStatus], index=list(UserStatus).index(user.status))

            submitted = st.form_submit_button("Simpan Perubahan")
            if submitted:
                # Implementasi simpan perubahan
                user.password = new_password
                user.full_name = new_full_name
                user.email = new_email
                user.role = UserRole(new_role)
                user.status = UserStatus(new_status)
                st.success(f"Pengguna {username} berhasil diperbarui")
# Halaman visualisasi
def show_visualization():
    from visualisasi import VisualisasiData
    st.title("Visualisasi Data")

    if 'df' not in st.session_state or 'Klaster' not in st.session_state['df'].columns:
        st.warning("Silakan lakukan segmentasi terlebih dahulu")
        return

    df = st.session_state['df']
    global visualisasi
    if visualisasi is None:
        visualisasi = VisualisasiData(df)

    st.subheader("Visualisasi Segmentasi")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Distribusi Klaster")
        success_pie, img_pie, msg_pie = visualisasi.buat_pie_chart_klaster()
        if success_pie:
            st.image(BytesIO(base64.b64decode(img_pie)))

    with col2:
        st.write("Distribusi Usia per Klaster")
        success_bar, img_bar, msg_bar = visualisasi.buat_bar_chart_usia()
        if success_bar:
            st.image(BytesIO(base64.b64decode(img_bar)))

    st.subheader("Filter Visualisasi")
    fitur_filter = st.selectbox("Pilih Fitur untuk Filter", df.columns)
    nilai_filter = st.selectbox("Pilih Nilai Filter", df[fitur_filter].unique())

    if st.button("Terapkan Filter"):
        success_filter, hasil_filter, msg_filter = visualisasi.filter_dan_update_grafik(fitur_filter, nilai_filter)
        if success_filter:
            st.image(BytesIO(base64.b64decode(hasil_filter['pie_chart'])))
            st.image(BytesIO(base64.b64decode(hasil_filter['bar_chart'])))
# Aplikasi utama
def main():
    if not st.session_state.get('logged_in'):
        show_login()
    else:
        selected_menu = main_menu()

        if selected_menu == "Dashboard":
            show_dashboard()
        elif selected_menu == "Manajemen Data":
            show_data_management()
        elif selected_menu == "Segmentasi Nasabah":
            show_segmentation()
        elif selected_menu == "Rekomendasi Produk":
            show_recommendation()
        elif selected_menu == "Manajemen Pengguna":
            show_user_management()
        elif selected_menu == "Visualisasi":
            show_visualization()

if __name__ == "__main__":
    main()