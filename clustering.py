from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
import logging
from typing import Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Segmenter:
    def __init__(self, data_asli: pd.DataFrame, data_proses: pd.DataFrame):
        if not isinstance(data_asli, pd.DataFrame) or not isinstance(data_proses, pd.DataFrame):
            raise TypeError("Data input harus berupa pandas DataFrame.")

        self.data_asli = data_asli.copy()
        self.data_proses = data_proses
        self.model = None
        self.label_klaster = None

    def jalankan_segmentasi(self, metode: str, params: dict) -> Tuple[bool, Optional[pd.DataFrame], str, Optional[float]]:
        try:
            # SN-001: Memilih metode segmentasi
            if metode == 'K-Means':
                n_clusters = params.get('n_clusters', 3)
                if n_clusters < 2: # SN-002-01 Validasi
                    return False, None, "Jumlah cluster tidak valid (harus >= 2).", None
                self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                logger.info(f"Menjalankan K-Means dengan {n_clusters} klaster.")

            elif metode == 'DBSCAN':
                # Parameter default untuk DBSCAN, bisa dibuat dinamis di UI jika perlu
                eps = params.get('eps', 0.5)
                min_samples = params.get('min_samples', 5)
                self.model = DBSCAN(eps=eps, min_samples=min_samples)
                logger.info(f"Menjalankan DBSCAN dengan eps={eps} dan min_samples={min_samples}.")

            else:
                return False, None, "Metode segmentasi tidak valid.", None

            # Menjalankan model dan menghitung skor
            self.label_klaster = self.model.fit_predict(self.data_proses)
            self.data_asli['Klaster'] = self.label_klaster

            skor_silhouette = None
            unique_labels = np.unique(self.label_klaster)
            # Silhouette score hanya bisa dihitung jika ada lebih dari 1 klaster
            if len(unique_labels) > 1:
                skor_silhouette = silhouette_score(self.data_proses, self.label_klaster)

            logger.info("Proses clustering selesai.")
            return True, self.data_asli, f"Segmentasi dengan {metode} berhasil.", skor_silhouette

        except Exception as e:
            pesan_error = f"Gagal menjalankan segmentasi: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error, None

    def dapatkan_detail_klaster(self, id_klaster: int) -> Optional[pd.DataFrame]:
        """Mendapatkan detail anggota dari sebuah klaster."""
        if 'Klaster' in self.data_asli.columns:
            return self.data_asli[self.data_asli['Klaster'] == id_klaster]
        return None