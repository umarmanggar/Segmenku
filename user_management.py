# from enum import Enum
# import hashlib
# import logging
# from typing import Dict, List, Optional, Tuple, Any
# from datetime import datetime
# import pandas as pd

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class UserRole(Enum):
#     """Enum untuk role pengguna sesuai dokumen SRS"""
#     ADMIN = "admin"
#     MARKETING = "marketing"  # Changed from "pemasaran"
#     MANAGEMENT = "management" # Changed from "manajemen"

# class UserStatus(Enum):
#     """Enum untuk status pengguna"""
#     PENDING = "pending"
#     ACTIVE = "active"
#     REJECTED = "rejected"
#     SUSPENDED = "suspended"

# class User:
#     """Class untuk representasi pengguna"""
#     def __init__(self, user_id: str, username: str, password: str, role: UserRole,
#                  email: str = "", full_name: str = "", department: str = "",
#                  created_at: datetime = None, status: UserStatus = UserStatus.PENDING):
#         self.user_id = user_id
#         self.username = username
#         self.password_hash = self._hash_password(password)
#         self.role = role
#         self.email = email
#         self.full_name = full_name
#         self.department = department
#         self.created_at = created_at or datetime.now()
#         self.status = status
#         self.approved_by = None
#         self.approved_at = None
#         self.rejection_reason = None

#     def _hash_password(self, password: str) -> str:
#         """Hash password menggunakan SHA256"""
#         return hashlib.sha256(password.encode()).hexdigest()

#     def verify_password(self, password: str) -> bool:
#         """Verifikasi password"""
#         return self.password_hash == self._hash_password(password)

#     def to_dict(self) -> Dict:
#         """Convert user object ke dictionary"""
#         return {
#             'user_id': self.user_id,
#             'username': self.username,
#             'full_name': self.full_name,
#             'email': self.email,
#             'department': self.department,
#             'role': self.role.value,
#             'status': self.status.value,
#             'created_at': self.created_at.isoformat(),
#             'approved_by': self.approved_by,
#             'approved_at': self.approved_at.isoformat() if self.approved_at else None,
#             'rejection_reason': self.rejection_reason
#         }

# class UserManagement:
#     """Class untuk manajemen pengguna dengan 3 role sesuai SRS"""

#     def __init__(self):
#         self.users: Dict[str, User] = {}
#         self.current_user: Optional[User] = None
#         self._init_default_users()

#     def _init_default_users(self):
#         """Inisialisasi user default untuk masing-masing role"""
#         default_users = [
#             {
#                 'user_id': "admin_001",
#                 'username': "admin",
#                 'password': "admin123",
#                 'role': UserRole.ADMIN,
#                 'email': "admin@bank.com",
#                 'full_name': "Administrator Sistem",
#                 'status': UserStatus.ACTIVE
#             },
#             {
#                 'user_id': "mkt_001",
#                 'username': "pemasaran", # Keep "pemasaran" for username, but the role enum value should align
#                 'password': "mkt123",
#                 'role': UserRole.MARKETING,
#                 'email': "marketing@bank.com",
#                 'full_name': "Tim Pemasaran",
#                 'status': UserStatus.ACTIVE
#             },
#             {
#                 'user_id': "mgmt_001",
#                 'username': "manajemen", # Keep "manajemen" for username, but the role enum value should align
#                 'password': "mgmt123",
#                 'role': UserRole.MANAGEMENT,
#                 'email': "management@bank.com",
#                 'full_name': "Manajemen Bank",
#                 'status': UserStatus.ACTIVE
#             }
#         ]

#         for user_data in default_users:
#             user = User(**user_data)
#             self.users[user.username] = user

#         logger.info("Default users created: admin, pemasaran, manajemen")

#     def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
#         """Login dengan validasi role"""
#         try:
#             if username not in self.users:
#                 return False, "Username tidak ditemukan", None

#             user = self.users[username]

#             if not user.verify_password(password):
#                 return False, "Password salah", None

#             if user.status != UserStatus.ACTIVE:
#                 return False, f"Akun tidak aktif. Status: {user.status.value}", None

#             self.current_user = user

