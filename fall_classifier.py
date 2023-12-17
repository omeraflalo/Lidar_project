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
    probabilities = classifier.predict_proba(flat)[0]

    # Identify the index of the "Fall" class
    stand_index = list(classifier.classes_).index(Situation.STAND.value)
    fall_index = list(classifier.classes_).index(Situation.FALL.value)
    stand_probability = probabilities[stand_index]
    fall_probability = probabilities[fall_index]

    # Check if the probability for "Fall" is above the threshold
    if fall_probability > 0.75:
        return Situation.FALL, fall_probability
    else:
        return Situation.STAND, stand_probability


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
            situation, probability = classify(person)
            classified_persons.append((situation, person, probability))

    mappedData.persons = classified_persons


mappedData.classify_fps = 0
fps_history = []  # Store recent FPS values
fps_history_size = 10  # Determine how many recent values to consider

def classify_iteration(fps=25):
    last_classify = None
    interval = 1 / fps
    while True:
        start_time = time.time()

        if last_classify != mappedData.lidar_diff:
            last_classify = mappedData.lidar_diff
            update_classification()

        elapsed_time = time.time() - start_time
        actual_fps = 1 / elapsed_time if elapsed_time > 0 else 0
        fps_history.append(actual_fps)
        if len(fps_history) > fps_history_size:
            fps_history.pop(0)
        average_fps = sum(fps_history) / len(fps_history)

        mappedData.classify_fps = average_fps

        time_to_wait = interval - elapsed_time
        if time_to_wait > 0:
            time.sleep(time_to_wait)


version = "3"
classifier_name = "extra_trees"
scaler = joblib.load('models/version ' + version + '/scaler.pkl')
classifier = joblib.load('models/version ' + version + '/' + classifier_name + '_model.pkl')
# `eps` is the maximum distance between two samples for them to be considered in the same neighborhood
dbscan = DBSCAN(eps=550, min_samples=1)
