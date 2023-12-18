import numpy as np
import joblib
from enum import Enum


class Situation(Enum):
    STAND = "Stand"
    FALL = "Fall"


class FallClassifier:
    def __init__(self, model_path, scaler_path, threshold=0.75):
        self.classifier = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.threshold = threshold

    def classify(self, data):
        scaled_data = self.scaler.transform(data.reshape(1, -1))
        probabilities = self.classifier.predict_proba(scaled_data)[0]
        stand_index = list(self.classifier.classes_).index(Situation.STAND.value)
        fall_index = list(self.classifier.classes_).index(Situation.FALL.value)
        stand_probability = probabilities[stand_index]
        fall_probability = probabilities[fall_index]
        return (Situation.FALL, fall_probability) if probabilities[fall_index] > self.threshold else (
            Situation.STAND, stand_probability)


class ClassificationUpdater:
    def __init__(self, system_state, preprocessor, classifier, dbscan):
        self.system_state = system_state
        self.preprocessor = preprocessor
        self.classifier = classifier
        self.dbscan = dbscan

    def update_classification(self):
        if not self.system_state.lidar_diff:
            self.system_state.update_persons([])
            return

        classified_persons = []
        arr = np.array([coords for _, (_, coords) in self.system_state.lidar_diff.items()])
        clusters = self.dbscan.fit_predict(arr)
        persons_split = self._split_persons(arr, clusters)

        for _, person_shape in persons_split.items():
            preprocessed_shape = self.preprocessor.process_shape(person_shape)
            situation, probability = self.classifier.classify(preprocessed_shape)
            classified_persons.append((situation, person_shape, probability))

        self.system_state.update_persons(classified_persons)

    def _split_persons(self, arr, clusters):
        persons_split = {}
        for index, cluster in enumerate(clusters):
            if cluster not in persons_split:
                persons_split[cluster] = []
            persons_split[cluster].append(arr[index])
        return persons_split
