from enum import Enum

import joblib
import numpy as np

from lidarUtills import measure_to_x_y

class situation(Enum):
    STAND = "Stand",
    FALL = "Fall"


def _preprocess_shapes(shape):
    x_y_shape = []
    for angle, distance in shape.items():
        x_y_shape.append(measure_to_x_y(int(angle), distance))

    max_length = 99

    # Convert to numpy array for processing
    x_y_shape = np.array(x_y_shape)

    # Normalization
    norm_shape = x_y_shape - np.min(x_y_shape, axis=0)
    norm_shape /= np.max(norm_shape, axis=0)

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

    return knn.predict(flat)


scaler = joblib.load('scaler.pkl')
knn = joblib.load("knn_model.pkl")

