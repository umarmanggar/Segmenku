class RecommendationSystem:
    def __init__(self, data):
        if 'Cluster' not in data.columns:
            raise ValueError("Error: Clustering belum dilakukan")
        self.data = data
    
    def generate_recommendations(self):
        recommendations = {
            0: "Tabungan Jangka Panjang",
            1: "Kredit Usaha Mikro",
            2: "Investasi Reksa Dana"
        }
        self.data['Recommendation'] = self.data['Cluster'].map(recommendations)
        return self.data[['age', 'balance', 'Cluster', 'Recommendation']]
    
    def save_recommendations(self, output_file="recommendations.csv"):
        recommendations = self.generate_recommendations()
        recommendations.to_csv(output_file, index=False)
        print(f"Hasil rekomendasi disimpan ke '{output_file}'.")