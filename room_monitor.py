import time

from shapely.geometry import Point, Polygon
from lidar_utils import LidarUtils


class RoomMonitor:
    def __init__(self, lidar_device, system_state, classification_updater):
        self.lidar_device = lidar_device
        self.system_state = system_state
        self.classification_updater = classification_updater
        self.room_polygon = None
        self.tolerance = 250
        self.initialization_progress = 0

    def run(self):
        try:
            self.initialize_room()
            self.start_monitoring()
        except:
            print("Scan stopped.")

    def initialize_room(self, max_iteration=15):
        if not self.lidar_device.is_connected():
            print("LIDAR device is not connected. Cannot initialize room.")
            return

        print("Initializing room...")
        self.lidar_device.lidar.iter_measures()  # Prepare the device for measurements
        for i, scan in enumerate(self.lidar_device.get_scans()):
            for res, angle, distance in scan:
                if res == 15:
                    self.system_state.room[round(angle)] = (distance, LidarUtils.measure_to_x_y(angle, distance))
            self.initialization_progress = min(int((i / max_iteration) * 100), 100)
            if i >= max_iteration:
                break
        self._create_room_polygon()
        print("Room initialization complete.")

    def _create_room_polygon(self):
        coordinates = [LidarUtils.measure_to_x_y(angle, distance) for angle, (distance, _) in
                       sorted(self.system_state.room.items())]
        self.room_polygon = Polygon(coordinates)

    def start_monitoring(self):
        if not self.lidar_device.is_connected():
            print("LIDAR device is not connected. Cannot start monitoring.")
            return

        print("Starting room monitoring...")
        for scan in self.lidar_device.get_scans():
            start_time = time.time()
            persons_in_scan = self._process_scan(scan)
            self.system_state.lidar_diff = persons_in_scan
            self.classification_updater.update_classification()
            self.measure_fps(start_time)

    def measure_fps(self, start_time):
        elapsed_time = time.time() - start_time
        actual_fps = 1 / elapsed_time if elapsed_time > 0 else 0
        self.system_state.fps_history.append(actual_fps)
        if len(self.system_state.fps_history) > self.system_state.fps_history_size:
            self.system_state.fps_history.pop(0)
        self.system_state.classify_fps = sum(self.system_state.fps_history) / len(self.system_state.fps_history)

    def _process_scan(self, scan):
        persons_in_scan = {}
        for res, angle, distance in scan:
            if res == 15:
                coordinates = LidarUtils.measure_to_x_y(angle, distance)
                new_point = Point(coordinates)
                distance_to_room = self.room_polygon.boundary.distance(new_point)

                if self.room_polygon.contains(new_point) and distance_to_room > self.tolerance:
                    persons_in_scan[angle] = (distance, coordinates)
        return persons_in_scan
