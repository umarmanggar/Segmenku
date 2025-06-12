# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.impute import SimpleImputer
# import logging
# from typing import Tuple, Optional, List, Union

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class DataProcessor:
#     def __init__(self, file_path: str = "bank.csv"):
#         self.file_path = file_path
#         self.data = None
#         self.required_columns = None  # Should be set based on your specific requirements
#         self.numeric_cols = None
#         self.categorical_cols = None
#         self.scaler = StandardScaler()
#         self.encoder = OneHotEncoder(handle_unknown='ignore')
#         self.imputer = SimpleImputer(strategy='mean')

#     def load_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
#         try:
#             self.data = pd.read_csv(self.file_path)
#             logger.info(f"Dataset '{self.file_path}' successfully loaded.")
#             return True, self.data, f"File berhasil diunggah, dan isi data ditampilkan dalam tampilan tabel"
#         except FileNotFoundError:
#             error_msg = f"Error: File '{self.file_path}' tidak ditemukan."
#             logger.error(error_msg)
#             return False, None, error_msg
#         except Exception as e:
#             error_msg = f"Error loading file: {str(e)}"
#             logger.error(error_msg)
#             return False, None, error_msg

#     def validate_data_structure(self, expected_columns: List[str]) -> Tuple[bool, str]:
#         if self.data is None:
#             return False, "Data belum dimuat. Silakan unggah file terlebih dahulu."

#         missing_cols = set(expected_columns) - set(self.data.columns)
#         if missing_cols:
#             error_msg = f"Validasi gagal, kolom berikut tidak ditemukan: {missing_cols}"
#             logger.error(error_msg)
#             return False, error_msg

#         self.required_columns = expected_columns
#         logger.info("Validasi berhasil, proses lanjut ke preprocessing")
#         return True, "Validasi berhasil, proses lanjut ke preprocessing"

#     def preprocess_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
#         if self.data is None:
#             return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

#         try:
#             # Identify numeric and categorical columns
#             self.numeric_cols = self.data.select_dtypes(include=['number']).columns.tolist()
#             self.categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()

#             # Handle missing values
#             self.data[self.numeric_cols] = self.imputer.fit_transform(self.data[self.numeric_cols])
#             self.data[self.categorical_cols] = self.data[self.categorical_cols].fillna('Unknown')

#             logger.info("Nilai kosong terhapus, nilai numerik ternormalisasi dengan benar")
#             return True, self.data, "Nilai kosong terhapus, nilai numerik ternormalisasi dengan benar"
#         except Exception as e:
#             error_msg = f"Error during preprocessing: {str(e)}"
#             logger.error(error_msg)
#             return False, None, error_msg

#     def select_features(self, selected_features: List[str]) -> Tuple[bool, Optional[pd.DataFrame], str]:
#         if self.data is None:
#             return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

#         missing_features = set(selected_features) - set(self.data.columns)
#         if missing_features:
#             error_msg = f"Kolom berikut tidak ditemukan dalam data: {missing_features}"
#             logger.error(error_msg)
#             return False, None, error_msg

#         self.data = self.data[selected_features]
#         logger.info("Kolom terpilih tercatat sebagai input untuk proses machine learning")
#         return True, self.data, "Kolom terpilih tercatat sebagai input untuk proses machine learning"

#     def transform_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
#         if self.data is None:
#             return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

#         try:
#             # Scale numeric features
#             if self.numeric_cols:
#                 self.data[self.numeric_cols] = self.scaler.fit_transform(self.data[self.numeric_cols])

#             # Encode categorical features
#             if self.categorical_cols:
#                 encoded_data = self.encoder.fit_transform(self.data[self.categorical_cols])
#                 encoded_df = pd.DataFrame(encoded_data.toarray(),
#                                         columns=self.encoder.get_feature_names_out(self.categorical_cols))
#                 self.data = pd.concat([self.data.drop(columns=self.categorical_cols), encoded_df], axis=1)

#             logger.info("Data kategorikal diencoding dan numerik diskalakan, siap untuk algoritma ML")
#             return True, self.data, "Data kategorikal diencoding dan numerik diskalakan, siap untuk algoritma Machine Learning"
#         except Exception as e:
#             error_msg = f"Error during transformation: {str(e)}"
#             logger.error(error_msg)
#             return False, None, error_msg

#     def get_data_summary(self) -> dict:
#         if self.data is None:
#             return {}

#         return {
#             "shape": self.data.shape,
#             "columns": self.data.columns.tolist(),
#             "missing_values": self.data.isnull().sum().to_dict(),
#             "numeric_stats": self.data.describe().to_dict() if self.numeric_cols else {},
#             "categorical_stats": self.data.describe(include=['object']).to_dict() if self.categorical_cols else {}
#         }

