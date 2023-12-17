import numpy as np
import json


class DataPreprocessor:
    def preprocess(self, shapes):
        x_y_shapes = [np.array(json.loads(shape)) for shape in shapes]
        max_length = max(len(shape) for shape in x_y_shapes)
        return np.array([self._process_shape(shape, max_length) for shape in x_y_shapes])

    def _process_shape(self, shape, max_length):
        # Normalization
        min_val = np.min(shape, axis=0)
        max_val = np.max(shape, axis=0)
        norm_shape = shape - min_val
        if np.any(max_val != 0):
            norm_shape /= max_val
        else:
            norm_shape = np.zeros_like(shape)

        # Padding
        pad_length = max_length - len(norm_shape)
        padded_shape = np.pad(norm_shape, ((0, pad_length), (0, 0)), mode='constant')

        return padded_shape.flatten()
