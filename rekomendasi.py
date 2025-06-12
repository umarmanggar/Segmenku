import pandas as pd
from typing import Tuple, Optional, Dict

# --- Kelas untuk Rekomendasi Berbasis Segmen (TETAP ADA) ---
class SistemRekomendasi:
    # ... (isi kelas ini sama seperti sebelumnya, tidak perlu diubah)
    def __init__(self, data: pd.DataFrame, konfig_produk: Optional[Dict] = None):
        if 'Klaster' not in data.columns:
            raise ValueError("Error: Kolom 'Klaster' tidak ditemukan.")
        self.data = data
        self.konfig_produk = konfig_produk or self._default_konfig()

    def _default_konfig(self) -> Dict:
        return {
            0: {'produk': 'Tabungan Berjangka', 'alasan': 'Profil risiko rendah, saldo stabil.'},
            1: {'produk': 'Kredit Usaha Mikro', 'alasan': 'Aktivitas transaksi tinggi, potensi usaha.'},
            2: {'produk': 'Reksa Dana Pendapatan Tetap', 'alasan': 'Saldo tinggi, profil risiko moderat.'},
            3: {'produk': 'Asuransi Jiwa', 'alasan': 'Memiliki tanggungan, butuh proteksi jangka panjang.'}
        }

    def buat_rekomendasi(self) -> Tuple[bool, pd.DataFrame, str]:
        try:
            def get_rekomendasi(klaster):
                return self.konfig_produk.get(klaster, {'produk': 'Tidak Ada', 'alasan': 'Tidak ada rekomendasi spesifik.'})
            rekomendasi = self.data['Klaster'].apply(get_rekomendasi)
            self.data['Produk_Rekomendasi'] = [item['produk'] for item in rekomendasi]
            self.data['Alasan_Rekomendasi'] = [item['alasan'] for item in rekomendasi]
            return True, self.data, "Rekomendasi produk berhasil dibuat."
        except Exception as e:
            return False, self.data, f"Gagal membuat rekomendasi: {e}"


# --- KELAS BARU UNTUK REKOMENDASI INDIVIDUAL (SESUAI SKENARIO RP) ---
class RekomendasiIndividual:
    """
    Kelas untuk memberikan rekomendasi berdasarkan input parameter individual.
    """
    def __init__(self):
        # Tempat untuk menyimpan feedback dari user (rating bintang)
        self.user_feedback = []

    def dapatkan_rekomendasi(self, usia: int, transaksi: int) -> Tuple[Optional[str], Optional[int]]:
        """
        Logika bisnis untuk menentukan produk dan skor berdasarkan input.
        Ini adalah contoh, aturan bisa dibuat lebih kompleks.
        """
        # RP-003-01: Logika jika tidak ada produk yang cocok
        if usia < 17:
            return None, None # Tidak ada produk untuk anak di bawah umur

        # RP-003-00: Logika untuk menentukan produk dan skor
        if usia > 55 and transaksi < 5:
            return "Produk Dana Pensiun", 95
        elif usia > 40 and transaksi > 20:
            return "Investasi Obligasi", 90
        elif usia < 30 and transaksi > 15:
            return "Kartu Kredit Milenial", 88
        elif transaksi > 10:
            return "Tabungan Digital", 85
        else:
            return "Tabungan Reguler", 70

    def simpan_feedback(self, produk: str, rating: int) -> bool:
        """
        Menyimpan feedback rating dari pengguna.
        Untuk demo, kita hanya simpan di memory. Di aplikasi nyata, ini akan disimpan ke database.
        """
        # RP-005
        if not produk or not rating:
            return False

        self.user_feedback.append({'produk': produk, 'rating': rating})
        print(f"Feedback diterima: {self.user_feedback[-1]}")
        return True