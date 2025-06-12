import pandas as pd
import logging
from typing import Tuple, Optional, Dict, Any

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SistemRekomendasi:
    """
    Kelas untuk menghasilkan rekomendasi produk berdasarkan segmentasi.
    """
    def __init__(self, data: pd.DataFrame, konfig_produk: Optional[Dict] = None):
        if 'Klaster' not in data.columns:
            raise ValueError("Error: Kolom 'Klaster' tidak ditemukan. Lakukan segmentasi dahulu.")
        self.data = data
        # SRS REQ-3.2: Kemampuan menyesuaikan rekomendasi (melalui parameter konfig_produk)
        self.konfig_produk = konfig_produk or self._default_konfig()

    def _default_konfig(self) -> Dict:
        """Menyediakan konfigurasi produk default."""
        return {
            0: {'produk': 'Tabungan Berjangka', 'alasan': 'Profil risiko rendah, saldo stabil', 'kategori': 'Tabungan'},
            1: {'produk': 'Kredit Usaha Mikro', 'alasan': 'Aktivitas transaksi tinggi, potensi usaha', 'kategori': 'Kredit'},
            2: {'produk': 'Reksa Dana Pendapatan Tetap', 'alasan': 'Saldo tinggi, profil risiko moderat', 'kategori': 'Investasi'},
            3: {'produk': 'Asuransi Jiwa', 'alasan': 'Memiliki tanggungan keluarga, butuh proteksi', 'kategori': 'Asuransi'},
            4: {'produk': 'Deposito', 'alasan': 'Dana idle, butuh imbal hasil tetap', 'kategori': 'Investasi'}
        }

    # Test Case: RP-01-01 (Tampilkan rekomendasi produk)
    # SRS: REQ-3.1
    def buat_rekomendasi(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Membuat kolom rekomendasi produk berdasarkan klaster nasabah.
        """
        try:
            self.data['Produk_Rekomendasi'] = self.data['Klaster'].map(lambda x: self.konfig_produk.get(x, {}).get('produk', 'Tidak Ada'))
            self.data['Kategori_Produk'] = self.data['Klaster'].map(lambda x: self.konfig_produk.get(x, {}).get('kategori', 'Tidak Ada'))
            self.data['Alasan_Rekomendasi'] = self.data['Klaster'].map(lambda x: self.konfig_produk.get(x, {}).get('alasan', 'Tidak Ada'))

            # Pesan sesuai log pada Test Case RP-01-01
            logger.info("Tampil daftar produk")
            return True, self.data, "Rekomendasi produk berhasil dibuat"
        except Exception as e:
            return False, None, f"Gagal membuat rekomendasi: {str(e)}"

    # Test Case: RP-01-02 (Lihat detail produk)
    # SRS: REQ-3.3
    def tampilkan_detail_produk(self, nama_produk: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Menampilkan detail untuk produk yang dipilih.
        """
        try:
            for klaster, info in self.konfig_produk.items():
                if info['produk'].lower() == nama_produk.lower():
                    detail_produk = {
                        'Nama Produk': info['produk'],
                        'Kategori': info['kategori'],
                        'Alasan Rekomendasi': info['alasan'],
                        'Target Klaster': klaster
                    }
                    # Pesan sesuai log pada Test Case RP-01-02
                    logger.info("Modal atau detail terbuka")
                    return True, detail_produk, "Detail produk berhasil diambil."
            return False, None, f"Produk '{nama_produk}' tidak ditemukan."
        except Exception as e:
            return False, None, f"Gagal mengambil detail produk: {str(e)}"

    # Test Case: RP-01-04 (Filter rekomendasi)
    # SRS: REQ-2.2
    def filter_rekomendasi(self, kategori: str) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Memfilter data rekomendasi berdasarkan kategori produk.
        """
        try:
            if 'Kategori_Produk' not in self.data.columns:
                return False, None, "Buat rekomendasi terlebih dahulu."

            if kategori.lower() == 'semua':
                data_filter = self.data
            else:
                data_filter = self.data[self.data['Kategori_Produk'].str.lower() == kategori.lower()]

            if data_filter.empty:
                return False, None, f"Tidak ada rekomendasi untuk kategori '{kategori}'."

            # Pesan sesuai log pada Test Case RP-01-04
            logger.info("Filter aktif")
            return True, data_filter, f"Filter untuk kategori '{kategori}' berhasil."
        except Exception as e:
            return False, None, f"Gagal memfilter rekomendasi: {str(e)}"

    # Test Case: RP-01-03 & RP-01-05 (Simpan/Ekspor rekomendasi)
    # SRS: REQ-3
    def ekspor_rekomendasi_csv(self, path_output: str) -> Tuple[bool, str]:
        """
        Mengekspor DataFrame dengan rekomendasi ke file CSV.
        """
        if 'Produk_Rekomendasi' not in self.data.columns:
            return False, "Tidak ada data rekomendasi untuk diekspor."

        try:
            self.data.to_csv(path_output, index=False)
            # Pesan sesuai log pada Test Case RP-01-03 & RP-01-05
            logger.info(f"Proses penyimpanan/ekspor ke {path_output}")
            return True, f"Rekomendasi berhasil diekspor ke {path_output}"
        except Exception as e:
            return False, f"Gagal mengekspor rekomendasi: {str(e)}"