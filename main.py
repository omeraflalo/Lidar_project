import sys
import threading

import joblib
import keyboard
import numpy as np
from rplidar import RPLidar
from sklearn.cluster import DBSCAN

import mappedData
from fall_classifier import classify, update_classification, classify_iteration
from lidarUtills import measure_to_x_y
from plot_gamer import PygamePlotter
import build_data_set
from mappedData import room
from shapely.geometry import Point, Polygon

lidar = None

try:
    lidar = RPLidar('COM9', baudrate=256000)
except:
    print("lidar does not connected")
    exit()
lidar._motor_speed = 600


def initialize_room(max_iteration=15):
    lidar.iter_measures()
    for i, scan in enumerate(lidar.iter_scans()):
        for res, angle, distance in scan:
            if res == 15:
                room[round(angle)] = (distance, measure_to_x_y(angle, distance))
        print(str(int((i / 15) * 100)) + "%")
        if i >= max_iteration:
            break
    print("Room initialized")


def run():
    tolerance = 250
    room_polygon = Polygon(coordinates for angle, (distance, coordinates) in sorted(room.items()))

    for i, scan in enumerate(lidar.iter_scans(scan_type='express', max_buf_meas=False)):
        persons_in_scan = {}
        for res, angle, distance in scan:
            if res == 15:
                coordinates = measure_to_x_y(angle, distance)
                new_point = Point(coordinates)
                distance_to_room = room_polygon.boundary.distance(new_point)

                if room_polygon.contains(new_point) and distance_to_room > tolerance:
                    persons_in_scan[angle] = (distance, coordinates)
        mappedData.lidar_diff = persons_in_scan


def _exit():
    if lidar:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()


def main():
    try:
        initialize_room()
        run()
    except KeyboardInterrupt:
        _exit()


try:
    keyboard.on_press(build_data_set.on_key_press)
    threading.Thread(target=main).start()
    threading.Thread(target=classify_iteration).start()
    plotter = PygamePlotter()
    plotter.on_exit(_exit)
    plotter.run()
except:
    _exit()
