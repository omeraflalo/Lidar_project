import numpy as np


class LidarUtils:
    @staticmethod
    def measure_to_x_y(angle, distance):
        angle_rad = np.deg2rad(angle)
        x = distance * np.cos(angle_rad)
        y = distance * np.sin(angle_rad)
        return x, y
