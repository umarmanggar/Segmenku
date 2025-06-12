# from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score
# import pandas as pd
# import numpy as np
# import logging
# from typing import Tuple, Optional, List, Dict, Any

# # Konfigurasi logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class SegmentasiNasabah:
#     def __init__(self, data: pd.DataFrame, jumlah_klaster: int = 3):
#         self.data = data
#         self.jumlah_klaster = jumlah_klaster
#         self.model = KMeans(n_clusters=jumlah_klaster, random_state=42)
#         self.label_klaster = None
#         self.fitur_numerik = ['age', 'balance', 'duration', 'campaign']
#         self.metrik_evaluasi = {}

#     def praproses_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
#         try:
#             # Pastikan fitur yang diperlukan ada
#             fitur_yang_tidak_ada = [f for f in self.fitur_numerik if f not in self.data.columns]
#             if fitur_yang_tidak_ada:
#                 pesan = f"Fitur berikut tidak ditemukan: {fitur_yang_tidak_ada}"
#                 logger.error(pesan)
#                 return False, None, pesan

#             # Bersihkan data
#             self.data = self.data.dropna(subset=self.fitur_numerik)

#             # Logging
#             logger.info("Praproses data selesai")
#             return True, self.data[self.fitur_numerik], "Data siap untuk proses segmentasi"

#         except Exception as e:
#             pesan_error = f"Gagal dalam praproses data: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def jalankan_segmentasi(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
#         try:
#             # Praproses data
#             sukses, data_proses, pesan = self.praproses_data()
#             if not sukses:
#                 return False, None, pesan

#             # Jalankan K-Means
#             self.label_klaster = self.model.fit_predict(data_proses)
#             self.data['Klaster'] = self.label_klaster

#             # Hitung metrik evaluasi
#             self._hitung_metrik_evaluasi(data_proses)

#             logger.info("Proses clustering dijalankan")
#             return True, self.data, "Segmentasi nasabah berhasil dilakukan"

#         except Exception as e:
#             pesan_error = f"Gagal menjalankan segmentasi: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def _hitung_metrik_evaluasi(self, data_proses: pd.DataFrame) -> None:
#         try:
#             # Silhouette Score
#             if len(np.unique(self.label_klaster)) > 1:
#                 self.metrik_evaluasi['silhouette'] = silhouette_score(data_proses, self.label_klaster)

#             # Ukuran setiap klaster
#             self.metrik_evaluasi['ukuran_klaster'] = pd.Series(self.label_klaster).value_counts().to_dict()

#             # Rata-rata fitur per klaster
#             data_dengan_klaster = data_proses.copy()
#             data_dengan_klaster['Klaster'] = self.label_klaster
#             self.metrik_evaluasi['rata_rata_fitur'] = data_dengan_klaster.groupby('Klaster').mean().to_dict()

#         except Exception as e:
#             logger.warning(f"Gagal menghitung beberapa metrik evaluasi: {str(e)}")

#     def tampilkan_hasil_klaster(self) -> Tuple[bool, Optional[Dict[str, Any]], str]:
#         if self.label_klaster is None:
#             return False, None, "Segmentasi belum dijalankan. Jalankan segmentasi terlebih dahulu."

#         try:
#             hasil = {
#                 'data': self.data.to_dict(orient='records'),
#                 'metrik': self.metrik_evaluasi,
#                 'pusat_klaster': self.model.cluster_centers_.tolist(),
#                 'jumlah_klaster': self.jumlah_klaster
#             }

#             logger.info("Tampil tabel cluster")
#             return True, hasil, "Hasil segmentasi berhasil diambil"

#         except Exception as e:
#             pesan_error = f"Gagal menyiapkan hasil klaster: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def lihat_detail_klaster(self, id_klaster: int) -> Tuple[bool, Optional[pd.DataFrame], str]:
#         if self.label_klaster is None:
#             return False, None, "Segmentasi belum dijalankan. Jalankan segmentasi terlebih dahulu."

#         if id_klaster not in set(self.label_klaster):
#             return False, None, f"Klaster {id_klaster} tidak ditemukan"

#         try:
#             data_klaster = self.data[self.data['Klaster'] == id_klaster]
#             logger.info(f"Detail anggota segmen {id_klaster} muncul")
#             return True, data_klaster, f"Detail klaster {id_klaster}"

#         except Exception as e:
#             pesan_error = f"Gagal mengambil detail klaster: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def simpan_hasil(self, path_output: str) -> Tuple[bool, str]:
#         if self.label_klaster is None:
#             return False, "Segmentasi belum dijalankan. Jalankan segmentasi terlebih dahulu."

#         try:
#             self.data.to_csv(path_output, index=False)
#             logger.info("Notifikasi 'Berhasil disimpan'")
#             return True, f"Hasil segmentasi berhasil disimpan di {path_output}"

#         except Exception as e:
#             pesan_error = f"Gagal menyimpan hasil: {str(e)}"
#             logger.error(pesan_error)
#             return False, pesan_error

#     def segmentasi_ulang(self, jumlah_klaster_baru: int) -> Tuple[bool, Optional[pd.DataFrame], str]:
#         try:
#             self.jumlah_klaster = jumlah_klaster_baru
#             self.model = KMeans(n_clusters=self.jumlah_klaster, random_state=42)

#             return self.jalankan_segmentasi()

#         except Exception as e:
#             pesan_error = f"Gagal melakukan segmentasi ulang: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

