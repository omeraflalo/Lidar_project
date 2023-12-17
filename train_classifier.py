import csv
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
from classifiers import classifiers
from data_preprocessor import DataPreprocessor
from model_trainer import ModelTrainer
from excel_formatter import ExcelFormatter


class TrainClassifier:
    def __init__(self, version):
        self.version = version
        self.data_file = f'models/version {version}/raw_data.csv'
        self.scaler_file = f'models/version {version}/scaler.pkl'
        self.excel_file = f'models/version {version}/model_evaluations.xlsx'
        self.preprocessor = DataPreprocessor()
        self.trainer = ModelTrainer(classifiers)

    def load_data(self):
        X, Y = [], []
        with open(self.data_file, 'r') as file:
            csvreader = csv.reader(file, delimiter=';')
            for row in csvreader:
                X.append(row[1])
                Y.append(row[0])
        return X, Y

    def run(self):
        X, Y = self.load_data()
        X = self.preprocessor.preprocess(X)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

        scaler = StandardScaler()
        scaler.fit(X_train)

        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        results, best_model = self.trainer.train_and_evaluate(X_train, X_test, y_train, y_test, self.version)

        joblib.dump(scaler, self.scaler_file)

        excel_formatter = ExcelFormatter()
        excel_formatter.format_and_save(results, self.excel_file)

        print(f"\nBest Model: {best_model[1]} Classifier with an Accuracy of {best_model[0]}")


if __name__ == "__main__":
    trainer = TrainClassifier(version="3")
    trainer.run()
