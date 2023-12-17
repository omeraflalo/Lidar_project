import json
from csv import writer
from fall_classifier import Situation


class DataSetBuilder:
    def __init__(self, system_state, file_path, version="3"):
        self.system_state = system_state
        self.file_path = f'models/version {version}/raw_data.csv'
        self.index = 1

    def add_to_csv(self, classification):
        if len(self.system_state.persons) != 1:
            print("Need to be only 1 person in the room")
            return

        shape = self.system_state.persons[0][1]
        record = [classification.value, json.dumps([coord.tolist() for coord in shape])]
        self._write_record(record)
        print(f"{self.index}. {classification} Record added")
        self.index += 1

    def _write_record(self, record):
        with open(self.file_path, 'a', newline='') as data:
            writer_object = writer(data, delimiter=';')
            writer_object.writerow(record)


def on_key_press(key, data_set_builder):
    try:
        key_name = key.name
    except AttributeError:
        return

    if key_name in ['s', '=']:
        data_set_builder.add_to_csv(Situation.STAND)
    elif key_name in ['f', '-']:
        data_set_builder.add_to_csv(Situation.FALL)