# File: clustering.py
# Deskripsi: Kelas ini mengimplementasikan algoritma clustering K-Means untuk segmentasi nasabah.
# Relevan dengan SRS Bab 3.1 (REQ-1) dan Test Case SN-01 hingga SN-05.

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
import logging
from typing import Tuple, Optional, Dict, Any

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SegmentasiNasabah:
    """
    Kelas untuk menjalankan segmentasi nasabah menggunakan K-Means.
    """
    def __init__(self, data: pd.DataFrame, jumlah_klaster: int = 3):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data input harus berupa pandas DataFrame.")
        self.original_data = data.copy() # Simpan data asli untuk penggabungan
        self.data_processed = data.select_dtypes(include=np.number) # Proses hanya kolom numerik
        self.jumlah_klaster = jumlah_klaster
        # SRS REQ-1.2: Konfigurasi algoritma clustering
        self.model = KMeans(n_clusters=jumlah_klaster, random_state=42, n_init=10)
        self.label_klaster = None
        self.metrik_evaluasi = {}

    # Test Case: SN-01-01 (Jalankan segmentasi)
    # SRS: REQ-1
    def jalankan_segmentasi(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Menjalankan algoritma K-Means pada data yang telah diproses.
        """
        try:
            # Jalankan K-Means
            self.label_klaster = self.model.fit_predict(self.data_processed)
            self.original_data['Klaster'] = self.label_klaster

            # Hitung metrik evaluasi
            self._hitung_metrik_evaluasi(self.data_processed)

            # Pesan sesuai log pada Test Case SN-01-01
            logger.info("Proses clustering dijalankan")
            return True, self.original_data, "Segmentasi nasabah berhasil dilakukan"

        except Exception as e:
            pesan_error = f"Gagal menjalankan segmentasi: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def _hitung_metrik_evaluasi(self, data_proses: pd.DataFrame) -> None:
        """Menghitung metrik evaluasi seperti Silhouette Score."""
        try:
            if len(np.unique(self.label_klaster)) > 1:
                self.metrik_evaluasi['silhouette'] = silhouette_score(data_proses, self.label_klaster)
            self.metrik_evaluasi['ukuran_klaster'] = pd.Series(self.label_klaster).value_counts().to_dict()

            data_dengan_klaster = data_proses.copy()
            data_dengan_klaster['Klaster'] = self.label_klaster
            self.metrik_evaluasi['rata_rata_fitur'] = data_dengan_klaster.groupby('Klaster').mean().to_dict()
        except Exception as e:
            logger.warning(f"Gagal menghitung beberapa metrik evaluasi: {str(e)}")

    # Test Case: SN-01-02 (Tampilkan hasil cluster)
    # SRS: REQ-2.1
    def tampilkan_hasil_klaster(self) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Menyiapkan hasil clustering untuk ditampilkan.
        """
        if self.label_klaster is None:
            return False, None, "Segmentasi belum dijalankan."

        try:
            hasil = {
                'data': self.original_data.to_dict(orient='records'),
                'metrik': self.metrik_evaluasi,
                'pusat_klaster': self.model.cluster_centers_.tolist(),
            }
            # Pesan sesuai log pada Test Case SN-01-02
            logger.info("Tampil tabel cluster")
            return True, hasil, "Hasil segmentasi berhasil diambil"
        except Exception as e:
            pesan_error = f"Gagal menyiapkan hasil klaster: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    # Test Case: SN-01-03 (Lihat detail anggota cluster)
    # SRS: REQ-2.2
    def lihat_detail_klaster(self, id_klaster: int) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Menampilkan data anggota dari klaster tertentu.
        """
        if self.label_klaster is None:
            return False, None, "Segmentasi belum dijalankan."

        if id_klaster not in set(self.label_klaster):
            return False, None, f"Klaster {id_klaster} tidak ditemukan"

        try:
            data_klaster = self.original_data[self.original_data['Klaster'] == id_klaster]
            # Pesan sesuai log pada Test Case SN-01-03
            logger.info(f"Detail anggota segmen {id_klaster} muncul")
            return True, data_klaster, f"Detail untuk klaster {id_klaster}"
        except Exception as e:
            pesan_error = f"Gagal mengambil detail klaster: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    # Test Case: SN-01-04 (Simpan hasil cluster)
    # SRS: REQ-1.3
    def simpan_hasil(self, path_output: str) -> Tuple[bool, str]:
        """
        Menyimpan data dengan label klaster ke file CSV.
        """
        if self.label_klaster is None:
            return False, "Segmentasi belum dijalankan."

        try:
            self.original_data.to_csv(path_output, index=False)
            # Pesan sesuai log pada Test Case SN-01-04
            logger.info("Notifikasi 'Berhasil disimpan'")
            return True, f"Hasil segmentasi berhasil disimpan di {path_output}"
        except Exception as e:
            pesan_error = f"Gagal menyimpan hasil: {str(e)}"
            logger.error(pesan_error)
            return False, pesan_error

    # Test Case: SN-01-05 (Uji ulang segmentasi)
    # SRS: REQ-1.2
    def segmentasi_ulang(self, jumlah_klaster_baru: int) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Menjalankan ulang proses segmentasi dengan jumlah klaster yang baru.
        """
        try:
            self.jumlah_klaster = jumlah_klaster_baru
            self.model = KMeans(n_clusters=self.jumlah_klaster, random_state=42, n_init=10)
            # Pesan sesuai log pada Test Case SN-01-05
            logger.info("Proses baru dijalankan")
            return self.jalankan_segmentasi()
        except Exception as e:
            pesan_error = f"Gagal melakukan segmentasi ulang: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error