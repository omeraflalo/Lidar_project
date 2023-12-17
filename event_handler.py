import keyboard
from build_data_set import DataSetBuilder, on_key_press
from data_visualizer import DataVisualizer
from fall_classifier import Situation


class EventHandler:
    def __init__(self, data_visualizer: DataVisualizer, data_set_builder: DataSetBuilder):
        self.data_visualizer = data_visualizer
        self.data_set_builder = data_set_builder

    def start_handling(self):
        keyboard.on_press(lambda key: on_key_press(key, self.data_set_builder))

    def _on_key_press(self, key):
        try:
            key_name = key.name
        except AttributeError:
            # Handle special keys here if needed
            return

        if key_name == 's' or key_name == '=':
            self.data_set_builder.add_to_csv(Situation.STAND)
        elif key_name == 'f' or key_name == '-':
            self.data_set_builder.add_to_csv(Situation.FALL)
        elif key_name == 'q':
            self._quit()

    def _quit(self):
        self.data_visualizer.stop_visualization()
        print("Application closing...")
        exit()
