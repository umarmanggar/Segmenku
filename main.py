from dataload import DataLoader
from clustering import ClusteringModel
from visualisasi import Visualization
from rekomendasi import RecommendationSystem

import streamlit as st
st.title("Segmenku: Clustering dan Rekomendasi Produk Bank")

# Load dataste
file_path = "bank.csv"
loader = DataLoader(file_path)
data = loader.load_data()

# Clustering
clustering = ClusteringModel(data)
clustering.fit_model()

# Visualisasi hasil clustering
Visualization.plot_clusters(clustering.data, 'age', 'balance')

# Rekomendasi produk
recommender = RecommendationSystem(clustering.data)
print(recommender.generate_recommendations())

# Simpan hasil rekomendasi
recommender.save_recommendations("hasil_rekomendasi.csv")

#output total masing-masing cluster
print(clustering.data['Cluster'].value_counts())