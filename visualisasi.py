import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional

class VisualisasiData:
    """
    Kelas untuk membuat visualisasi interaktif dari data nasabah yang sudah disegmentasi.
    """
    def __init__(self, df: pd.DataFrame):
        # Memastikan input adalah DataFrame untuk mencegah error
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame() # Buat DataFrame kosong jika input tidak valid
        self.df = df

        # Inisialisasi peta warna hanya jika kolom 'Klaster' ada
        if 'Klaster' in self.df.columns and not self.df.empty:
            self.color_discrete_map = {
                i: color for i, color in enumerate(px.colors.qualitative.Vivid)
            }
        else:
            self.color_discrete_map = {}

    def buat_pie_chart_klaster(self) -> Optional[go.Figure]:
        """
        Membuat pie chart interaktif untuk menunjukkan distribusi nasabah per segmen.
        Sesuai skenario VD-001-02 (pilih pie chart) dan VD-004 (interaktifitas).
        """
        try:
            # Pengecekan data yang lebih aman untuk mencegah error
            if self.df.empty or 'Klaster' not in self.df.columns:
                return None

            distribusi = self.df['Klaster'].value_counts().reset_index()
            distribusi.columns = ['Klaster_ID', 'Jumlah']

            # Jangan buat grafik jika tidak ada data setelah dihitung
            if distribusi.empty:
                return None

            fig = px.pie(
                distribusi,
                names='Klaster_ID',
                values='Jumlah',
                title='<b>Distribusi Nasabah per Segmen</b>',
                color='Klaster_ID',
                color_discrete_map=self.color_discrete_map,
                hole=.3
            )
            # Tooltip akan muncul secara default saat mouse diarahkan (hover)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            return fig
        except Exception:
            return None

    def buat_bar_chart(self, fitur: str) -> Optional[go.Figure]:
        """
        Membuat bar chart interaktif untuk menunjukkan rata-rata fitur per segmen.
        Sesuai skenario VD-001-01 (pilih bar chart) dan VD-004 (interaktifitas).
        """
        try:
            # Pengecekan data yang lebih aman
            if self.df.empty or fitur not in self.df.columns or 'Klaster' not in self.df.columns:
                return None

            rata_rata_fitur = self.df.groupby('Klaster')[fitur].mean().reset_index()

            # Jangan buat grafik jika tidak ada data setelah dihitung
            if rata_rata_fitur.empty:
                return None

            fig = px.bar(
                rata_rata_fitur,
                x='Klaster',
                y=fitur,
                title=f'<b>Rata-rata {fitur.capitalize()} per Segmen</b>',
                color='Klaster',
                color_discrete_map=self.color_discrete_map,
                text_auto='.2s'
            )
            # Tooltip akan muncul secara default saat mouse diarahkan (hover)
            return fig
        except Exception:
            return None