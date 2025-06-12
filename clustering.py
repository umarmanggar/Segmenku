import pandas as pd
import numpy as np
import logging
from typing import Tuple, Optional, List, Dict, Any
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SegmentasiNasabah:
    def __init__(self, data: pd.DataFrame, jumlah_klaster: int = 3):
        # --- PERUBAHAN DIMULAI DI SINI ---
        if jumlah_klaster <= 0:
            pesan_error = "Jumlah klaster harus lebih besar dari 0."
            logger.error(pesan_error)
            raise ValueError(pesan_error)
        # --- PERUBAHAN SELESAI ---

        self.data = data
        self.jumlah_klaster = jumlah_klaster
        self.model = KMeans(n_clusters=jumlah_klaster, random_state=42)
        self.label_klaster = None
        self.fitur_numerik = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous'] # Disesuaikan dengan gambar
        self.metrik_evaluasi = {}

    # ... (metode praproses_data tidak berubah) ...
    def praproses_data(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        try:
            fitur_yang_tidak_ada = [f for f in self.fitur_numerik if f not in self.data.columns]
            if fitur_yang_tidak_ada:
                pesan = f"Fitur berikut tidak ditemukan: {fitur_yang_tidak_ada}"
                logger.error(pesan)
                return False, None, pesan
            
            self.data = self.data.dropna(subset=self.fitur_numerik)
            logger.info("Praproses data selesai")
            return True, self.data[self.fitur_numerik], "Data siap untuk proses segmentasi"
        except Exception as e:
            pesan_error = f"Gagal dalam praproses data: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error


    # ... (metode jalankan_segmentasi dan _hitung_metrik_evaluasi tidak berubah) ...
    def jalankan_segmentasi(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        try:
            sukses, data_proses, pesan = self.praproses_data()
            if not sukses:
                return False, None, pesan
            
            self.label_klaster = self.model.fit_predict(data_proses)
            self.data['Klaster'] = self.label_klaster
            self._hitung_metrik_evaluasi(data_proses)

            logger.info("Proses clustering dijalankan")
            return True, self.data, "Segmentasi nasabah berhasil dilakukan"
        except Exception as e:
            pesan_error = f"Gagal menjalankan segmentasi: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def _hitung_metrik_evaluasi(self, data_proses: pd.DataFrame) -> None:
        try:
            if len(np.unique(self.label_klaster)) > 1:
                self.metrik_evaluasi['silhouette'] = silhouette_score(data_proses, self.label_klaster)
            
            self.metrik_evaluasi['ukuran_klaster'] = pd.Series(self.label_klaster).value_counts().to_dict()
            
            data_dengan_klaster = data_proses.copy()
            data_dengan_klaster['Klaster'] = self.label_klaster
            self.metrik_evaluasi['rata_rata_fitur'] = data_dengan_klaster.groupby('Klaster').mean().to_dict()
        except Exception as e:
            logger.warning(f"Gagal menghitung beberapa metrik evaluasi: {str(e)}")


    # ... (metode tampilkan_hasil_klaster, lihat_detail_klaster, dan simpan_hasil tidak berubah) ...
    def tampilkan_hasil_klaster(self) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        if self.label_klaster is None:
            return False, None, "Segmentasi belum dijalankan. Jalankan segmentasi terlebih dahulu."
        try:
            hasil = {
                'data': self.data.to_dict(orient='records'),
                'metrik': self.metrik_evaluasi,
                'pusat_klaster': self.model.cluster_centers_.tolist(),
                'jumlah_klaster': self.jumlah_klaster
            }
            logger.info("Tampil tabel cluster")
            return True, hasil, "Hasil segmentasi berhasil diambil"
        except Exception as e:
            pesan_error = f"Gagal menyiapkan hasil klaster: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def lihat_detail_klaster(self, id_klaster: int) -> Tuple[bool, Optional[pd.DataFrame], str]:
        if self.label_klaster is None:
            return False, None, "Segmentasi belum dijalankan. Jalankan segmentasi terlebih dahulu."
        if id_klaster not in set(self.label_klaster):
            return False, None, f"Klaster {id_klaster} tidak ditemukan"
        try:
            data_klaster = self.data[self.data['Klaster'] == id_klaster]
            logger.info(f"Detail anggota segmen {id_klaster} muncul")
            return True, data_klaster, f"Detail klaster {id_klaster}"
        except Exception as e:
            pesan_error = f"Gagal mengambil detail klaster: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def simpan_hasil(self, path_output: str) -> Tuple[bool, str]:
        if self.label_klaster is None:
            return False, "Segmentasi belum dijalankan. Jalankan segmentasi terlebih dahulu."
        try:
            self.data.to_csv(path_output, index=False)
            logger.info("Notifikasi 'Berhasil disimpan'")
            return True, f"Hasil segmentasi berhasil disimpan di {path_output}"
        except Exception as e:
            pesan_error = f"Gagal menyimpan hasil: {str(e)}"
            logger.error(pesan_error)
            return False, pesan_error


    def segmentasi_ulang(self, jumlah_klaster_baru: int) -> Tuple[bool, Optional[pd.DataFrame], str]:
        try:
            # --- PERUBAHAN DIMULAI DI SINI ---
            if jumlah_klaster_baru <= 0:
                pesan_error = "Jumlah klaster harus lebih besar dari 0."
                logger.error(pesan_error)
                return False, None, pesan_error
            # --- PERUBAHAN SELESAI ---

            self.jumlah_klaster = jumlah_klaster_baru
            self.model = KMeans(n_clusters=self.jumlah_klaster, random_state=42)

            return self.jalankan_segmentasi()

        except Exception as e:
            pesan_error = f"Gagal melakukan segmentasi ulang: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error