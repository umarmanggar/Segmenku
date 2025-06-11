import pandas as pd
import logging
from typing import Tuple, Optional, Dict, List, Any
import json

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SistemRekomendasi:
    def __init__(self, data: pd.DataFrame, konfig_produk: Optional[Dict] = None):
        """
        Inisialisasi sistem rekomendasi produk.

        Args:
            data (pd.DataFrame): Data nasabah yang sudah termasuk klaster
            konfig_produk (Optional[Dict]): Konfigurasi mapping klaster ke produk
        """
        if 'Klaster' not in data.columns:
            raise ValueError("Error: Segmentasi belum dilakukan. Kolom 'Klaster' tidak ditemukan.")

        self.data = data
        self.konfig_produk = konfig_produk or {
            0: {
                'produk': 'Tabungan Berjangka',
                'alasan': 'Nasabah dengan profil risiko rendah dan saldo stabil',
                'kategori': 'Tabungan'
            },
            1: {
                'produk': 'Kredit Usaha Mikro',
                'alasan': 'Nasabah dengan aktivitas transaksi tinggi dan potensi usaha',
                'kategori': 'Kredit'
            },
            2: {
                'produk': 'Reksa Dana Pendapatan Tetap',
                'alasan': 'Nasabah dengan saldo tinggi dan profil risiko moderat',
                'kategori': 'Investasi'
            },
            3: {
                'produk': 'Asuransi Jiwa',
                'alasan': 'Nasabah dengan tanggungan keluarga dan kebutuhan proteksi',
                'kategori': 'Asuransi'
            },
            4: {
                'produk': 'Deposito',
                'alasan': 'Nasabah dengan dana menganggur dan kebutuhan imbal hasil tetap',
                'kategori': 'Investasi'
            }
        }

    def buat_rekomendasi(self) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Membuat rekomendasi produk untuk setiap nasabah berdasarkan klaster (RP-01-01).

        Returns:
            Tuple[bool, Optional[pd.DataFrame], str]:
                - Status keberhasilan
                - DataFrame dengan rekomendasi
                - Pesan status
        """
        try:
            # Tambahkan rekomendasi ke dataset
            self.data['Produk_Rekomendasi'] = self.data['Klaster'].map(lambda x: self.konfig_produk[x]['produk'])
            self.data['Kategori_Produk'] = self.data['Klaster'].map(lambda x: self.konfig_produk[x]['kategori'])
            self.data['Alasan_Rekomendasi'] = self.data['Klaster'].map(lambda x: self.konfig_produk[x]['alasan'])

            logger.info("Tampil daftar produk")
            return True, self.data, "Rekomendasi produk berhasil dibuat"

        except Exception as e:
            pesan_error = f"Gagal membuat rekomendasi: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def tampilkan_detail_produk(self, nama_produk: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Menampilkan detail produk tertentu (RP-01-02).

        Args:
            nama_produk (str): Nama produk yang ingin dilihat detailnya

        Returns:
            Tuple[bool, Optional[Dict], str]:
                - Status keberhasilan
                - Detail produk
                - Pesan status
        """
        try:
            # Cari produk dalam konfigurasi
            detail_produk = None
            for klaster, produk_info in self.konfig_produk.items():
                if produk_info['produk'].lower() == nama_produk.lower():
                    detail_produk = {
                        'nama': produk_info['produk'],
                        'kategori': produk_info['kategori'],
                        'deskripsi': produk_info['alasan'],
                        'klaster_target': klaster,
                        'jumlah_nasabah': len(self.data[self.data['Klaster'] == klaster])
                    }
                    break

            if not detail_produk:
                return False, None, f"Produk '{nama_produk}' tidak ditemukan"

            logger.info("Modal atau detail terbuka")
            return True, detail_produk, "Detail produk berhasil diambil"

        except Exception as e:
            pesan_error = f"Gagal mengambil detail produk: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def simpan_rekomendasi(self, format_file: str = 'csv') -> Tuple[bool, Optional[str], str]:
        """
        Menyimpan hasil rekomendasi (RP-01-03).

        Args:
            format_file (str): Format file output ('csv' atau 'json')

        Returns:
            Tuple[bool, Optional[str], str]:
                - Status keberhasilan
                - Nama file yang disimpan
                - Pesan status
        """
        try:
            # Pastikan rekomendasi sudah dibuat
            if 'Produk_Rekomendasi' not in self.data.columns:
                sukses, _, pesan = self.buat_rekomendasi()
                if not sukses:
                    return False, None, pesan

            nama_file = f"rekomendasi_produk.{format_file}"

            if format_file == 'csv':
                self.data[['id_nasabah', 'Klaster', 'Produk_Rekomendasi', 'Kategori_Produk']].to_csv(nama_file, index=False)
            elif format_file == 'json':
                rekomendasi_json = self.data[['id_nasabah', 'Klaster', 'Produk_Rekomendasi', 'Kategori_Produk']].to_dict(orient='records')
                with open(nama_file, 'w') as f:
                    json.dump(rekomendasi_json, f)
            else:
                return False, None, "Format file tidak didukung. Gunakan 'csv' atau 'json'"

            logger.info("Proses penyimpanan")
            return True, nama_file, f"Rekomendasi berhasil disimpan sebagai {nama_file}"

        except Exception as e:
            pesan_error = f"Gagal menyimpan rekomendasi: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def filter_rekomendasi(self, kategori: str) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Filter rekomendasi berdasarkan kategori produk (RP-01-04).

        Args:
            kategori (str): Kategori produk untuk filter

        Returns:
            Tuple[bool, Optional[pd.DataFrame], str]:
                - Status keberhasilan
                - DataFrame hasil filter
                - Pesan status
        """
        try:
            if 'Kategori_Produk' not in self.data.columns:
                sukses, _, pesan = self.buat_rekomendasi()
                if not sukses:
                    return False, None, pesan

            # Daftar kategori yang valid
            kategori_valid = set(info['kategori'] for info in self.konfig_produk.values())

            if kategori.lower() == 'semua':
                data_filter = self.data
            elif kategori not in kategori_valid:
                return False, None, f"Kategori '{kategori}' tidak valid. Pilihan: {', '.join(kategori_valid)}"
            else:
                data_filter = self.data[self.data['Kategori_Produk'] == kategori]

            logger.info("Filter aktif")
            return True, data_filter, f"Filter kategori '{kategori}' berhasil diterapkan"

        except Exception as e:
            pesan_error = f"Gagal memfilter rekomendasi: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def ekspor_rekomendasi_csv(self) -> Tuple[bool, Optional[str], str]:
        """
        Mengekspor hasil rekomendasi dalam format CSV (RP-01-05).

        Returns:
            Tuple[bool, Optional[str], str]:
                - Status keberhasilan
                - Nama file yang dihasilkan
                - Pesan status
        """
        try:
            # Gunakan fungsi simpan_rekomendasi dengan format CSV
            return self.simpan_rekomendasi(format_file='csv')

        except Exception as e:
            pesan_error = f"Gagal mengekspor rekomendasi: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def rekomendasi_untuk_klaster(self, id_klaster: int) -> Tuple[bool, Optional[Dict], str]:
        """
        Mendapatkan rekomendasi produk untuk klaster tertentu.

        Args:
            id_klaster (int): ID klaster yang ingin dilihat rekomendasinya

        Returns:
            Tuple[bool, Optional[Dict], str]:
                - Status keberhasilan
                - Informasi rekomendasi untuk klaster
                - Pesan status
        """
        try:
            if id_klaster not in self.konfig_produk:
                return False, None, f"Klaster {id_klaster} tidak ditemukan"

            rekomendasi = {
                'klaster': id_klaster,
                'produk': self.konfig_produk[id_klaster]['produk'],
                'kategori': self.konfig_produk[id_klaster]['kategori'],
                'alasan': self.konfig_produk[id_klaster]['alasan'],
                'jumlah_nasabah': len(self.data[self.data['Klaster'] == id_klaster]),
                'ciri_khas': self._analisis_ciri_klaster(id_klaster)
            }

            return True, rekomendasi, "Rekomendasi untuk klaster berhasil diambil"

        except Exception as e:
            pesan_error = f"Gagal mengambil rekomendasi klaster: {str(e)}"
            logger.error(pesan_error)
            return False, None, pesan_error

    def _analisis_ciri_klaster(self, id_klaster: int) -> Dict[str, Any]:
        """
        Analisis ciri khas nasabah dalam suatu klaster.

        Args:
            id_klaster (int): ID klaster yang dianalisis

        Returns:
            Dict[str, Any]: Statistik deskriptif untuk klaster tersebut
        """
        data_klaster = self.data[self.data['Klaster'] == id_klaster]

        if data_klaster.empty:
            return {}

        # Hitung statistik numerik
        stat_numerik = {}
        kolom_numerik = data_klaster.select_dtypes(include=['number']).columns
        for kolom in kolom_numerik:
            stat_numerik[kolom] = {
                'rata_rata': data_klaster[kolom].mean(),
                'median': data_klaster[kolom].median(),
                'min': data_klaster[kolom].min(),
                'max': data_klaster[kolom].max()
            }

        # Hitung statistik kategorikal
        stat_kategorikal = {}
        kolom_kategorikal = data_klaster.select_dtypes(include=['object']).columns
        for kolom in kolom_kategorikal:
            if kolom not in ['Produk_Rekomendasi', 'Kategori_Produk', 'Alasan_Rekomendasi']:
                stat_kategorikal[kolom] = data_klaster[kolom].value_counts().to_dict()

        return {
            'numerik': stat_numerik,
            'kategorikal': stat_kategorikal
        }