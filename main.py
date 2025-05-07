import streamlit as st
from streamlit_lottie import st_lottie
import json
from dataload import DataLoader
from clustering import ClusteringModel
from visualisasi import Visualization
from rekomendasi import RecommendationSystem

# -------------------- UTILITAS --------------------
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# -------------------- KONFIGURASI HALAMAN --------------------
st.set_page_config(page_title="Segmenku", layout="wide", page_icon="📊")

# -------------------- HEADER APLIKASI --------------------
col1, col2 = st.columns([1, 2])
with col1:
    lottie_animation = load_lottiefile("lottie/bank.json")  # Tempatkan animasi Lottie di folder lottie/
    st_lottie(lottie_animation, speed=1, height=180)

with col2:
    st.title("💡 Segmenku: Clustering & Rekomendasi Produk Bank")
    st.markdown("""
    🚀 Selamat datang di **Segmenku** – platform cerdas untuk memahami nasabah bank secara lebih mendalam melalui clustering dan rekomendasi produk.
    Unggah data Anda dan biarkan algoritma bekerja untuk menghasilkan wawasan yang bermakna dan rekomendasi yang personal.
    """)

# -------------------- SIDEBAR --------------------
st.sidebar.image("assets/logo.png", width=180)  # Ganti dengan logo bank atau app kamu
st.sidebar.title("📂 Menu Aplikasi")
file_path = st.sidebar.file_uploader("📄 Unggah file CSV", type=["csv"])
st.sidebar.markdown("---")
st.sidebar.info("💡 Gunakan file yang berisi informasi nasabah seperti usia, saldo, dan status pekerjaan untuk hasil terbaik.")

# -------------------- MAIN SECTION --------------------
if file_path is not None:
    # Load Data
    with st.spinner("📊 Memuat data..."):
        loader = DataLoader(file_path)
        data = loader.load_data()

    with st.expander("📋 Lihat Data Nasabah", expanded=False):
        st.dataframe(data.head(10), use_container_width=True)

    # Clustering
    clustering = ClusteringModel(data)
    with st.spinner("🔍 Melakukan Clustering..."):
        clustering.fit_model()

    # Visualisasi
    st.markdown("## 📌 Hasil Clustering")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📈 Plot Cluster (Usia vs Saldo)")
        Visualization.plot_clusters(clustering.data, 'age', 'balance')
    with col2:
        st.markdown("#### 📊 Distribusi Cluster")
        cluster_counts = clustering.data['Cluster'].value_counts()
        st.bar_chart(cluster_counts)

    # Rekomendasi
    st.markdown("## 💼 Rekomendasi Produk")
    recommender = RecommendationSystem(clustering.data)
    with st.spinner("⚙️ Menghasilkan Rekomendasi..."):
        recommendations = recommender.generate_recommendations()
    st.write(recommendations)

    # Simpan Rekomendasi
    if st.button("💾 Simpan Hasil Rekomendasi"):
        recommender.save_recommendations("hasil_rekomendasi.csv")
        st.success("✅ Hasil rekomendasi telah disimpan sebagai `hasil_rekomendasi.csv`.")

else:
    st.warning("🚨 Silakan unggah file CSV untuk memulai analisis.")

# -------------------- FOOTER --------------------
st.markdown("---")
with st.expander("ℹ️ Tentang Aplikasi"):
    st.markdown("""
    **Segmenku** adalah aplikasi berbasis data yang bertujuan membantu industri perbankan mengenali segmen nasabah dengan lebih baik.
    Didukung oleh teknologi machine learning dan visualisasi interaktif, aplikasi ini memungkinkan pengambilan keputusan yang lebih tepat sasaran.
    """)
    st.markdown("🔗 Dibuat oleh [Muhammad Umar](https://github.com/umarmanggar) | Telkom University 💻")

