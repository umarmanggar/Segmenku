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
        # Initialize session state
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

    # [Implementasi method lainnya tetap sama...]
        def show_auth_page(self):
        st.title("🔐 Login ke Sistem")

        if st.session_state.show_register:
            self.show_register_form()
        else:
            self.show_login_form()

        if st.button("Belum punya akun? Daftar di sini"):
            st.session_state.show_register = True

    def show_login_form(self):
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            success, msg, user_info = st.session_state.user_mgmt.login(username, password)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    def show_register_form(self):
        st.subheader("Daftar Pengguna Baru")

        username = st.text_input("Username (baru)")
        password = st.text_input("Password", type="password")
        full_name = st.text_input("Nama Lengkap")
        email = st.text_input("Email")
        phone = st.text_input("No. Telepon")

        if st.button("Daftar"):
            if username in st.session_state.user_mgmt.users:
                st.warning("Username sudah terdaftar.")
            else:
                st.session_state.user_mgmt.users[username] = User(
                    username=username,
                    password=password,
                    full_name=full_name,
                    email=email,
                    phone=phone
                )
                st.success("Pendaftaran berhasil! Silakan login.")
                st.session_state.show_register = False
    def show_dashboard(self, user_info):
        st.title("🏦 Dashboard Sistem Rekomendasi Produk Bank")

        st.sidebar.header("Menu")
        menu_options = ["Beranda", "Profil", "Kelola Pengguna", "Sistem Rekomendasi"]
        if user_info['role'] == UserRole.ADMIN.value:
            menu_options.append("Edit Pengguna")

        selected_menu = st.sidebar.selectbox("Pilih Menu:", menu_options)

        if selected_menu == "Beranda":
            self.show_home()
        elif selected_menu == "Profil":
            self.show_profile(user_info)
        elif selected_menu == "Kelola Pengguna":
            self.show_manage_users()
        elif selected_menu == "Sistem Rekomendasi":
            self.show_recommendation_system()
        elif selected_menu == "Edit Pengguna" and user_info['role'] == UserRole.ADMIN.value:
            self.show_edit_user_form()

    def show_edit_user_form(self):
        """Form edit pengguna yang lengkap"""
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
                # Update user data
                user.full_name = new_full_name
                user.email = new_email
                user.role = UserRole(new_role)
                user.status = UserStatus(new_status)
                user.phone = new_phone

                st.success("Perubahan berhasil disimpan!")
                st.rerun()

    def show_recommendation_system(self):
        """Implementasi sistem rekomendasi untuk admin"""
        st.header("🎯 Sistem Rekomendasi")
        st.write("Fitur sistem rekomendasi untuk admin")

        # Placeholder - bisa diisi dengan implementasi nyata
        with st.expander("📊 Statistik Rekomendasi"):
            st.write("Grafik dan statistik rekomendasi akan ditampilkan di sini")

        with st.expander("⚙️ Konfigurasi Rekomendasi"):
            st.write("Form konfigurasi aturan rekomendasi")

if __name__ == "__main__":
    app = MainApplication()
    app.run()