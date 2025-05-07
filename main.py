import streamlit as st
from dataload import DataLoader
from clustering import ClusteringModel
from visualisasi import Visualization
from rekomendasi import RecommendationSystem

# Pengaturan Halaman
st.set_page_config(page_title="Segmenku: Clustering dan Rekomendasi Produk Bank", layout="wide")

# Judul Aplikasi
st.title("Segmenku: Clustering dan Rekomendasi Produk Bank")
st.markdown("""
    Aplikasi ini membantu bank dalam menganalisis dan mengelompokkan nasabah serta memberikan rekomendasi produk yang sesuai.
    Silakan unggah dataset Anda untuk memulai analisis.
""")

# Sidebar untuk Unggah Dataset
st.sidebar.header("Unggah Dataset")
file_path = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

if file_path is not None:
    # Load data
    loader = DataLoader(file_path)
    data = loader.load_data()

    # Tampilkan data
    st.subheader("Data Nasabah")
    st.dataframe(data.head())

    # Clustering
    clustering = ClusteringModel(data)
    clustering.fit_model()

    # Visualisasi hasil clustering
    st.subheader("Visualisasi Hasil Clustering")
    col1, col2 = st.columns(2)
    with col1:
        Visualization.plot_clusters(clustering.data, 'age', 'balance')
    with col2:
        st.subheader("Distribusi Cluster")
        cluster_counts = clustering.data['Cluster'].value_counts()
        st.bar_chart(cluster_counts)

    # Rekomendasi produk
    recommender = RecommendationSystem(clustering.data)
    recommendations = recommender.generate_recommendations()

    # Tampilkan rekomendasi
    st.subheader("Rekomendasi Produk")
    st.write(recommendations)

    # Simpan hasil rekomendasi
    if st.button("Simpan Hasil Rekomendasi"):
        recommender.save_recommendations("hasil_rekomendasi.csv")
        st.success("Hasil rekomendasi telah disimpan sebagai 'hasil_rekomendasi.csv'.")

    # Tampilkan informasi tambahan
    st.sidebar.subheader("Informasi Tambahan")
    st.sidebar.write("Aplikasi ini menggunakan algoritma clustering untuk mengelompokkan nasabah berdasarkan usia dan saldo.")
    st.sidebar.write("Silakan unggah dataset Anda untuk memulai analisis.")

else:
    st.warning("Silakan unggah file CSV untuk melanjutkan.")

# Footer
st.markdown("---")
st.markdown("### Tentang Aplikasi")
st.markdown("Aplikasi ini dirancang untuk membantu bank dalam memahami nasabah mereka dan memberikan rekomendasi produk yang sesuai.")
