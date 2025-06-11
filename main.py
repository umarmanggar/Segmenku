import pandas as pd
import streamlit as st
from datetime import datetime
import logging

# Import modules
from user_management import UserManagement, Dashboard, UserStatus
from rekomendasi import SistemRekomendasi
from visualisasi import VisualisasiData

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainApplication:
    """Class utama untuk aplikasi sistem rekomendasi produk"""

    def __init__(self):
        # Initialize session state
        if 'user_mgmt' not in st.session_state:
            st.session_state.user_mgmt = UserManagement()
        if 'dashboard' not in st.session_state:
            st.session_state.dashboard = Dashboard(st.session_state.user_mgmt)
        if 'page' not in st.session_state:
            st.session_state.page = 'login'
        if 'show_register' not in st.session_state:
            st.session_state.show_register = False

    def run(self):
        """Menjalankan aplikasi utama"""
        st.set_page_config(
            page_title="Sistem Rekomendasi Produk Bank",
            page_icon="🏦",
            layout="wide"
        )

        # Cek status login
        current_user = st.session_state.user_mgmt.get_current_user_info()

        if current_user is None:
            self.show_auth_page()
        else:
            self.show_dashboard(current_user)

    def show_auth_page(self):
        """Halaman autentikasi (login/register)"""
        st.title("🏦 Sistem Rekomendasi Produk Bank")

        # Toggle antara login dan register
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Login", use_container_width=True,
                        type="primary" if not st.session_state.show_register else "secondary"):
                st.session_state.show_register = False
                st.rerun()

        with col2:
            if st.button("Daftar Akun Baru", use_container_width=True,
                        type="primary" if st.session_state.show_register else "secondary"):
                st.session_state.show_register = True
                st.rerun()

        st.divider()

        if st.session_state.show_register:
            self.show_register_form()
        else:
            self.show_login_form()

    def show_login_form(self):
        """Form login"""
        st.subheader("🔐 Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if username and password:
                    status, message, user_data = st.session_state.user_mgmt.login(username, password)

                    if status:
                        st.success(message)
                        st.session_state.page = 'dashboard'
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Mohon isi username dan password")

        # Info akun demo
        with st.expander("ℹ️ Info Akun Demo"):
            st.info("""
            **Akun Admin Default:**
            - Username: admin
            - Password: admin123

            **Untuk akun user:** Silakan daftar terlebih dahulu dan tunggu persetujuan admin.
            """)

    def show_register_form(self):
        """Form registrasi"""
        st.subheader("📝 Daftar Akun Baru")

        with st.form("register_form"):
            col1, col2 = st.columns(2)

            with col1:
                username = st.text_input("Username*")
                full_name = st.text_input("Nama Lengkap*")
                email = st.text_input("Email*")

            with col2:
                password = st.text_input("Password*", type="password")
                confirm_password = st.text_input("Konfirmasi Password*", type="password")
                phone = st.text_input("Nomor Telepon")

            st.caption("* Field wajib diisi")

            submit = st.form_submit_button("Daftar", use_container_width=True)

            if submit:
                # Validasi input
                if not all([username, full_name, email, password, confirm_password]):
                    st.error("Mohon isi semua field yang wajib")
                elif password != confirm_password:
                    st.error("Password dan konfirmasi password tidak sama")
                elif len(password) < 6:
                    st.error("Password minimal 6 karakter")
                else:
                    status, message = st.session_state.user_mgmt.register_user(
                        username=username,
                        password=password,
                        email=email,
                        full_name=full_name,
                        phone=phone
                    )

                    if status:
                        st.success(message)
                        st.info("Silakan login setelah akun Anda disetujui admin")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(message)

    def show_dashboard(self, current_user):
        """Dashboard utama berdasarkan role user"""
        # Header
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.title(f"Dashboard - {current_user['full_name']}")

        with col2:
            st.write(f"**Role:** {current_user['role'].title()}")

        with col3:
            if st.button("Logout", type="secondary"):
                st.session_state.user_mgmt.logout()
                st.session_state.page = 'login'
                st.rerun()

        st.divider()

        # Menu berdasarkan role
        if current_user['role'] == 'admin':
            self.show_admin_dashboard()
        else:
            self.show_user_dashboard()

    def show_admin_dashboard(self):
        """Dashboard untuk admin"""
        # Sidebar menu
        st.sidebar.title("Menu Admin")
        menu_options = [
            "📊 Overview",
            "👥 Kelola Pengguna",
            "✅ Persetujuan Pengguna",
            "🎯 Sistem Rekomendasi",
            "📈 Laporan"
        ]

        selected_menu = st.sidebar.selectbox("Pilih Menu:", menu_options)

        if selected_menu == "📊 Overview":
            self.show_admin_overview()
        elif selected_menu == "👥 Kelola Pengguna":
            self.show_user_management()
        elif selected_menu == "✅ Persetujuan Pengguna":
            self.show_user_approval()
        elif selected_menu == "🎯 Sistem Rekomendasi":
            self.show_recommendation_system()
        elif selected_menu == "📈 Laporan":
            self.show_reports()

    def show_admin_overview(self):
        """Overview dashboard admin"""
        st.header("📊 Overview Sistem")

        # Statistik pengguna
        users = st.session_state.user_mgmt.users
        total_users = len(users)
        active_users = len([u for u in users.values() if u.status == UserStatus.ACTIVE])
        pending_users = len([u for u in users.values() if u.status == UserStatus.PENDING])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Pengguna", total_users)
        with col2:
            st.metric("Pengguna Aktif", active_users)
        with col3:
            st.metric("Menunggu Persetujuan", pending_users)
        with col4:
            st.metric("Admin", len([u for u in users.values() if u.role.value == 'admin']))

        # Grafik status pengguna
        if total_users > 0:
            status_data = {}
            for user in users.values():
                status = user.status.value
                status_data[status] = status_data.get(status, 0) + 1

            st.subheader("Distribusi Status Pengguna")
            st.bar_chart(status_data)

    def show_user_approval(self):
        """Halaman persetujuan pengguna"""
        st.header("✅ Persetujuan Pengguna Baru")

        # Ambil daftar pending users
        status, df, message = st.session_state.user_mgmt.get_pending_users()

        if status and df is not None and not df.empty:
            st.success(message)

            # Tampilkan tabel pending users
            for idx, row in df.iterrows():
                with st.expander(f"👤 {row['full_name']} (@{row['username']})"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.write(f"**Email:** {row['email']}")
                        st.write(f"**Telepon:** {row['phone'] if row['phone'] else 'Tidak ada'}")
                        st.write(f"**Tanggal Daftar:** {row['created_at'][:19]}")

                    with col2:
                        col_approve, col_reject = st.columns(2)

                        with col_approve:
                            if st.button(f"✅ Setujui", key=f"approve_{row['username']}"):
                                approve_status, approve_msg = st.session_state.user_mgmt.approve_user(row['username'])
                                if approve_status:
                                    st.success(approve_msg)
                                    st.rerun()
                                else:
                                    st.error(approve_msg)

                        with col_reject:
                            if st.button(f"❌ Tolak", key=f"reject_{row['username']}"):
                                # Form untuk alasan penolakan
                                with st.form(f"reject_form_{row['username']}"):
                                    reason = st.text_area("Alasan penolakan:", key=f"reason_{row['username']}")
                                    if st.form_submit_button("Konfirmasi Penolakan"):
                                        reject_status, reject_msg = st.session_state.user_mgmt.reject_user(
                                            row['username'], reason
                                        )
                                        if reject_status:
                                            st.success(reject_msg)
                                            st.rerun()
                                        else:
                                            st.error(reject_msg)
        else:
            st.info("Tidak ada pengguna yang menunggu persetujuan")

    def show_user_management(self):
        """Halaman kelola pengguna"""
        st.header("👥 Kelola Pengguna")

        # Tab untuk berbagai fungsi
        tab1, tab2, tab3 = st.tabs(["📋 Daftar Pengguna", "➕ Tambah Pengguna", "⚙️ Edit Pengguna"])

        with tab1:
            self.show_user_list()

        with tab2:
            self.show_add_user_form()

        with tab3:
            self.show_edit_user_form()

    def show_user_list(self):
        """Tampilkan daftar semua pengguna"""
        status, df, message = st.session_state.user_mgmt.get_daftar_pengguna()

        if status and df is not None and not df.empty:
            st.success(message)

            # Filter berdasarkan status
            status_filter = st.selectbox(
                "Filter berdasarkan status:",
                ["Semua", "active", "pending", "rejected", "suspended"]
            )

            if status_filter != "Semua":
                df_filtered = df[df['status'] == status_filter]
            else:
                df_filtered = df

            # Tampilkan tabel
            st.dataframe(
                df_filtered[['username', 'full_name', 'email', 'role', 'status', 'created_at']],
                use_container_width=True
            )
        else:
            st.error(message if message else "Gagal mengambil daftar pengguna")

    def show_add_user_form(self):
        """Form tambah pengguna langsung oleh admin"""
        st.subheader("➕ Tambah Pengguna Baru (Langsung Aktif)")

        with st.form("add_user_admin"):
            col1, col2 = st.columns(2)

            with col1:
                username = st.text_input("Username")
                full_name = st.text_input("Nama Lengkap")
                email = st.text_input("Email")

            with col2:
                password = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["user", "admin"])
                phone = st.text_input("Nomor Telepon")

            if st.form_submit_button("Tambah Pengguna"):
                if username and password and email and full_name:
                    status, message = st.session_state.user_mgmt.tambah_pengguna_langsung(
                        username=username,
                        password=password,
                        role=role,
                        email=email,
                        full_name=full_name
                    )

                    if status:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Mohon isi semua field yang wajib")

    def show_edit_user_form(self):
        """Form edit pengguna"""
        st.subheader("⚙️ Edit Pengguna")

        # Pilih pengguna untuk diedit
        users = st.session_state.user_mgmt.users
        user_options = [u.username for u in users.values() if u.username != 'admin']

        if user_options:
            selected_user = st.selectbox("Pilih pengguna:", user_options)

            if selected_user:
                user = users[selected_user]

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Username:** {user.username}")
                    st.write
