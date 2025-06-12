import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from typing import Tuple, Optional, List

class DataProcessor:
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
        self.audit_log = []

    def log_step(self, message: str):
        """Menambahkan pesan ke audit log."""
        self.audit_log.append(f"- {message}")

    def load_data(self, uploaded_file) -> Tuple[bool, str]:
        """Memuat data dari file yang diunggah dan melakukan validasi awal."""
        try:
            # PD-001-05: Validasi Ukuran File (< 10 MB)
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > 10:
                self.log_step("PERINGATAN: Ukuran file > 10MB. Performa mungkin menurun.")

            # PD-001-01: Baca file CSV
            self.raw_data = pd.read_csv(uploaded_file)
            self.processed_data = self.raw_data.copy()

            # PD-001-03: Validasi CSV Kosong
            if self.processed_data.empty:
                self.log_step("ERROR: File CSV yang diunggah tidak memiliki data.")
                return False, "Data kosong"

            self.log_step(f"File '{uploaded_file.name}' berhasil diunggah ({file_size_mb:.2f} MB).")
            return True, "File berhasil diunggah."

        except Exception as e:
            # PD-001-02: Validasi Format (ditangani secara implisit)
            self.log_step(f"ERROR: Gagal memuat file. Kemungkinan format tidak valid. Detail: {e}")
            return False, "Format tidak valid atau file rusak."

    def clean_data(self, missing_value_method: str, outlier_method: str) -> Tuple[bool, str]:
        """Membersihkan data berdasarkan metode yang dipilih pengguna."""
        if self.processed_data is None:
            return False, "Data belum dimuat."
        try:
            # PD-002-01: Penanganan Nilai Kosong
            if missing_value_method == 'Hapus Baris':
                self.processed_data.dropna(inplace=True)
                self.log_step("Membersihkan nilai kosong dengan menghapus baris.")
            elif missing_value_method == 'Isi dengan Mean/Modus':
                for col in self.processed_data.columns:
                    if self.processed_data[col].dtype == 'object':
                        # Isi dengan modus untuk kategorikal
                        self.processed_data[col].fillna(self.processed_data[col].mode()[0], inplace=True)
                    else:
                        # Isi dengan mean untuk numerik
                        self.processed_data[col].fillna(self.processed_data[col].mean(), inplace=True)
                self.log_step("Membersihkan nilai kosong dengan Mean/Modus.")

            # PD-002-02: Penanganan Outlier
            if outlier_method == 'Hapus Outlier (IQR)':
                numeric_cols = self.processed_data.select_dtypes(include=np.number).columns
                for col in numeric_cols:
                    Q1 = self.processed_data[col].quantile(0.25)
                    Q3 = self.processed_data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    # Simpan data yang bukan outlier
                    self.processed_data = self.processed_data[
                        (self.processed_data[col] >= lower_bound) & (self.processed_data[col] <= upper_bound)
                    ]
                self.log_step("Menghapus outlier menggunakan metode IQR.")

            return True, "Data berhasil dibersihkan."
        except Exception as e:
            self.log_step(f"ERROR saat cleaning: {e}")
            return False, f"Gagal membersihkan data: {e}"

    def select_features(self, selected_features: List[str]) -> Tuple[bool, str]:
        """Memilih fitur sesuai input pengguna."""
        # PD-003: Seluruh fungsionalitas
        if not selected_features:
            return False, "Pilih minimal 1 fitur"

        try:
            self.processed_data = self.processed_data[selected_features]
            self.log_step(f"Memilih {len(selected_features)} fitur: {', '.join(selected_features)}.")
            return True, "Fitur berhasil dipilih."
        except KeyError:
            return False, "Satu atau lebih fitur yang dipilih tidak valid."

    def transform_data(self, scaler_method: str) -> Tuple[bool, str]:
        """Melakukan transformasi data (scaling & encoding)."""
        # PD-004
        if self.processed_data is None:
            return False, "Tidak ada data untuk ditransformasi."

        try:
            # Pisahkan kolom numerik dan kategorikal
            numeric_cols = self.processed_data.select_dtypes(include=np.number).columns.tolist()
            categorical_cols = self.processed_data.select_dtypes(include='object').columns.tolist()

            # PD-004-03 & PD-002-03: Scaling
            if scaler_method == 'StandardScaler (Z-score)':
                scaler = StandardScaler()
                self.log_step("Menerapkan StandardScaler (Z-score).")
            elif scaler_method == 'MinMaxScaler':
                scaler = MinMaxScaler()
                self.log_step("Menerapkan MinMaxScaler.")

            if numeric_cols:
                self.processed_data[numeric_cols] = scaler.fit_transform(self.processed_data[numeric_cols])

            # PD-004-01: Encoding (One-Hot)
            if categorical_cols:
                self.processed_data = pd.get_dummies(self.processed_data, columns=categorical_cols, drop_first=True)
                self.log_step("Menerapkan One-Hot Encoding pada fitur kategorikal.")

            return True, "Data berhasil ditransformasi dan siap untuk segmentasi."
        except Exception as e:
            self.log_step(f"ERROR saat transformasi: {e}")
            return False, f"Transformasi gagal, pastikan tidak ada kolom kosong. Detail: {e}"