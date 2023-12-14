import sys
import threading

from rplidar import RPLidar

import mappedData
from plot_gamer import PygamePlotter
# from build_data_set import listen_keys
from mappedData import room
lidar = None
try:
    lidar = RPLidar('COM9', baudrate=256000)
except:
    print("lidar does not connected")
    exit()
lidar._motor_speed = 600


def initialize_room(deg_amount=250):
    lidar.iter_measures()
    for i, scan in enumerate(lidar.iter_scans()):
        for measure in scan:
            room[round(measure[1])] = measure[2]
        print(str(int((len(room) / deg_amount) * 100)) + "%")
        if len(room) > deg_amount:
            break
    print("Room initialized")


def run():
    tolerance = 300

    for i, scan in enumerate(lidar.iter_scans()):
        person_in_scan = {}
        for res, angle, distance in scan:
            angle = int(angle)

            if angle not in room:
                room[angle] = distance
            if distance + tolerance < room[angle]:
                person_in_scan[angle] = distance
            else:
                room[angle] = distance

        mappedData.persons = person_in_scan


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
    # threading.Thread(target=listen_keys).start()
    plotter = PygamePlotter()
    threading.Thread(target=main).start()
    plotter.on_exit(_exit)
    plotter.run()
except:
    _exit()
