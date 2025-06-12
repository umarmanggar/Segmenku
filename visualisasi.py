# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# import numpy as np
# import os
# from typing import Tuple, Optional, Dict, Any
# from io import BytesIO
# import base64
# import logging

# # Konfigurasi logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class VisualisasiData:
#     def __init__(self, data: pd.DataFrame):
#         self.data = data
#         self.warna_klaster = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F']

#     def buat_pie_chart_klaster(self) -> Tuple[bool, Optional[str], str]:
#         try:
#             if 'Klaster' not in self.data.columns:
#                 return False, None, "Kolom 'Klaster' tidak ditemukan. Jalankan segmentasi terlebih dahulu."

#             plt.figure(figsize=(8, 6))
#             distribusi = self.data['Klaster'].value_counts()
#             plt.pie(distribusi,
#                     labels=distribusi.index,
#                     colors=self.warna_klaster[:len(distribusi)],
#                     autopct='%1.1f%%',
#                     startangle=90)
#             plt.title('Distribusi Nasabah per Segmen')

#             # Konversi ke base64 untuk tampilan di Streamlit
#             img_buffer = BytesIO()
#             plt.savefig(img_buffer, format='png')
#             plt.close()
#             img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

#             logger.info("Grafik pie chart muncul")
#             return True, img_base64, "Grafik distribusi segmen berhasil dibuat"

#         except Exception as e:
#             pesan_error = f"Gagal membuat pie chart: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def buat_bar_chart_usia(self) -> Tuple[bool, Optional[str], str]:
#         try:
#             if 'Klaster' not in self.data.columns or 'usia' not in self.data.columns:
#                 return False, None, "Data tidak lengkap. Pastikan sudah ada kolom 'Klaster' dan 'usia'"

#             plt.figure(figsize=(10, 6))
#             sns.boxplot(data=self.data, x='Klaster', y='usia', palette=self.warna_klaster)
#             plt.title('Distribusi Usia per Segmen')
#             plt.xlabel('Segmen')
#             plt.ylabel('Usia')

#             img_buffer = BytesIO()
#             plt.savefig(img_buffer, format='png')
#             plt.close()
#             img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

#             logger.info("Bar chart ditampilkan")
#             return True, img_base64, "Grafik distribusi usia berhasil dibuat"

#         except Exception as e:
#             pesan_error = f"Gagal membuat bar chart usia: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def filter_dan_update_grafik(self, fitur_filter: str, nilai_filter: Any) -> Tuple[bool, Optional[Dict[str, str]], str]:
#         try:
#             if fitur_filter not in self.data.columns:
#                 return False, None, f"Kolom {fitur_filter} tidak ditemukan"

#             data_filter = self.data[self.data[fitur_filter] == nilai_filter]

#             # Buat pie chart
#             sukses_pie, pie_base64, pesan_pie = self.buat_pie_chart_klaster()
#             if not sukses_pie:
#                 return False, None, pesan_pie

#             # Buat bar chart usia
#             sukses_bar, bar_base64, pesan_bar = self.buat_bar_chart_usia()
#             if not sukses_bar:
#                 return False, None, pesan_bar

#             hasil = {
#                 'pie_chart': pie_base64,
#                 'bar_chart': bar_base64
#             }

#             logger.info("Grafik ter-update")
#             return True, hasil, "Grafik berhasil diperbarui dengan filter"

#         except Exception as e:
#             pesan_error = f"Gagal memfilter grafik: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def buat_tooltip_info(self, hover_data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], str]:
#         try:
#             # Contoh: hitung statistik untuk nasabah di area hover
#             # Implementasi aktual tergantung pada library visualisasi yang digunakan
#             tooltip_info = {
#                 'jumlah_nasabah': len(self.data),
#                 'rata_rata_usia': self.data['usia'].mean(),
#                 'segment_terbesar': self.data['Klaster'].value_counts().idxmax()
#             }

#             logger.info("Info nasabah muncul")
#             return True, tooltip_info, "Data tooltip berhasil dibuat"

#         except Exception as e:
#             pesan_error = f"Gagal membuat tooltip: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def ekspor_visualisasi(self, jenis_grafik: str = 'pie') -> Tuple[bool, Optional[str], str]:
#         try:
#             if jenis_grafik == 'pie':
#                 sukses, img_base64, pesan = self.buat_pie_chart_klaster()
#             elif jenis_grafik == 'bar':
#                 sukses, img_base64, pesan = self.buat_bar_chart_usia()
#             else:
#                 return False, None, "Jenis grafik tidak valid"

#             if not sukses:
#                 return False, None, pesan

#             # Simpan ke file
#             nama_file = f"grafik_{jenis_grafik}_segmentasi.png"
#             with open(nama_file, "wb") as f:
#                 f.write(base64.b64decode(img_base64))

#             logger.info("File di ekspor")
#             return True, nama_file, f"Grafik berhasil disimpan sebagai {nama_file}"

#         except Exception as e:
#             pesan_error = f"Gagal mengekspor grafik: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

#     def buat_scatter_plot(self, fitur_x: str, fitur_y: str) -> Tuple[bool, Optional[str], str]:
#         try:
#             if 'Klaster' not in self.data.columns or fitur_x not in self.data.columns or fitur_y not in self.data.columns:
#                 return False, None, "Data tidak lengkap. Pastikan kolom klaster dan fitur tersedia"

#             plt.figure(figsize=(10, 6))
#             sns.scatterplot(data=self.data, x=fitur_x, y=fitur_y, hue='Klaster',
#                            palette=self.warna_klaster, s=100)
#             plt.title(f'Visualisasi Segmen: {fitur_x} vs {fitur_y}')
#             plt.legend(title='Segmen')

#             img_buffer = BytesIO()
#             plt.savefig(img_buffer, format='png')
#             plt.close()
#             img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

#             return True, img_base64, "Scatter plot berhasil dibuat"

#         except Exception as e:
#             pesan_error = f"Gagal membuat scatter plot: {str(e)}"
#             logger.error(pesan_error)
#             return False, None, pesan_error

# File: visualisasi.py
# Deskripsi: Kelas untuk membuat berbagai visualisasi data hasil segmentasi.
# Relevan dengan SRS Bab 3.2 (REQ-2) dan Test Case VD-01 hingga VD-05.

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
        