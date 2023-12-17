class SystemState:
    def __init__(self):
        self.room = {}
        self.persons = []
        self.lidar_diff = {}
        self.classify_fps = 0
        self.fps_history = []
        self.fps_history_size = 30

    def update_room(self, room_data):
        self.room = room_data

    def update_persons(self, persons_data):
        self.persons = persons_data

    def update_lidar_diff(self, lidar_diff_data):
        self.lidar_diff = lidar_diff_data

    def update_classify_fps(self, fps):
        self.classify_fps = fps
