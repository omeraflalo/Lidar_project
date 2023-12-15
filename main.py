import sys
import threading

import joblib
import keyboard
import numpy as np
from rplidar import RPLidar
from sklearn.cluster import DBSCAN

import mappedData
from fall_classifier import classify_obj
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
lidar._motor_speed = 660


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


def run(dbscan):
    tolerance = 250
    room_polygon = Polygon(coordinates for angle, (distance, coordinates) in sorted(room.items()))

    for i, scan in enumerate(lidar.iter_scans()):
        person_in_scan = {}
        for res, angle, distance in scan:
            coordinates = measure_to_x_y(angle, distance)
            new_point = Point(coordinates)
            distance_to_room = room_polygon.boundary.distance(new_point)

            if room_polygon.contains(new_point) and distance_to_room > tolerance:
                if res == 15:
                    person_in_scan[angle] = (distance, coordinates)

        classified_persons = []
        if len(person_in_scan) > 0:
            arr = np.array([coordinates for angle, (distance, coordinates) in person_in_scan.items()])
            clusters = dbscan.fit_predict(arr)
            persons_split = {}
            for person_index, cluster in enumerate(clusters):
                if cluster not in persons_split:
                    persons_split[cluster] = []
                persons_split[cluster].append(arr[person_index])

            for cluster, person in persons_split.items():
                classified_persons.append((classify_obj(person), person))

        mappedData.persons = classified_persons


def _exit():
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


def main():
    try:
        # `eps` is the maximum distance between two samples for them to be considered in the same neighborhood
        dbscan = DBSCAN(eps=550, min_samples=1)
        initialize_room()
        run(dbscan)
    except KeyboardInterrupt:
        _exit()


try:
    keyboard.on_press(build_data_set.on_key_press)
    threading.Thread(target=main).start()
    plotter = PygamePlotter()
    plotter.on_exit(_exit)
    plotter.run()
except:
    _exit()
