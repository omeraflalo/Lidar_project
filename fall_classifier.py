from enum import Enum

import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from lidarUtills import measure_to_x_y


class situation(Enum):
    STAND = "Stand"
    FALL = "Fall"


def _preprocess_shapes(shape):
    x_y_shape = [coordinates for angle, (distance, coordinates) in shape.items()]

    max_length = 104  # TODO: load from model. version 1 = 99

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


def classify_obj(person_shape):
    pro = _preprocess_shapes(person_shape)
    flat = _flatten_shapes(pro)

    # Reshape for a single sample
    flat = flat.reshape(1, -1)

    # Scale the test data
    flat = scaler.transform(flat)

    # return knn.predict(flat)
    # Get probability estimates for each class
    probabilities = knn.predict_proba(flat)[0]

    # Identify the index of the "Fall" class
    fall_index = list(knn.classes_).index(situation.FALL.value)
    fall_probability = probabilities[fall_index]

    # Check if the probability for "Fall" is above the threshold
    if fall_probability >= 0.7:
        return situation.FALL
    else:
        return situation.STAND


version = "2"
scaler = joblib.load('models/version ' + version + '/scaler.pkl')
knn: KNeighborsClassifier = joblib.load('models/version ' + version + '/knn_model.pkl')
