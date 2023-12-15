import sys
import threading

import joblib
import keyboard
from rplidar import RPLidar

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


def initialize_room(deg_amount=260):
    lidar.iter_measures()
    for i, scan in enumerate(lidar.iter_scans()):
        for res, angle, distance in scan:
            if res == 15:
                room[round(angle)] = (distance, measure_to_x_y(angle, distance))
        print(str(int((i / 15) * 100)) + "%")
        if i >= 15:
            break
        # print(str(int((len(room) / deg_amount) * 100)) + "%")
        # if len(room) > deg_amount:
        #     break
    print("Room initialized")


def run():
    tolerance = 400
    room_polygon = Polygon(coordinates for angle, (distance, coordinates) in sorted(room.items()))

    for i, scan in enumerate(lidar.iter_scans()):
        person_in_scan = {}
        for res, angle, distance in scan:
            coordinates = measure_to_x_y(angle, distance)
            new_point = Point(coordinates)
            distance_to_room = room_polygon.boundary.distance(new_point)

            if room_polygon.contains(new_point) and distance_to_room > 250:
                if res == 15:
                    person_in_scan[angle] = (distance, coordinates)
            # else:
            # room[angle] = distance

            # if angle not in room:
            #     if not room_polygon.contains(new_point):
            #         room[angle] = distance
            #     elif distance_to_room > 90:
            #         person_in_scan[angle] = distance
            #     continue
            # if distance + tolerance < room[angle]:
            #     person_in_scan[angle] = distance
            #     print(distance_to_room)
            # else:
            #     room[angle] = distance
        mappedData.persons = person_in_scan
        if len(mappedData.persons) > 0:
            mappedData.person_state = classify_obj(mappedData.persons)
            # print(mappedData.person_state)
        else:
            mappedData.person_state = None


def _exit():
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
    plotter = PygamePlotter()
    threading.Thread(target=main).start()
    plotter.on_exit(_exit)
    plotter.run()
except:
    _exit()
