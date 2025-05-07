import pandas as pd

class DataLoader:
    def __init__(self, file_path="bank.csv"):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"Dataset '{self.file_path}' berhasil dimuat.")
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' tidak ditemukan.")
        return self.data