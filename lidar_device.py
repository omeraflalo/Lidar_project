from rplidar import RPLidar


class LidarDevice:
    def __init__(self, port, baudrate=256000):
        self.port = port
        self.baudrate = baudrate
        self.lidar = None
        self.connected = False

    def connect(self):
        try:
            self.lidar = RPLidar(self.port, self.baudrate)
            self.lidar._motor_speed = 600
            self.connected = True
            print("LIDAR connected.")
        except Exception as e:
            print(f"Failed to connect to LIDAR: {e}")
            self.connected = False

    def disconnect(self):
        if self.lidar and self.connected:
            self.lidar.stop()
            self.lidar.stop_motor()
            self.lidar.disconnect()
            self.connected = False
            print("LIDAR disconnected.")

    def is_connected(self):
        return self.connected

    def get_scans(self, scan_type='normal', max_buf_meas=False):
        if not self.is_connected():
            raise ConnectionError("LIDAR is not connected.")
        return self.lidar.iter_scans(scan_type=scan_type, max_buf_meas=max_buf_meas)
