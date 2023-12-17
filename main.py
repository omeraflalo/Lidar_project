import sys
import threading

from system_state import SystemState
from build_data_set import DataSetBuilder
from lidar_device import LidarDevice
from room_monitor import RoomMonitor
from data_visualizer import DataVisualizer
from event_handler import EventHandler
from fall_classifier import DataPreprocessor, FallClassifier, ClassificationUpdater, Situation
from sklearn.cluster import DBSCAN


class Application:
    def __init__(self):
        self.system_state = SystemState()
        self.lidar_device = LidarDevice('COM9', baudrate=256000)
        preprocessor = DataPreprocessor(max_length=100)

        models_path = "models/version 3/"

        classifier = FallClassifier(model_path=models_path + 'random_forest_model.pkl',
                                    scaler_path=models_path + 'scaler.pkl',
                                    threshold=0.75)
        dbscan = DBSCAN(eps=550, min_samples=1)
        self.classification_updater = ClassificationUpdater(self.system_state, preprocessor, classifier, dbscan)
        self.room_monitor = RoomMonitor(self.lidar_device, self.system_state, self.classification_updater)
        self.data_visualizer = DataVisualizer(self.room_monitor, self.system_state)
        self.data_set_builder = DataSetBuilder(self.system_state, file_path=models_path)

        # When setting up event handlers, pass this instance
        self.event_handler = EventHandler(self.data_visualizer, self.data_set_builder)

    def run(self):
        try:
            self.lidar_device.connect()

            threading.Thread(target=self.room_monitor.run).start()
            threading.Thread(target=self.event_handler.start_handling).start()

            self.data_visualizer.start_visualization()

        except:
            self.close()

    def close(self):
        self.lidar_device.disconnect()
        self.data_visualizer.stop_visualization()
        sys.exit(0)


if __name__ == "__main__":
    app = Application()
    app.run()
