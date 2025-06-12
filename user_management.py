from enum import Enum
import hashlib
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRole(Enum):
    """Enum untuk role pengguna sesuai dokumen SRS"""
    ADMIN = "admin"
    MARKETING = "pemasaran"
    MANAGEMENT = "manajemen"

class UserStatus(Enum):
    """Enum untuk status pengguna"""
    PENDING = "pending"
    ACTIVE = "active"
    REJECTED = "rejected"
    SUSPENDED = "suspended"

class User:
    """Class untuk representasi pengguna"""
    def __init__(self, user_id: str, username: str, password: str, role: UserRole,
                 email: str = "", full_name: str = "", department: str = "",
                 created_at: datetime = None, status: UserStatus = UserStatus.PENDING):
        self.user_id = user_id
        self.username = username
        self.password_hash = self._hash_password(password)
        self.role = role
        self.email = email
        self.full_name = full_name
        self.department = department
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

    def to_dict(self) -> Dict:
        """Convert user object ke dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'department': self.department,
            'role': self.role.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejection_reason': self.rejection_reason
        }

class UserManagement:
    """Class untuk manajemen pengguna dengan 3 role sesuai SRS"""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.current_user: Optional[User] = None
        self._init_default_users()

    def _init_default_users(self):
        """Inisialisasi user default untuk masing-masing role"""
        default_users = [
            {
                'user_id': "admin_001",
                'username': "admin",
                'password': "admin123",
                'role': UserRole.ADMIN,
                'email': "admin@bank.com",
                'full_name': "Administrator Sistem",
                'status': UserStatus.ACTIVE
            },
            {
                'user_id': "mkt_001",
                'username': "pemasaran",
                'password': "mkt123",
                'role': UserRole.MARKETING,
                'email': "marketing@bank.com",
                'full_name': "Tim Pemasaran",
                'status': UserStatus.ACTIVE
            },
            {
                'user_id': "mgmt_001",
                'username': "manajemen",
                'password': "mgmt123",
                'role': UserRole.MANAGEMENT,
                'email': "management@bank.com",
                'full_name': "Manajemen Bank",
                'status': UserStatus.ACTIVE
            }
        ]

        for user_data in default_users:
            user = User(**user_data)
            self.users[user.username] = user

        logger.info("Default users created: admin, pemasaran, manajemen")

    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Login dengan validasi role"""
        try:
            if username not in self.users:
                return False, "Username tidak ditemukan", None

            user = self.users[username]

            if not user.verify_password(password):
                return False, "Password salah", None

            if user.status != UserStatus.ACTIVE:
                return False, f"Akun tidak aktif. Status: {user.status.value}", None

            self.current_user = user

            # Pesan login berbeda berdasarkan role
            if user.role == UserRole.ADMIN:
                msg = "Login admin berhasil - Akses penuh sistem"
            elif user.role == UserRole.MARKETING:
                msg = "Login tim pemasaran berhasil - Akses analisis dan rekomendasi"
            else:
                msg = "Login manajemen berhasil - Akses dashboard dan laporan"

            return True, msg, user.to_dict()

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False, f"Error saat login: {str(e)}", None

#     # Method lainnya tetap sama, tetapi perlu disesuaikan dengan 3 role
#     def logout(self) -> Tuple[bool, str]:
#         """Logout pengguna saat ini"""
#         if self.current_user is None:
#             return False, "Tidak ada pengguna yang sedang login"

#         self.current_user = None
#         logger.info("Pengguna berhasil logout")
#         return True, "Logout berhasil"
#     def register_user(self, username: str, password: str, role: UserRole,
#                       email: str = "", full_name: str = "", department: str = "") -> Tuple[bool, str]:

#         """Registrasi pengguna baru"""
#         if username in self.users:
#             return False, "Username sudah digunakan"
#         hashed_password = self._hash_password(password)
#         new_user = User(
#             user_id=f"user_{len(self.users) + 1}",
#             username=username,
#             password=hashed_password,
#             role=role,
#             email=email,
#             full_name=full_name,
#             department=department
#         )
#         self.users[username] = new_user
#         logger.info(f"User {username} registered successfully")
#         return True, "Registrasi berhasil"
#     def approve_user(self, username: str, approved_by: str) -> Tuple[bool, str]:
#         """Menyetujui pengguna yang telah terdaftar"""
#         if username not in self.users:
#             return False, "Pengguna tidak ditemukan"
#         user = self.users[username]
#         if user.status != UserStatus.PENDING:
#             return False, "Pengguna tidak dalam status pending"
#         user.status = UserStatus.ACTIVE
#         user.approved_by = approved_by
#         user.approved_at = datetime.now()
#         logger.info(f"User {username} approved by {approved_by}")
#         return True, f"Pengguna {username} berhasil disetujui"
#     def reject_user(self, username: str, reason: str) -> Tuple[bool, str]:
#         """Menolak pengguna yang telah terdaftar"""
#         if username not in self.users:
#             return False, "Pengguna tidak ditemukan"
#         user = self.users[username]
#         if user.status != UserStatus.PENDING:
#             return False, "Pengguna tidak dalam status pending"
#         user.status = UserStatus.REJECTED
#         user.rejection_reason = reason
#         logger.info(f"User {username} rejected: {reason}")
#         return True, f"Pengguna {username} berhasil ditolak: {reason}"
#     def suspend_user(self, username: str) -> Tuple[bool, str]:
#         """Menangguhkan pengguna"""
#         if username not in self.users:
#             return False, "Pengguna tidak ditemukan"
#         user = self.users[username]
#         if user.status != UserStatus.ACTIVE:
#             return False, "Pengguna tidak dalam status aktif"
#         user.status = UserStatus.SUSPENDED
#         logger.info(f"User {username} suspended")
#         return True, f"Pengguna {username} berhasil ditangguhkan"
#     def get_user_info(self, username: str) -> Tuple[bool, Optional[Dict], str]:
#         """Mengambil informasi pengguna berdasarkan username"""
#         if username not in self.users:
#             return False, None, "Pengguna tidak ditemukan"
#         user = self.users[username]
#         return True, user.to_dict(), "Informasi pengguna berhasil diambil"
#     def get_all_users(self) -> List[Dict]:
#         """Mengambil daftar semua pengguna"""
#         return [user.to_dict() for user in self.users.values()]
#     def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
#         """Mengganti password pengguna"""
#         if username not in self.users:
#             return False, "Pengguna tidak ditemukan"
#         user = self.users[username]
#         if not user.verify_password(old_password):
#             return False, "Password lama salah"
#         user.password_hash = user._hash_password(new_password)
#         logger.info(f"Password for user {username} changed successfully")
#         return True, "Password berhasil diganti"
#     def _hash_password(self, password: str) -> str:
#         """Hash password menggunakan SHA256"""
#         return hashlib.sha256(password.encode()).hexdigest()
#     def update_user_info(self, username: str, email: Optional[str] = None,
#                          full_name: Optional[str] = None, department: Optional[str] = None) -> Tuple[bool, str]:
#         """Memperbarui informasi pengguna"""
#         if username not in self.users:
#             return False, "Pengguna tidak ditemukan"
#         user = self.users[username]
#         if email is not None:
#             user.email = email
#         if full_name is not None:
#             user.full_name = full_name
#         if department is not None:
#             user.department = department
#         logger.info(f"User {username} info updated successfully")
#         return True, "Informasi pengguna berhasil diperbarui"
#     def get_user_info(self, username: str) -> Tuple[bool, Optional[Dict], str]:
#         """Mengambil informasi pengguna berdasarkan username"""
#         if username not in self.users:
#             return False, None, "Pengguna tidak ditemukan"
#         user = self.users[username]
#         return True, user.to_dict(), "Informasi pengguna berhasil diambil"
#     def get_current_user(self) -> Optional[Dict]:
#         """Mengambil informasi pengguna yang sedang login"""
#         if self.current_user is None:
#             return None
#         return self.current_user.to_dict()
#     def get_all_users(self) -> List[Dict]:
#         """Mengambil daftar semua pengguna"""
#         return [user.to_dict() for user in self.users.values()]
#         self.data = pd.concat([self.data, encoded_df], axis=1)
# #             else:#                 self.data = encoded_df #
# #             logger.info("Data berhasil ditransformasi")
# #             return True, "Data berhasil ditransformasi"
# #         except

#     #         return False, "Terjadi kesalahan saat transformasi data"
#     def export_users(self) -> pd.DataFrame:
#         """Ekspor daftar pengguna ke DataFrame"""
#         return pd.DataFrame([user.to_dict() for user in self.users.values()])
#     def export_users(self) -> pd.DataFrame:
#         """Ekspor daftar pengguna ke DataFrame"""
#         return pd.DataFrame([user.to_dict() for user in self.users.values()])
#     def export_users_to_csv(self, file_path: str) -> Tuple[bool, str]:
#         """Ekspor daftar pengguna ke file CSV"""
#         try:
#             df = self.export_users()
#             df.to_csv(file_path, index=False)
#             logger.info(f"Daftar pengguna berhasil diekspor ke {file_path}")
#             return True, f"Daftar pengguna berhasil diekspor ke {file_path}"
#         except Exception as e:
#             logger.error(f"Gagal mengekspor pengguna: {str(e)}")
#             return False, f"Gagal mengekspor pengguna: {str(e)}"
#     def export_users_to_excel(self, file_path: str) -> Tuple[bool, str]:
#         """Ekspor daftar pengguna ke file Excel"""
#         try:
#             df = self.export_users()
#             df.to_excel(file_path, index=False)
#             logger.info(f"Daftar pengguna berhasil diekspor ke {file_path}")
#             return True, f"Daftar pengguna berhasil diekspor ke {file_path}"
#         except Exception as e:
#             logger.error(f"Gagal mengekspor pengguna: {str(e)}")
#             return False, f"Gagal mengekspor pengguna: {str(e)}"
#     def export_users_to_json(self, file_path: str) -> Tuple[bool, str]:
#         """Ekspor daftar pengguna ke file JSON"""
#         try:
#             df = self.export_users()
#             df.to_json(file_path, orient='records', lines=True)
#             logger.info(f"Daftar pengguna berhasil diekspor ke {file_path}")
#             return True, f"Daftar pengguna berhasil diekspor ke {file_path}"
#         except Exception as e:
#             logger.error(f"Gagal mengekspor pengguna: {str(e)}")
#             return False, f"Gagal mengekspor pengguna: {str(e)}"
#             return False, None, f"Gagal menyimpan hasil: {str(e)}"
#             return False, None, f"Gagal menyimpan hasil: {str(e)}"
#             return False, None, f"Gagal menyimpan hasil: {str(e)}"
#             return False, None, f"Gagal menyimpan hasil: {str(e)}"
#             return False, None, f"Gagal menyimpan hasil: {str(e)}"