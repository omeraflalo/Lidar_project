from csv import writer

import mappedData
from fall_classifier import Situation
from lidarUtills import measure_to_x_y


def on_key_press(key):
    match key.name:
        case 's':
            add_to_csv(Situation.STAND)
        case 'f':
            add_to_csv(Situation.FALL)
        case '=':
            add_to_csv(Situation.STAND)
        case '-':
            add_to_csv(Situation.FALL)


index = 0


def add_to_csv(classification):
    if len(mappedData.persons) <= 0:
        return

    shape = sorted(mappedData.persons.items())
    record = [classification.value]
    for angle, (distance, coordinates) in shape:
        record.append(measure_to_x_y(angle, distance))

    with open('models/version 2/raw_data.csv', 'a', newline='') as data:
        writer_object = writer(data)
        writer_object.writerow(record)
        data.close()

    print(str(index) + ". " + str(classification) + " Record added")
