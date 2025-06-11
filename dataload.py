import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import logging
from typing import Tuple, Optional, List, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, file_path: str = "bank.csv"):
        self.file_path = file_path
        self.data = None
        self.required_columns = None  # Should be set based on your specific requirements
        self.numeric_cols = None
        self.categorical_cols = None
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.imputer = SimpleImputer(strategy='mean')

    def load_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        try:
            self.data = pd.read_csv(self.file_path)
            logger.info(f"Dataset '{self.file_path}' successfully loaded.")
            return True, self.data, f"File berhasil diunggah, dan isi data ditampilkan dalam tampilan tabel"
        except FileNotFoundError:
            error_msg = f"Error: File '{self.file_path}' tidak ditemukan."
            logger.error(error_msg)
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Error loading file: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg

    def validate_data_structure(self, expected_columns: List[str]) -> Tuple[bool, str]:
        if self.data is None:
            return False, "Data belum dimuat. Silakan unggah file terlebih dahulu."

        missing_cols = set(expected_columns) - set(self.data.columns)
        if missing_cols:
            error_msg = f"Validasi gagal, kolom berikut tidak ditemukan: {missing_cols}"
            logger.error(error_msg)
            return False, error_msg

        self.required_columns = expected_columns
        logger.info("Validasi berhasil, proses lanjut ke preprocessing")
        return True, "Validasi berhasil, proses lanjut ke preprocessing"

    def preprocess_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        if self.data is None:
            return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

        try:
            # Identify numeric and categorical columns
            self.numeric_cols = self.data.select_dtypes(include=['number']).columns.tolist()
            self.categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()

            # Handle missing values
            self.data[self.numeric_cols] = self.imputer.fit_transform(self.data[self.numeric_cols])
            self.data[self.categorical_cols] = self.data[self.categorical_cols].fillna('Unknown')

            logger.info("Nilai kosong terhapus, nilai numerik ternormalisasi dengan benar")
            return True, self.data, "Nilai kosong terhapus, nilai numerik ternormalisasi dengan benar"
        except Exception as e:
            error_msg = f"Error during preprocessing: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg

    def select_features(self, selected_features: List[str]) -> Tuple[bool, Optional[pd.DataFrame], str]:
        if self.data is None:
            return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

        missing_features = set(selected_features) - set(self.data.columns)
        if missing_features:
            error_msg = f"Kolom berikut tidak ditemukan dalam data: {missing_features}"
            logger.error(error_msg)
            return False, None, error_msg

        self.data = self.data[selected_features]
        logger.info("Kolom terpilih tercatat sebagai input untuk proses machine learning")
        return True, self.data, "Kolom terpilih tercatat sebagai input untuk proses machine learning"

    def transform_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        if self.data is None:
            return False, None, "Data belum dimuat. Silakan unggah file terlebih dahulu."

        try:
            # Scale numeric features
            if self.numeric_cols:
                self.data[self.numeric_cols] = self.scaler.fit_transform(self.data[self.numeric_cols])

            # Encode categorical features
            if self.categorical_cols:
                encoded_data = self.encoder.fit_transform(self.data[self.categorical_cols])
                encoded_df = pd.DataFrame(encoded_data.toarray(),
                                        columns=self.encoder.get_feature_names_out(self.categorical_cols))
                self.data = pd.concat([self.data.drop(columns=self.categorical_cols), encoded_df], axis=1)

            logger.info("Data kategorikal diencoding dan numerik diskalakan, siap untuk algoritma ML")
            return True, self.data, "Data kategorikal diencoding dan numerik diskalakan, siap untuk algoritma Machine Learning"
        except Exception as e:
            error_msg = f"Error during transformation: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg

    def get_data_summary(self) -> dict:
        if self.data is None:
            return {}

        return {
            "shape": self.data.shape,
            "columns": self.data.columns.tolist(),
            "missing_values": self.data.isnull().sum().to_dict(),
            "numeric_stats": self.data.describe().to_dict() if self.numeric_cols else {},
            "categorical_stats": self.data.describe(include=['object']).to_dict() if self.categorical_cols else {}
        }