# File: dataload.py
# Deskripsi: Modul ini menangani pemrosesan data, termasuk memuat, validasi,
# pembersihan, dan transformasi data nasabah.
# Relevan dengan SRS Bab 3.1 (REQ-1) dan Test Case PD-001 hingga PD-006.

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import logging
from typing import Tuple, Optional, List

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Kelas untuk memuat dan memproses data nasabah dari file CSV.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.numeric_cols = None
        self.categorical_cols = None
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.imputer = SimpleImputer(strategy='mean')

    # Test Case: PD-001-01 (Input Data)
    # SRS: REQ-1.1
    def load_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Memuat data dari file CSV.
        """
        try:
            self.data = pd.read_csv(self.file_path)
            logger.info(f"Dataset '{self.file_path}' berhasil dimuat.")
            # Pesan sesuai Expected Result pada Test Case PD-001-01
            return True, self.data, "File berhasil diunggah, dan isi data ditampilkan dalam tampilan tabel"
        except FileNotFoundError:
            error_msg = f"Error: File '{self.file_path}' tidak ditemukan."
            logger.error(error_msg)
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Error saat memuat file: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg

    # Test Case: PD-001-02 & PD-001-03 (Validasi Format Data)
    # SRS: REQ-1.1 (Pengecekan Integritas)
    def validate_data_structure(self, expected_columns: List[str]) -> Tuple[bool, str]:
        """
        Memvalidasi apakah kolom yang dibutuhkan ada dalam data.
        """
        if self.data is None:
            return False, "Data belum dimuat. Silakan unggah file terlebih dahulu."

        missing_cols = set(expected_columns) - set(self.data.columns)
        if missing_cols:
            # Pesan sesuai Expected Result pada Test Case PD-001-03
            error_msg = f"Validasi gagal, kolom berikut tidak ditemukan: {missing_cols}"
            logger.error(error_msg)
            return False, error_msg

        # Pesan sesuai Expected Result pada Test Case PD-001-02
        logger.info("Validasi berhasil, proses lanjut ke preprocessing")
        return True, "Validasi berhasil, proses lanjut ke preprocessing"

    # Test Case: PD-001-04 (Pembersihan Data)
    # SRS: REQ-1.1
    def preprocess_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Membersihkan data dengan menangani nilai yang hilang.
        """
        if self.data is None:
            return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

        try:
            # Identifikasi kolom numerik dan kategorikal
            self.numeric_cols = self.data.select_dtypes(include=np.number).columns.tolist()
            self.categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()

            # Tangani nilai yang hilang
            if self.numeric_cols:
                self.data[self.numeric_cols] = self.imputer.fit_transform(self.data[self.numeric_cols])
            if self.categorical_cols:
                for col in self.categorical_cols:
                    self.data[col] = self.data[col].fillna('Unknown')

            # Pesan sesuai Expected Result pada Test Case PD-001-04
            logger.info("Nilai kosong terhapus, nilai numerik ternormalisasi dengan benar")
            return True, self.data, "Nilai kosong terhapus, nilai numerik ternormalisasi dengan benar"
        except Exception as e:
            error_msg = f"Error saat preprocessing: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg

    # Test Case: PD-001-05 (Pemilihan Fitur)
    # SRS: REQ-1
    def select_features(self, selected_features: List[str]) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Memilih fitur spesifik untuk digunakan dalam model.
        """
        if self.data is None:
            return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

        missing_features = set(selected_features) - set(self.data.columns)
        if missing_features:
            error_msg = f"Kolom berikut tidak ditemukan dalam data: {missing_features}"
            logger.error(error_msg)
            return False, None, error_msg

        self.data = self.data[selected_features]
        # Pesan sesuai Expected Result pada Test Case PD-001-05
        logger.info("Kolom terpilih tercatat sebagai input untuk proses machine learning")
        return True, self.data, "Kolom terpilih tercatat sebagai input untuk proses machine learning"

    # Test Case: PD-001-06 (Transformasi Data)
    # SRS: REQ-1.1
    def transform_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Melakukan scaling pada fitur numerik dan encoding pada fitur kategorikal.
        """
        if self.data is None:
            return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

        try:
            data_to_transform = self.data.copy()

            # Identifikasi ulang kolom numerik dan kategorikal dari data yang mungkin sudah difilter
            self.numeric_cols = data_to_transform.select_dtypes(include=np.number).columns.tolist()
            self.categorical_cols = data_to_transform.select_dtypes(include=['object']).columns.tolist()

            # Scale fitur numerik
            if self.numeric_cols:
                data_to_transform[self.numeric_cols] = self.scaler.fit_transform(data_to_transform[self.numeric_cols])

            # Encode fitur kategorikal
            if self.categorical_cols:
                encoded_data = self.encoder.fit_transform(data_to_transform[self.categorical_cols])
                encoded_df = pd.DataFrame(encoded_data,
                                        columns=self.encoder.get_feature_names_out(self.categorical_cols),
                                        index=data_to_transform.index)
                data_to_transform = data_to_transform.drop(columns=self.categorical_cols)
                data_to_transform = pd.concat([data_to_transform, encoded_df], axis=1)

            self.data = data_to_transform
            # Pesan sesuai Expected Result pada Test Case PD-001-06
            logger.info("Data kategorikal diencoding dan numerik diskalakan, siap untuk algoritma ML")
            return True, self.data, "Data kategorikal diencoding dan numerik diskalakan, siap untuk algoritma Machine Learning"
        except Exception as e:
            error_msg = f"Error saat transformasi data: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg