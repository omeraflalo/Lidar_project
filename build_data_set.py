from enum import Enum

from csv import writer

import keyboard

import mappedData
from fall_classifier import situation
from lidarUtills import measure_to_x_y



def on_key_press(key):
    match key.name:
        case 's':
            add_to_csv(situation.STAND)
        case 'f':
            add_to_csv(situation.FALL)
        case '=':
            add_to_csv(situation.STAND)
        case '-':
            add_to_csv(situation.FALL)


index = 0


def add_to_csv(classification):
    if len(mappedData.persons) <= 0:
        return

    shape = sorted(mappedData.persons.items())
    record = [classification]
    for angle, distance in shape:
        record.append(measure_to_x_y(angle, distance))

    with open('trainData/raw_data.csv', 'a') as data:
        writer_object = writer(data)
        writer_object.writerow(record)
        data.close()

    print(str(index) + ". " + str(classification) + " Record added")
