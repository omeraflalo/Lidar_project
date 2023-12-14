import tkinter
import numpy as np
import threading
import time


class Plotter:
    def __init__(self):
        self.root = tkinter.Tk()
        self.room = {}
        self.canvas = tkinter.Canvas(self.root, bg="black", height=600, width=600)
        self.canvas.pack()
        self.radius = 3
        self.color = "red"
        self.zoom = 1 / 10
        self.x_correction = 300
        self.y_correction = 300

    def start(self):
        self.loop()

    def loop(self):
        self.draw_room()
        self.root.after(round(1000 / 60), self.loop)  # Schedule the next loop

    def draw_room(self):
        self.canvas.delete("all")  # Clear the canvas
        for angle, dist in self.room.items():
            x, y = self.measure_to_x_y(angle, dist)
            self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill=self.color,
                                    outline=self.color)

    def measure_to_x_y(self, angle, dist):
        angle = np.deg2rad(angle)
        y = dist * np.sin(angle) * self.zoom
        x = dist * np.cos(angle) * self.zoom
        return x + self.x_correction, y + self.y_correction

    def set_room(self, room):
        self.room = room


def update_room(plotter, new_room):
    plotter.set_room(new_room)  # Place the update in the queue


plotter = Plotter()
plotter.start()


# Example of updating the room from another thread
def worker_thread(plotter):
    while True:
        update_room(plotter, {45: 100, 90: 150})
        time.sleep(1 / 60)
        update_room(plotter, {25: 200, 50: 30, 70: 50})
        time.sleep(1 / 60)


threading.Thread(target=worker_thread, args=(plotter,)).start()

# Start the Tkinter event loop
plotter.root.mainloop()
