from enum import Enum
import hashlib
import logging
from typing import Dict, Optional, Tuple, Any, List
from datetime import datetime
import pandas as pd

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SRS 2.3: Mendefinisikan kelas pengguna
class UserRole(Enum):
    ADMIN = "admin"
    MARKETING = "marketing"
    MANAGEMENT = "management"

class UserStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"

class User:
    """Kelas untuk representasi objek pengguna."""
    def __init__(self, username: str, password: str, role: UserRole, full_name: str, email: str, status: UserStatus = UserStatus.ACTIVE):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.role = role
        self.full_name = full_name
        self.email = email
        self.status = status
        self.created_at = datetime.now()

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat()
        }

class UserManagement:
    """
    Kelas untuk mengelola semua operasi pengguna (login, tambah, edit, hapus).
    """
    def __init__(self):
        self.users: Dict[str, User] = {}
        self._add_default_users()

    def _add_default_users(self):
        if not self.users:
            self.add_user("admin", "admin123", UserRole.ADMIN, "Admin Sistem", "admin@bank.com")
            self.add_user("marketing", "marketing123", UserRole.MARKETING, "Tim Pemasaran", "pemasaran@bank.com")
            self.add_user("management", "management123", UserRole.MANAGEMENT, "Manajemen Bank", "manajemen@bank.com")
            logger.info("Pengguna default (admin, marketing, management) telah dibuat.")

    # Test Case: MU_01-03 (Tambah pengguna)
    def add_user(self, username: str, password: str, role: UserRole, full_name: str, email: str) -> Tuple[bool, str]:
        if not username or not password or not full_name or not email:
            return False, "Semua field harus diisi."
        if username in self.users:
            return False, f"Username '{username}' sudah ada."
        self.users[username] = User(username, password, role, full_name, email)
        logger.info(f"Pengguna baru '{username}' ditambahkan.")
        return True, f"Pengguna '{username}' berhasil ditambahkan."

    # FUNGSI BARU: Untuk mengedit pengguna yang ada
    # Test Case: MU_01-04 (Edit hak akses)
    def edit_user(self, username: str, new_data: Dict[str, Any]) -> Tuple[bool, str]:
        if username not in self.users:
            return False, "Pengguna tidak ditemukan."

        user = self.users[username]
        try:
            if 'full_name' in new_data:
                user.full_name = new_data['full_name']
            if 'email' in new_data:
                user.email = new_data['email']
            if 'role' in new_data:
                user.role = UserRole(new_data['role'])
            if 'status' in new_data:
                user.status = UserStatus(new_data['status'])
            # Opsi untuk mengubah password
            if 'password' in new_data and new_data['password']:
                user.password_hash = user._hash_password(new_data['password'])

            logger.info(f"Data pengguna '{username}' berhasil diubah.")
            return True, f"Pengguna '{username}' berhasil diperbarui."
        except Exception as e:
            logger.error(f"Error saat mengedit pengguna {username}: {e}")
            return False, f"Terjadi kesalahan: {e}"

    # FUNGSI BARU: Untuk menghapus pengguna
    # Test Case: MU_01-05 (Hapus pengguna)
    def delete_user(self, username: str, current_admin: str) -> Tuple[bool, str]:
        if username not in self.users:
            return False, "Pengguna tidak ditemukan."
        if username == current_admin:
            return False, "Admin tidak dapat menghapus akunnya sendiri."

        del self.users[username]
        logger.info(f"Pengguna '{username}' telah dihapus oleh '{current_admin}'.")
        return True, f"Pengguna '{username}' berhasil dihapus."

    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        user = self.users.get(username)
        if not user or not user.verify_password(password):
            return False, "Username atau password salah.", None
        if user.status != UserStatus.ACTIVE:
            return False, f"Akun Anda tidak aktif (status: {user.status.value}).", None
        logger.info(f"Pengguna '{username}' berhasil login.")
        return True, "Login berhasil!", user.to_dict()

    def get_user(self, username: str) -> Optional[User]:
        """Mendapatkan objek User berdasarkan username."""
        return self.users.get(username)

    def get_all_usernames(self) -> List[str]:
        """Mendapatkan daftar semua username."""
        return list(self.users.keys())

    def get_user_list_df(self) -> pd.DataFrame:
        """Mengembalikan daftar pengguna sebagai DataFrame pandas untuk ditampilkan di UI."""
        user_data = [user.to_dict() for user in self.users.values()]
        return pd.DataFrame(user_data, columns=['username', 'full_name', 'email', 'role', 'status', 'created_at'])