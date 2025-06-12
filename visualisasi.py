import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64
import logging
from typing import Tuple, Optional, Dict, Any

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisualisasiData:
    """
    Kelas untuk membuat visualisasi dari data nasabah yang sudah disegmentasi.
    """
    def __init__(self, df: pd.DataFrame):
        if 'Klaster' not in df.columns:
            raise ValueError("DataFrame harus memiliki kolom 'Klaster'.")
        self.df = df
        self.warna_klaster = sns.color_palette("viridis", len(df['Klaster'].unique()))

    def _convert_plot_to_base64(self) -> str:
        """Mengonversi plot matplotlib ke string base64."""
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        plt.close()
        return base64.b64encode(img_buffer.getvalue()).decode()

    # Test Case: VD-01-01 (Tampilkan grafik segmen)
    # SRS: REQ-2.1
    def buat_pie_chart_klaster(self) -> Tuple[bool, Optional[str], str]:
        """
        Membuat pie chart untuk menunjukkan distribusi nasabah per segmen.
        """
        try:
            plt.figure(figsize=(8, 6))
            distribusi = self.df['Klaster'].value_counts()
            plt.pie(distribusi, labels=distribusi.index, colors=self.warna_klaster, autopct='%1.1f%%', startangle=90)
            plt.title('Distribusi Nasabah per Segmen')

            img_base64 = self._convert_plot_to_base64()
            # Pesan sesuai log pada Test Case VD-01-01
            logger.info("Grafik pie chart muncul")
            return True, img_base64, "Grafik distribusi segmen berhasil dibuat"
        except Exception as e:
            return False, None, f"Gagal membuat pie chart: {e}"

    # Test Case: VD-01-02 (Lihat distribusi usia)
    # SRS: REQ-2.1
    def buat_bar_chart(self, fitur: str) -> Tuple[bool, Optional[str], str]:
        """
        Membuat box plot untuk menunjukkan distribusi fitur numerik per segmen.
        """
        if fitur not in self.df.columns:
            return False, None, f"Fitur '{fitur}' tidak ditemukan."
        try:
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=self.df, x='Klaster', y=fitur, palette=self.warna_klaster)
            plt.title(f'Distribusi {fitur.capitalize()} per Segmen')
            plt.xlabel('Segmen')
            plt.ylabel(fitur.capitalize())

            img_base64 = self._convert_plot_to_base64()
            # Pesan sesuai log pada Test Case VD-01-02
            logger.info(f"Bar chart untuk fitur '{fitur}' ditampilkan")
            return True, img_base64, f"Grafik distribusi {fitur} berhasil dibuat"
        except Exception as e:
            return False, None, f"Gagal membuat bar chart: {e}"

    # Test Case: VD-01-03 (Filter segmen)
    # SRS: REQ-2.2
    def filter_dan_update_grafik(self, fitur_filter: str, nilai_filter: Any) -> Tuple[bool, Optional[str], str]:
        """
        Memfilter data dan membuat ulang pie chart distribusi klaster.
        """
        if fitur_filter not in self.df.columns:
            return False, None, f"Kolom '{fitur_filter}' tidak ditemukan."
        try:
            filtered_df = self.df[self.df[fitur_filter] == nilai_filter]

            # Buat instance baru untuk data yang difilter
            temp_visualizer = VisualisasiData(filtered_df)
            sukses, img_base64, pesan = temp_visualizer.buat_pie_chart_klaster()

            if sukses:
                # Pesan sesuai log pada Test Case VD-01-03
                logger.info("Grafik ter-update")
                return True, img_base64, "Grafik berhasil diperbarui dengan filter"
            else:
                return False, None, pesan
        except Exception as e:
            return False, None, f"Gagal memfilter grafik: {e}"

    # Test Case: VD-01-05 (Ekspor visualisasi)
    # SRS: REQ-2
    def ekspor_visualisasi(self, plot_base64: str, nama_file: str) -> Tuple[bool, str]:
        """
        Menyimpan visualisasi sebagai file PNG.
        """
        try:
            with open(nama_file, "wb") as f:
                f.write(base64.b64decode(plot_base64))
            # Pesan sesuai log pada Test Case VD-01-05
            logger.info("File di ekspor")
            return True, f"Grafik berhasil disimpan sebagai {nama_file}"
        except Exception as e:
            return False, f"Gagal mengekspor grafik: {e}"
