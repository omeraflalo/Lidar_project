import numpy as np


def measure_to_x_y(angle, dist):
    angle = np.deg2rad(angle)
    y = dist * np.sin(angle)
    x = dist * np.cos(angle)
    return x, y
