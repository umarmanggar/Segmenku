import pandas as pd
import hashlib
import logging
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRole(Enum):
    """Enum untuk role pengguna"""
    ADMIN = "admin"
    USER = "user"

class UserStatus(Enum):
    """Enum untuk status pengguna"""
    PENDING = "pending"      # Menunggu persetujuan admin
    ACTIVE = "active"        # Aktif dan bisa login
    REJECTED = "rejected"    # Ditolak admin
    SUSPENDED = "suspended"  # Disuspend admin

class User:
    """Class untuk representasi pengguna"""

    def __init__(self, user_id: str, username: str, password: str, role: UserRole,
                 email: str = "", full_name: str = "", phone: str = "",
                 created_at: datetime = None, status: UserStatus = UserStatus.PENDING):
        self.user_id = user_id
        self.username = username
        self.password_hash = self._hash_password(password)
        self.role = role
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.created_at = created_at or datetime.now()
        self.status = status
        self.approved_by = None
        self.approved_at = None
        self.rejection_reason = None

    def _hash_password(self, password: str) -> str:
        """Hash password menggunakan SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verifikasi password"""
        return self.password_hash == self._hash_password(password)

    def approve(self, admin_username: str):
        """Setujui pengguna"""
        self.status = UserStatus.ACTIVE
        self.approved_by = admin_username
        self.approved_at = datetime.now()

    def reject(self, admin_username: str, reason: str = ""):
        """Tolak pengguna"""
        self.status = UserStatus.REJECTED
        self.approved_by = admin_username
        self.approved_at = datetime.now()
        self.rejection_reason = reason

    def to_dict(self) -> Dict:
        """Convert user object ke dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejection_reason': self.rejection_reason
        }

class UserManagement:
    """Class untuk manajemen pengguna dengan sistem persetujuan"""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.current_user: Optional[User] = None
        self._init_default_admin()

    def _init_default_admin(self):
        """Inisialisasi admin default"""
        admin = User(
            user_id="admin_001",
            username="admin",
            password="admin123",
            role=UserRole.ADMIN,
            email="admin@system.com",
            full_name="System Administrator",
            status=UserStatus.ACTIVE  # Admin langsung aktif
        )
        self.users[admin.username] = admin
        logger.info("Admin default berhasil dibuat")

    def register_user(self, username: str, password: str, email: str,
                     full_name: str, phone: str = "") -> Tuple[bool, str]:
        """
        Registrasi pengguna baru (akan masuk ke pending list)

        Args:
            username: Username yang diinginkan
            password: Password
            email: Email pengguna
            full_name: Nama lengkap
            phone: Nomor telepon (opsional)

        Returns:
            Tuple[bool, str]: Status dan pesan
        """
        try:
            # Validasi input
            if not username or not password or not email or not full_name:
                return False, "Semua field wajib diisi (username, password, email, nama lengkap)"

            # Cek apakah username sudah ada
            if username in self.users:
                return False, f"Username '{username}' sudah digunakan"

            # Cek format email sederhana
            if "@" not in email or "." not in email:
                return False, "Format email tidak valid"

            # Cek apakah email sudah digunakan
            for user in self.users.values():
                if user.email == email:
                    return False, f"Email '{email}' sudah terdaftar"

            # Buat user baru dengan status PENDING
            user_id = f"user_{len(self.users):03d}"
            new_user = User(
                user_id=user_id,
                username=username,
                password=password,
                role=UserRole.USER,  # Default role adalah USER
                email=email,
                full_name=full_name,
                phone=phone,
                status=UserStatus.PENDING
            )

            # Tambahkan ke sistem
            self.users[username] = new_user

            logger.info(f"Registrasi baru: {username} ({full_name}) - Status: PENDING")
            return True, f"Registrasi berhasil! Akun Anda menunggu persetujuan admin. Anda akan dihubungi melalui email: {email}"

        except Exception as e:
            error_msg = f"Gagal melakukan registrasi: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Login pengguna (hanya yang statusnya ACTIVE)

        Args:
            username: Username pengguna
            password: Password pengguna

        Returns:
            Tuple[bool, str, Optional[Dict]]: Status, pesan, data user
        """
        try:
            # Cek apakah user ada
            if username not in self.users:
                return False, "Username tidak ditemukan", None

            user = self.users[username]

            # Verifikasi password
            if not user.verify_password(password):
                return False, "Password salah", None

            # Cek status user
            if user.status == UserStatus.PENDING:
                return False, "Akun Anda masih menunggu persetujuan admin", None
            elif user.status == UserStatus.REJECTED:
                reason = f" Alasan: {user.rejection_reason}" if user.rejection_reason else ""
                return False, f"Akun Anda ditolak oleh admin.{reason}", None
            elif user.status == UserStatus.SUSPENDED:
                return False, "Akun Anda telah disuspend", None
            elif user.status != UserStatus.ACTIVE:
                return False, "Status akun tidak valid", None

            # Set current user
            self.current_user = user

            # Log berdasarkan role
            if user.role == UserRole.ADMIN:
                logger.info(f"Admin login: {username}")
                return True, "Login admin berhasil - Redirect ke dashboard admin", user.to_dict()
            else:
                logger.info(f"User login: {username}")
                return True, "Login user berhasil - Dashboard terbuka dengan akses terbatas", user.to_dict()

        except Exception as e:
            error_msg = f"Error saat login: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, None

    def logout(self) -> Tuple[bool, str]:
        """Logout pengguna"""
        if self.current_user:
            logger.info(f"User logout: {self.current_user.username}")
            self.current_user = None
            return True, "Logout berhasil"
        return False, "Tidak ada user yang login"

    def is_admin(self) -> bool:
        """Cek apakah current user adalah admin"""
        return (self.current_user is not None and
                self.current_user.role == UserRole.ADMIN and
                self.current_user.status == UserStatus.ACTIVE)

    def get_pending_users(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Mendapatkan daftar pengguna yang menunggu persetujuan

        Returns:
            Tuple[bool, Optional[pd.DataFrame], str]: Status, data, pesan
        """
        try:
            # Cek apakah user yang login adalah admin
            if not self.is_admin():
                return False, None, "Akses ditolak: Hanya admin yang dapat melihat pending users"

            # Filter user dengan status PENDING
            pending_users = []
            for user in self.users.values():
                if user.status == UserStatus.PENDING:
                    user_dict = user.to_dict()
                    pending_users.append(user_dict)

            if not pending_users:
                return True, pd.DataFrame(), "Tidak ada pengguna yang menunggu persetujuan"

            df = pd.DataFrame(pending_users)
            # Pilih kolom yang relevan untuk review
            columns = ['username', 'full_name', 'email', 'phone', 'created_at']
            df_display = df[columns]

            return True, df_display, f"Ditemukan {len(pending_users)} pengguna menunggu persetujuan"

        except Exception as e:
            error_msg = f"Gagal mengambil daftar pending users: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg

    def approve_user(self, username: str) -> Tuple[bool, str]:
        """
        Setujui pengguna yang pending

        Args:
            username: Username yang akan disetujui

        Returns:
            Tuple[bool, str]: Status dan pesan
        """
        try:
            # Cek apakah user yang login adalah admin
            if not self.is_admin():
                return False, "Akses ditolak: Hanya admin yang dapat menyetujui pengguna"

            # Cek apakah user ada
            if username not in self.users:
                return False, f"Pengguna '{username}' tidak ditemukan"

            user = self.users[username]

            # Cek apakah user masih pending
            if user.status != UserStatus.PENDING:
                return False, f"Pengguna '{username}' tidak dalam status pending (Status: {user.status.value})"

            # Setujui user
            user.approve(self.current_user.username)

            logger.info(f"Admin {self.current_user.username} menyetujui pengguna: {username}")
            return True, f"Pengguna '{username}' ({user.full_name}) berhasil disetujui dan dapat login"

        except Exception as e:
            error_msg = f"Gagal menyetujui pengguna: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def reject_user(self, username: str, reason: str = "") -> Tuple[bool, str]:
        """
        Tolak pengguna yang pending

        Args:
            username: Username yang akan ditolak
            reason: Alasan penolakan

        Returns:
            Tuple[bool, str]: Status dan pesan
        """
        try:
            # Cek apakah user yang login adalah admin
            if not self.is_admin():
                return False, "Akses ditolak: Hanya admin yang dapat menolak pengguna"

            # Cek apakah user ada
            if username not in self.users:
                return False, f"Pengguna '{username}' tidak ditemukan"

            user = self.users[username]

            # Cek apakah user masih pending
            if user.status != UserStatus.PENDING:
                return False, f"Pengguna '{username}' tidak dalam status pending (Status: {user.status.value})"

            # Tolak user
            user.reject(self.current_user.username, reason)

            logger.info(f"Admin {self.current_user.username} menolak pengguna: {username}. Alasan: {reason}")
            return True, f"Pengguna '{username}' ({user.full_name}) berhasil ditolak"

        except Exception as e:
            error_msg = f"Gagal menolak pengguna: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def tambah_pengguna_langsung(self, username: str, password: str, role: str,
                                email: str = "", full_name: str = "") -> Tuple[bool, str]:
        """
        Tambah pengguna langsung oleh admin (langsung aktif, tidak perlu approval)

        Args:
            username: Username baru
            password: Password baru
            role: Role pengguna (admin/user)
            email: Email pengguna
            full_name: Nama lengkap

        Returns:
            Tuple[bool, str]: Status dan pesan
        """
        try:
            # Cek apakah user yang login adalah admin
            if not self.is_admin():
                return False, "Akses ditolak: Hanya admin yang dapat menambah pengguna"

            # Cek apakah username sudah ada
            if username in self.users:
                return False, f"Username '{username}' sudah digunakan"

            # Validasi role
            try:
                user_role = UserRole(role.lower())
            except ValueError:
                return False, "Role tidak valid. Gunakan 'admin' atau 'user'"

            # Buat user baru dengan status ACTIVE
            user_id = f"user_{len(self.users):03d}"
            new_user = User(
                user_id=user_id,
                username=username,
                password=password,
                role=user_role,
                email=email,
                full_name=full_name,
                status=UserStatus.ACTIVE  # Langsung aktif
            )
            new_user.approved_by = self.current_user.username
            new_user.approved_at = datetime.now()

            # Tambahkan ke sistem
            self.users[username] = new_user

            logger.info(f"Admin {self.current_user.username} menambah pengguna langsung: {username}")
            return True, f"Pengguna '{username}' berhasil ditambahkan dan langsung aktif"

        except Exception as e:
            error_msg = f"Gagal menambah pengguna: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def edit_hak_akses(self, username: str, role_baru: str) -> Tuple[bool, str]:
        """
        Edit hak akses pengguna (MU-01-04)

        Args:
            username: Username yang akan diubah
            role_baru: Role baru (admin/user)

        Returns:
            Tuple[bool, str]: Status dan pesan
        """
        try:
            # Cek apakah user yang login adalah admin
            if not self.is_admin():
                return False, "Akses ditolak: Hanya admin yang dapat mengubah hak akses"

            # Cek apakah user ada
            if username not in self.users:
                return False, f"Pengguna '{username}' tidak ditemukan"

            # Validasi role baru
            try:
                new_role = UserRole(role_baru.lower())
            except ValueError:
                return False, "Role tidak valid. Gunakan 'admin' atau 'user'"

            # Cek apakah tidak mengubah role diri sendiri
            if username == self.current_user.username:
                return False, "Tidak dapat mengubah role diri sendiri"

            # Update role
            old_role = self.users[username].role.value
            self.users[username].role = new_role

            logger.info(f"Admin {self.current_user.username} mengubah role {username}: {old_role} -> {role_baru}")
            return True, f"Role pengguna '{username}' berhasil diubah dari '{old_role}' ke '{role_baru}'"

        except Exception as e:
            error_msg = f"Gagal mengubah hak akses: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def hapus_pengguna(self, username: str, konfirmasi: bool = False) -> Tuple[bool, str]:
        """
        Hapus pengguna (MU-01-05)

        Args:
            username: Username yang akan dihapus
            konfirmasi: Konfirmasi penghapusan

        Returns:
            Tuple[bool, str]: Status dan pesan
        """
        try:
            # Cek apakah user yang login adalah admin
            if not self.is_admin():
                return False, "Akses ditolak: Hanya admin yang dapat menghapus pengguna"

            # Cek apakah user ada
            if username not in self.users:
                return False, f"Pengguna '{username}' tidak ditemukan"

            # Cek apakah tidak menghapus diri sendiri
            if username == self.current_user.username:
                return False, "Tidak dapat menghapus akun diri sendiri"

            # Jika belum konfirmasi, minta konfirmasi
            if not konfirmasi:
                return False, f"Konfirmasi diperlukan untuk menghapus pengguna '{username}'"

            # Hapus pengguna
            deleted_user = self.users.pop(username)

            logger.info(f"Admin {self.current_user.username} menghapus pengguna: {username}")
            return True, f"Pengguna '{username}' berhasil dihapus"

        except Exception as e:
            error_msg = f"Gagal menghapus pengguna: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def get_daftar_pengguna(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Mendapatkan daftar semua pengguna

        Returns:
            Tuple[bool, Optional[pd.DataFrame], str]: Status, data, pesan
        """
        try:
            # Cek apakah user yang login adalah admin
            if not self.is_admin():
                return False, None, "Akses ditolak: Hanya admin yang dapat melihat daftar pengguna"

            if not self.users:
                return True, pd.DataFrame(), "Tidak ada pengguna"

            # Convert ke DataFrame
            users_data = []
            for user in self.users.values():
                user_dict = user.to_dict()
                users_data.append(user_dict)

            df = pd.DataFrame(users_data)
            return True, df, f"Ditemukan {len(users_data)} pengguna"

        except Exception as e:
            error_msg = f"Gagal mengambil daftar pengguna: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg

    def get_current_user_info(self) -> Optional[Dict]:
        """Mendapatkan informasi user yang sedang login"""
        if self.current_user:
            return self.current_user.to_dict()
        return None

# Class untuk simulasi dashboard
class Dashboard:
    """Class untuk dashboard sistem"""

    def __init__(self, user_management: UserManagement):
        self.user_mgmt = user_management

    def tampilkan_menu_admin(self) -> List[str]:
        """Menu untuk admin"""
        return [
            "1. Lihat Daftar Pengguna",
            "2. Tambah Pengguna",
            "3. Edit Hak Akses",
            "4. Hapus Pengguna",
            "5. Kelola Sistem Rekomendasi",
            "6. Logout"
        ]

    def tampilkan_menu_user(self) -> List[str]:
        """Menu untuk user biasa (akses terbatas)"""
        return [
            "1. Lihat Profil",
            "2. Lihat Rekomendasi Produk",
            "3. Logout"
        ]

    def get_menu_berdasarkan_role(self) -> List[str]:
        """Mendapatkan menu berdasarkan role user"""
        if not self.user_mgmt.current_user:
            return ["Silakan login terlebih dahulu"]

        if self.user_mgmt.is_admin():
            return self.tampilkan_menu_admin()
        else:
            return self.tampilkan_menu_user()

# Contoh penggunaan
if __name__ == "__main__":
    # Inisialisasi sistem
    user_mgmt = UserManagement()
    dashboard = Dashboard(user_mgmt)

    print("=== DEMO SISTEM USER MANAGEMENT ===\n")

    # MU-01-01: Login sebagai admin
    print("1. Login sebagai admin:")
    status, pesan, user_data = user_mgmt.login("admin", "admin123")
    print(f"Status: {status}")
    print(f"Pesan: {pesan}")
    if user_data:
        print(f"Role: {user_data['role']}")
    print()

    # MU-01-03: Tambah pengguna
    print("2. Tambah pengguna baru:")
    status, pesan = user_mgmt.tambah_pengguna("john_doe", "password123", "user", "john@email.com")
    print(f"Status: {status}")
    print(f"Pesan: {pesan}")
    print()

    # Tambah user lain
    user_mgmt.tambah_pengguna("jane_smith", "password456", "user", "jane@email.com")

    # Lihat daftar pengguna
    print("3. Daftar pengguna:")
    status, df, pesan = user_mgmt.get_daftar_pengguna()
    if status and df is not None:
        print(df[['username', 'role', 'email', 'is_active']])
    print()

    # MU-01-04: Edit hak akses
    print("4. Edit hak akses john_doe menjadi admin:")
    status, pesan = user_mgmt.edit_hak_akses("john_doe", "admin")
    print(f"Status: {status}")
    print(f"Pesan: {pesan}")
    print()

    # MU-01-05: Hapus pengguna (tanpa konfirmasi)
    print("5. Hapus pengguna jane_smith (tanpa konfirmasi):")
    status, pesan = user_mgmt.hapus_pengguna("jane_smith")
    print(f"Status: {status}")
    print(f"Pesan: {pesan}")
    print()

    # MU-01-05: Hapus pengguna (dengan konfirmasi)
    print("6. Hapus pengguna jane_smith (dengan konfirmasi):")
    status, pesan = user_mgmt.hapus_pengguna("jane_smith", konfirmasi=True)
    print