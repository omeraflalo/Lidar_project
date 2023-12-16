import json
from csv import writer

import mappedData
from fall_classifier import Situation


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


index = {
    "i": 1
}


def add_to_csv(classification):
    if len(mappedData.persons) != 1:
        print("need to be only 1 person in the room")
        return
    shape = mappedData.persons[0][1]
    record = [classification.value, json.dumps([coord.tolist() for coord in shape])]
    version = "3"
    with open('models/version ' + version + '/raw_data.csv', 'a', newline='') as data:
        writer_object = writer(data, delimiter=';')
        writer_object.writerow(record)
        data.close()

    print(str(index["i"]) + ". " + str(classification) + " Record added")
    index["i"] += 1
