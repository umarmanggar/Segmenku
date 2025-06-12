import pandas as pd
import streamlit as st
from datetime import datetime
import logging
from enum import Enum, auto

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
        self.email = kwargs.get('email', ' ')
        self.phone = kwargs.get('phone', ' ')
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

        # Hide Streamlit menu and footer
        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        current_user = st.session_state.user_mgmt.get_current_user_info()

        if current_user is None:
            self.show_auth_page()
        else:
            self.show_dashboard(current_user)

    def show_auth_page(self):
        st.title("🔐 Login ke Sistem")

        if st.session_state.show_register:
            self.show_register_page()
        else:
            self.show_login_page()

    def show_login_page(self):
        st.subheader("Masuk ke akun Anda")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            success, message, user_info = st.session_state.user_mgmt.login(username, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

        if st.button("Belum punya akun? Daftar di sini"):
            st.session_state.show_register = True
            st.rerun()

    def show_register_page(self):
        st.subheader("📋 Formulir Pendaftaran")

        username = st.text_input("Username Baru")
        password = st.text_input("Password", type="password")
        full_name = st.text_input("Nama Lengkap")
        email = st.text_input("Email")
        phone = st.text_input("No. Telepon")

        if st.button("Daftar"):
            if username in st.session_state.user_mgmt.users:
                st.error("Username sudah digunakan")
            else:
                new_user = User(username=username, password=password, full_name=full_name, email=email, phone=phone)
                st.session_state.user_mgmt.users[username] = new_user
                st.success("Pendaftaran berhasil! Menunggu persetujuan admin.")
                st.session_state.show_register = False
                st.rerun()

        if st.button("Sudah punya akun? Login di sini"):
            st.session_state.show_register = False
            st.rerun()

    def show_dashboard(self, user_info):
        st.sidebar.title(f"Selamat datang, {user_info['full_name']} 👋")
        menu = st.sidebar.radio("Navigasi", ["Beranda", "Profil", "Rekomendasi", "Edit User", "Logout"])

        if menu == "Beranda":
            self.show_home()
        elif menu == "Profil":
            self.show_profile(user_info)
        elif menu == "Rekomendasi":
            self.show_recommendation_system()
        elif menu == "Edit User":
            if user_info['role'] == 'admin':
                self.show_edit_user_form()
            else:
                st.warning("Hanya admin yang dapat mengedit user.")
        elif menu == "Logout":
            st.session_state.user_mgmt.logout()
            st.rerun()

    def show_home(self):
        st.title("🏠 Beranda")
        st.write("Selamat datang di Sistem Rekomendasi Produk Bank. Silakan pilih menu di samping untuk melanjutkan.")

    def show_profile(self, user_info):
        st.title("👤 Profil Pengguna")

        st.markdown("### Informasi Pengguna")
        st.write(f"**Nama Lengkap:** {user_info['full_name']}")
        st.write(f"**Username:** {user_info['username']}")
        st.write(f"**Email:** {user_info['email']}")
        st.write(f"**Nomor Telepon:** {user_info['phone']}")
        st.write(f"**Peran:** {user_info['role'].capitalize()}")
        st.write(f"**Status Akun:** {user_info['status'].capitalize()}")
        st.write(f"**Tanggal Dibuat:** {user_info['created_at']}")

    def show_edit_user_form(self):
        st.subheader("⚙️ Edit Pengguna")

        users = st.session_state.user_mgmt.users
        user_options = [u.username for u in users.values() if u.username != 'admin']

        if not user_options:
            st.warning("Tidak ada pengguna yang bisa diedit")
            return

        selected_user = st.selectbox("Pilih pengguna:", user_options)
        user = users[selected_user]

        with st.form(f"edit_form_{user.username}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Username:** {user.username}")
                new_full_name = st.text_input("Nama Lengkap", value=user.full_name)
                new_email = st.text_input("Email", value=user.email)

            with col2:
                new_role = st.selectbox(
                    "Role",
                    [r.value for r in UserRole],
                    index=0 if user.role == UserRole.USER else 1
                )
                new_status = st.selectbox(
                    "Status",
                    [s.value for s in UserStatus],
                    index=[s.value for s in UserStatus].index(user.status.value)
                )
                new_phone = st.text_input("Nomor Telepon", value=user.phone or "")

            if st.form_submit_button("Simpan Perubahan"):
                user.full_name = new_full_name
                user.email = new_email
                user.role = UserRole(new_role)
                user.status = UserStatus(new_status)
                user.phone = new_phone

                st.success("Perubahan berhasil disimpan!")
                st.rerun()

    def show_recommendation_system(self):
        st.header("🎯 Sistem Rekomendasi")
        st.write("Fitur sistem rekomendasi untuk admin")

        with st.expander("📊 Statistik Rekomendasi"):
            st.write("Grafik dan statistik rekomendasi akan ditampilkan di sini")

        with st.expander("⚙️ Konfigurasi Rekomendasi"):
            st.write("Form konfigurasi aturan rekomendasi")


if __name__ == "__main__":
    app = MainApplication()
    app.run()