#             # Pesan login berbeda berdasarkan role
#             if user.role == UserRole.ADMIN:
#                 msg = "Login admin berhasil - Akses penuh sistem"
#             elif user.role == UserRole.MARKETING:
#                 msg = "Login tim pemasaran berhasil - Akses analisis dan rekomendasi"
#             else:
#                 msg = "Login manajemen berhasil - Akses dashboard dan laporan"

#             return True, msg, user.to_dict()

#         except Exception as e:
#             logger.error(f"Login error: {str(e)}")
#             return False, f"Error saat login: {str(e)}", None

#     def get_daftar_pengguna(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
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
#                     'Dibuat': user.created_at.isoformat()
#                 })
#             df = pd.DataFrame(users_data)
#             return True, df, "Data pengguna berhasil dimuat"
#         except Exception as e:
#             return False, None, f"Error: {str(e)}"

# File: user_management.py
# Deskripsi: Modul untuk manajemen pengguna, termasuk login, peran, dan status.
# Relevan dengan SRS Bab 2.3 (Kelas Pengguna) dan Test Case MU-01 hingga MU-05.

from enum import Enum
import hashlib
import logging
from typing import Dict, Optional, Tuple, Any
from datetime import datetime
import pandas as pd

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SRS 2.3: Mendefinisikan kelas pengguna
class UserRole(Enum):
    """Enum untuk peran pengguna sesuai dokumen SRS."""
    ADMIN = "admin"
    MARKETING = "marketing"
    MANAGEMENT = "management"

class UserStatus(Enum):
    """Enum untuk status pengguna."""
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
        """Hash password untuk keamanan."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verifikasi password yang diinput dengan hash yang tersimpan."""
        return self.password_hash == self._hash_password(password)

    def to_dict(self) -> Dict[str, Any]:
        """Mengubah objek User menjadi dictionary."""
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
    Kelas untuk mengelola semua operasi pengguna (login, registrasi, dll.).
    """
    def __init__(self):
        self.users: Dict[str, User] = {}
        self._add_default_users()

    # SRS 2.3: Inisialisasi pengguna default untuk setiap peran
    def _add_default_users(self):
        """Menambahkan pengguna default untuk pengujian dan demo."""
        self.add_user("admin", "admin123", UserRole.ADMIN, "Admin Sistem", "admin@bank.com")
        self.add_user("marketing", "marketing123", UserRole.MARKETING, "Tim Pemasaran", "pemasaran@bank.com")
        self.add_user("management", "management123", UserRole.MANAGEMENT, "Manajemen Bank", "manajemen@bank.com")
        logger.info("Pengguna default (admin, marketing, management) telah dibuat.")

    # Test Case: MU_01-03 (Tambah pengguna)
    def add_user(self, username: str, password: str, role: UserRole, full_name: str, email: str) -> Tuple[bool, str]:
        """Menambahkan pengguna baru ke sistem."""
        if username in self.users:
            return False, f"Username '{username}' sudah ada."
        self.users[username] = User(username, password, role, full_name, email)
        return True, f"Pengguna '{username}' berhasil ditambahkan."

    # Test Case: MU_01-01 & MU_01-02 (Login)
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Memvalidasi kredensial pengguna dan mengelola sesi login.
        """
        user = self.users.get(username)
        if not user:
            return False, "Username atau password salah.", None

        if not user.verify_password(password):
            return False, "Username atau password salah.", None

        if user.status != UserStatus.ACTIVE:
            return False, f"Akun Anda tidak aktif (status: {user.status.value}).", None

        logger.info(f"Pengguna '{username}' berhasil login dengan peran '{user.role.value}'.")
        return True, "Login berhasil!", user.to_dict()

    # Test Case: MU_01-04 (Edit hak akses) & MU_01-05 (Hapus pengguna)
    def get_user_list_df(self) -> pd.DataFrame:
        """Mengembalikan daftar pengguna sebagai DataFrame pandas."""
        user_data = [user.to_dict() for user in self.users.values()]
        # Hapus password_hash untuk keamanan
        for user in user_data:
            user.pop('password_hash', None)
        return pd.DataFrame(user_data)