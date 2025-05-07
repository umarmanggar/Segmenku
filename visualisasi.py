import matplotlib.pyplot as plt
import pandas as pd
import os

class Visualization:
    # Kelas untuk menampilkan hasil clustering dalam bentuk grafik
    @staticmethod
    def plot_clusters(data, x_feature, y_feature):
        plt.figure(figsize=(8,6))
        plt.scatter(data[x_feature], data[y_feature], c=data['Cluster'], cmap='viridis')
        plt.xlabel(x_feature)
        plt.ylabel(y_feature)
        plt.title(f'Segmen Nasabah Berdasarkan {x_feature} dan {y_feature}')
        plt.show()
