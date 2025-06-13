**Readme: Sistem Segmentasi & Rekomendasi Nasabah**

**Kelompok Ketoprak GBA**
Anggota:
1. Rifki Arif Febrian - 103052300041
2. Raya Ramadha Fitroh - 103052300024
3. Enuka Lula Ansori - 103052300070
4. Muhammad Umar - 103052330102

**Deskripsi Sistem**
Sistem ini dirancang untuk melakukan segmentasi nasabah dan memberikan rekomendasi produk berdasarkan karakteristik masing-masing segmen. Sistem ini mencakup proses mulai dari unggah data, pemrosesan data, segmentasi, hingga visualisasi dan rekomendasi produk.

**Fitur Utama**
1. Manajemen Pengguna: Mengelola data pengguna sistem dengan berbagai role seperti admin, marketing, dan management.

2. Proses Data:
      - Unggah data dalam format CSV (maksimal 200MB)
      - Pemilihan fitur untuk analisis
      - Pemrosesan data untuk persiapan segmentasi

3. Segmentasi Nasabah:
      - Pemilihan metode segmentasi (K-Means, DBSCAN)
      - Penentuan jumlah cluster
      - Evaluasi hasil segmentasi (Silhouette Score)
4. Visualisasi & Analisis:
      - Distribusi nasabah per segmen
      - Analisis fitur penting setiap segmen
5. Rekomendasi Produk:
      - Rekomendasi produk per segmen nasabah
      - Simulasi rekomendasi individual
      - Feedback user terhadap rekomendasi
  
**Panduan Penggunaan**
1. Login:
      - Masukkan username dan password yang valid

2. Unggah Data:
      - Klik "Browse files" atau drag and drop file CSV
      - Pastikan data memenuhi format yang ditentukan

3. Proses Data:
      - Sistem akan memproses data secara otomatis
      - Lakukan pemilihan fitur jika diperlukan
      - Klik "Ulangi Proses" jika perlu menyesuaikan parameter

4. Segmentasi:
      - Pilih metode segmentasi (K-Means atau DBSCAN)
      - Tentukan jumlah cluster yang diinginkan
      - Klik "Jalankan Segmentasi"
      - Sistem akan menampilkan hasil segmentasi dan Silhouette Score

5. Visualisasi & Rekomendasi:
      - Lihat distribusi nasabah per segmen
      - Analisis karakteristik setiap segmen
      - Sistem akan menampilkan rekomendasi produk untuk setiap segmen

6. Simulasi Individual:
      - Masukkan parameter nasabah untuk mendapatkan rekomendasi khusus
      - Sistem akan menampilkan skor rekomendasi (contoh: 88/100)
      - Nasabah dapat memberikan feedback terhadap rekomendasi
  
**Catatan**
      - Sistem hanya mendukung file CSV hingga 200MB
