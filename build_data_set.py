from enum import Enum

from pynput.keyboard import Listener
from csv import writer

import main
from lidarUtills import measure_to_x_y


class situation(Enum):
    STAND = "Stand",
    FALL = "Fall"


def on_press(key):
    print(f"{key} pressed")
    if key == 's':
        add_to_csv(situation.STAND)
    elif key == 'f':
        add_to_csv(situation.FALL)


def add_to_csv(classification):
    if len(main.persons) <= 0:
        return

    shape = sorted(main.persons.items())
    record = [classification]
    for angle, distance in shape:
        record.append(measure_to_x_y(angle, distance))

    with open('trainData/raw_data.csv', 'a') as data:
        writer_object = writer(data)
        writer_object.writerow(record)
        data.close()


def listen_keys():
    with Listener(on_press=on_press) as listener:
        listener.join()
