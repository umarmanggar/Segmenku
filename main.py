import streamlit as st
from dataload import DataLoader
from clustering import ClusteringModel
from visualisasi import Visualization
from rekomendasi import RecommendationSystem

# 🎨 Pengaturan Halaman
st.set_page_config(page_title="Segmenku", layout="wide", page_icon="💳")

# 🎯 Judul Aplikasi
st.markdown("<h1 style='text-align: center;'>💼 Segmenku</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Clustering & Rekomendasi Produk Bank</h4>", unsafe_allow_html=True)
st.markdown("---")

# 📂 Sidebar: Upload Data
st.sidebar.title("📁 Upload Dataset")
file_path = st.sidebar.file_uploader("Unggah file CSV Anda di sini", type=["csv"])

# 📊 Proses dan Analisis Data
if file_path is not None:
    with st.spinner("🔄 Sedang memuat data..."):
        loader = DataLoader(file_path)
        data = loader.load_data()

    st.success("✅ Data berhasil dimuat!")

    # 🔍 Tampilkan Data
    st.subheader("📋 Data Nasabah")
    st.dataframe(data.head(), use_container_width=True)

    # 🚀 Clustering
    clustering = ClusteringModel(data)
    clustering.fit_model()

    # 📈 Visualisasi Clustering
    st.subheader("📊 Visualisasi Hasil Clustering")
    col1, col2 = st.columns(2)

    with col1:
        Visualization.plot_clusters(clustering.data, 'age', 'balance')
    with col2:
        st.write("📌 Distribusi Cluster")
        cluster_counts = clustering.data['Cluster'].value_counts()
        st.bar_chart(cluster_counts)

    # 💡 Rekomendasi Produk
    st.subheader("🎯 Rekomendasi Produk")
    recommender = RecommendationSystem(clustering.data)
    recommendations = recommender.generate_recommendations()
    st.write(recommendations)

    if st.button("💾 Simpan Rekomendasi ke CSV"):
        recommender.save_recommendations("hasil_rekomendasi.csv")
        st.success("📁 Rekomendasi disimpan sebagai 'hasil_rekomendasi.csv'")

    # 📚 Sidebar Informasi
    st.sidebar.markdown("### ℹ️ Informasi Aplikasi")
    st.sidebar.info(
        "🔍 Aplikasi ini menggunakan **Clustering KMeans** untuk mengelompokkan nasabah berdasarkan usia dan saldo, "
        "kemudian memberikan rekomendasi produk bank yang sesuai untuk setiap segmen."
    )

else:
    st.warning("⚠️ Silakan unggah file CSV terlebih dahulu.")

# 📌 Footer
st.markdown("---")
st.markdown("📘 **Tentang Aplikasi**")
st.markdown("Aplikasi ini dirancang untuk membantu pihak bank dalam memahami kebutuhan nasabah dan menyarankan produk yang sesuai secara otomatis berdasarkan analisis data.")

