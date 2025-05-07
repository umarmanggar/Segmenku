from sklearn.cluster import KMeans

class ClusteringModel:
    def __init__(self, data, n_clusters=3):
        self.data = data  
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.cluster_labels = None
    
    def preprocess_data(self):
        numeric_features = ['age', 'balance', 'duration', 'campaign']
        self.data = self.data.dropna(subset=numeric_features)  
        return self.data[numeric_features]
    
    def fit_model(self):
        processed_data = self.preprocess_data()
        self.cluster_labels = self.model.fit_predict(processed_data)
        self.data['Cluster'] = self.cluster_labels 
        print("Clustering selesai dan ditambahkan ke dataset.")
        return self.cluster_labels

    