import numpy as np
import tensorflow as tf
from keras import layers, models
from sklearn.model_selection import train_test_split


# Example data: list of shapes with their x,y coordinates
shapes = [
    np.array([[0, 0], [1, 0], [0.5, 0.866]], dtype=np.float64),  # Triangle
    np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float64), # Square
    np.array([[0, 1], [0.951, 0.309], [0.588, -0.809], [-0.588, -0.809], [-0.951, 0.309]], dtype=np.float64) # Pentagon
]

# Labels for the shapes (e.g., 0 for Triangle, 1 for Square, 2 for Pentagon)
labels = np.array([0, 1, 2])

# Normalizing and padding the shapes
def preprocess_shapes(shapes):
    max_length = max(len(shape) for shape in shapes)
    processed_shapes = []

    for shape in shapes:
        # Normalization (example: scale between 0 and 1)
        norm_shape = shape - np.min(shape, axis=0)
        norm_shape /= np.max(norm_shape, axis=0)

        # Padding
        pad_length = max_length - len(norm_shape)
        padded_shape = np.pad(norm_shape, ((0, pad_length), (0, 0)), mode='constant')

        processed_shapes.append(padded_shape)

    return np.array(processed_shapes)

preprocessed_shapes = preprocess_shapes(shapes)
