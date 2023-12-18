import numpy as np
import json


class DataPreprocessor:
    def __init__(self, max_length=100):
        self.max_length = max_length

    def preprocess(self, shapes):
        x_y_shapes = [np.array(json.loads(shape)) for shape in shapes]
        self.max_length = max(len(shape) for shape in x_y_shapes)
        return np.array([self.process_shape(shape) for shape in x_y_shapes])

    def process_shape(self, shape):
        shape = shape[:self.max_length] if len(shape) > self.max_length else shape
        shape = np.array(shape)
        shape = self._normalize(shape)
        return self._pad(shape).flatten()

    def _normalize(self, shape):
        min_val, max_val = np.min(shape, axis=0), np.max(shape, axis=0)
        norm_shape = (shape - min_val) / max_val if np.any(max_val != 0) else np.zeros_like(shape)
        return norm_shape

    def _pad(self, shape):
        pad_length = self.max_length - len(shape)
        return np.pad(shape, ((0, pad_length), (0, 0)), mode='constant')
