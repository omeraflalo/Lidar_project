import time
from enum import Enum

import joblib
import numpy as np
from sklearn.cluster import DBSCAN

import mappedData


class Situation(Enum):
    STAND = "Stand"
    FALL = "Fall"


def _preprocess_shapes(shape):
    max_length = 100  # TODO: load from model. version 1 = 99
    if len(shape) > max_length:
        shape = shape[:max_length]
    x_y_shape = shape

    # Convert to numpy array for processing
    x_y_shape = np.array(x_y_shape)

    # Normalization
    min_val = np.min(x_y_shape, axis=0)
    max_val = np.max(x_y_shape, axis=0)
    norm_shape = x_y_shape - min_val
    if np.any(max_val != 0):  # Check if max value is not zero
        norm_shape /= max_val
    else:
        norm_shape = np.zeros_like(x_y_shape)  # or handle it differently

    # Padding
    pad_length = max_length - len(norm_shape)
    padded_shape = np.pad(norm_shape, ((0, pad_length), (0, 0)), mode='constant')

    return padded_shape


def _flatten_shapes(shape):
    return shape.flatten()


def classify(person_shape):
    pre = _preprocess_shapes(person_shape)
    flat = _flatten_shapes(pre)

    # Reshape for a single sample
    flat = flat.reshape(1, -1)

    # Scale the test data
    flat = scaler.transform(flat)

    if classifier.predict(flat) == Situation.FALL.value:
        # Get probability estimates for each class
        probabilities = classifier.predict_proba(flat)[0]

        # Identify the index of the "Fall" class
        fall_index = list(classifier.classes_).index(Situation.FALL.value)
        fall_probability = probabilities[fall_index]

        # Check if the probability for "Fall" is above the threshold
        if fall_probability > 0.75:
            return Situation.FALL
        else:
            return Situation.STAND
    else:
        return Situation.STAND


def update_classification():
    classified_persons = []
    if len(mappedData.lidar_diff) > 0:
        arr = np.array([coordinates for angle, (distance, coordinates) in mappedData.lidar_diff.items()])
        clusters = dbscan.fit_predict(arr)
        persons_split = {}
        for person_index, cluster in enumerate(clusters):
            if cluster not in persons_split:
                persons_split[cluster] = []
            persons_split[cluster].append(arr[person_index])

        for cluster, person in persons_split.items():
            classified_persons.append((classify(person), person))

        # arr = np.array([coordinates for angle, (distance, coordinates) in mappedData.lidar_diff.items()])
        #
        # classified_persons.append((classify(arr), arr))
    mappedData.persons = classified_persons


def classify_iteration(fps=25):
    last_classify = None
    interval = 1 / fps
    while True:
        start_time = time.time()

        if last_classify != mappedData.lidar_diff:
            last_classify = mappedData.lidar_diff
            update_classification()

        elapsed_time = time.time() - start_time
        time_to_wait = interval - elapsed_time
        if time_to_wait > 0:
            time.sleep(time_to_wait)


version = "3"
classifier_name = "extra_trees"
scaler = joblib.load('models/version ' + version + '/scaler.pkl')
classifier = joblib.load('models/version ' + version + '/' + classifier_name + '_model.pkl')
# `eps` is the maximum distance between two samples for them to be considered in the same neighborhood
dbscan = DBSCAN(eps=550, min_samples=1)
