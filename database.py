# File: database.py
# Deskripsi: Modul untuk menangani semua interaksi dengan database SQLite.

import sqlite3
import pandas as pd
import os

DB_FILE = "bank_segmentation.db"

def get_db_connection():
    """Membuat dan mengembalikan koneksi ke database."""
    conn = sqlite3.connect(DB_FILE)
    return conn

def init_db():
    """
    Inisialisasi database dan membuat tabel jika belum ada.
    Fungsi ini aman untuk dijalankan setiap kali aplikasi dimulai.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabel untuk menyimpan data yang telah diproses oleh Admin
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_data (
        age REAL,
        balance REAL,
        duration REAL,
        campaign REAL
        -- Tambahkan kolom lain sesuai dengan hasil transformasi data Anda
        -- Nama kolom setelah one-hot encoding bisa dinamis, jadi menyimpan
        -- dalam format ini mungkin memerlukan penanganan lebih lanjut atau
        -- menyimpan sebagai file CSV/pickle yang path-nya disimpan di DB.
        -- Untuk kesederhanaan, kita fokus pada fitur numerik utama.
    )
    """)

    # Tabel untuk menyimpan data yang sudah di-cluster oleh Tim Pemasaran
    # SRS: REQ-1.3
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clustered_data (
        age REAL,
        balance REAL,
        duration REAL,
        campaign REAL,
        Klaster INTEGER,
        Produk_Rekomendasi TEXT,
        Kategori_Produk TEXT,
        Alasan_Rekomendasi TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database berhasil diinisialisasi.")

def save_dataframe(df: pd.DataFrame, table_name: str):
    """
    Menyimpan Pandas DataFrame ke dalam tabel SQLite.
    if_exists='replace' akan menghapus tabel lama dan menggantinya dengan data baru.
    """
    conn = get_db_connection()
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"DataFrame berhasil disimpan ke tabel '{table_name}'.")
    except Exception as e:
        print(f"Gagal menyimpan DataFrame: {e}")
    finally:
        conn.close()

def load_dataframe(table_name: str) -> pd.DataFrame:
    """
    Memuat data dari tabel SQLite ke dalam Pandas DataFrame.
    """
    if not os.path.exists(DB_FILE):
        return None

    conn = get_db_connection()
    try:
        # Cek apakah tabel ada
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.fetchone() is None:
            return None

        # Jika ada, muat data
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        print(f"DataFrame berhasil dimuat dari tabel '{table_name}'.")
        return df
    except Exception as e:
        print(f"Gagal memuat DataFrame: {e}")
        return None
    finally:
        conn.close()