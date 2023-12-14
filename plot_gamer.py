import pygame
from mappedData import room, persons

from lidarUtills import measure_to_x_y


class PygamePlotter:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Room Plotter')
        self.clock = pygame.time.Clock()
        self.persons_max = None
        self.persons_min = None
        self.radius = 2
        self.zoom = 1 / 10
        self.x_correction = 300
        self.y_correction = 300
        self.running = True
        self._exit_call = None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if self._exit_call is not None:
                        self._exit_call()

            self.draw()

            pygame.display.flip()
            self.clock.tick(25)

        pygame.quit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_room()
        self.draw_persons()

    def on_exit(self, exit_call):
        self._exit_call = exit_call

    def draw_room(self):
        arr = []
        for angle, dist in sorted(room.items()):
            x, y = self.measure_to_x_y(angle, dist)
            arr.append((x, y))
            pygame.draw.circle(self.screen, "red", (int(x), int(y)), self.radius)
        if len(arr) > 0:
            pygame.draw.lines(self.screen, "red", True, arr)
            # print(str(min(arr)) + " " + str(max(arr)))

    def update_min_max(self, x, y):
        if x < self.persons_min[0]:
            self.persons_min[0] = x
        if y < self.persons_min[1]:
            self.persons_min[1] = y
        if x > self.persons_max[0]:
            self.persons_max[0] = x
        if y > self.persons_max[1]:
            self.persons_max[1] = y

    def draw_persons(self):
        print(persons)
        person_items = persons.items()
        if len(person_items) > 0:
            firstItem = list(person_items)[0]
            firstItem_x_y = self.measure_to_x_y(firstItem[0], firstItem[1])
            self.persons_min = [firstItem_x_y[0], firstItem_x_y[1]]
            self.persons_max = [firstItem_x_y[0], firstItem_x_y[1]]
            for angle, dist in persons.items():
                x, y = self.measure_to_x_y(angle, dist)
                self.update_min_max(x, y)
                pygame.draw.circle(self.screen, "blue", (int(x), int(y)), 4)
            pygame.draw.rect(self.screen, "green", (
                self.persons_min[0], self.persons_min[1], self.persons_max[0] - self.persons_min[0],
                self.persons_max[1] - self.persons_min[1]), 2)

    def measure_to_x_y(self, angle, dist):
        x, y = measure_to_x_y(angle, dist)
        return x * self.zoom + self.x_correction, y * self.zoom + self.y_correction
