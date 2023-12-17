import pygame
import pygame.freetype

import mappedData
from fall_classifier import Situation, update_classification


class PygamePlotter:
    def __init__(self):
        pygame.init()
        self.screen_size = (1000, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Room Plotter')
        self.clock = pygame.time.Clock()
        self.radius = 2
        self.zoom = 1 / 15
        self.x_correction = 400
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
        if len(mappedData.room) > 0:
            sorted_room = sorted(mappedData.room.items())
            self.update_correction(sorted_room)
            self.draw_room(sorted_room)
        self.draw_persons()
        self.draw_fps()

    def on_exit(self, exit_call):
        self._exit_call = exit_call

    def update_correction(self, sorted_room):
        x_points = [x for angle, (distance, (x, y)) in sorted_room]
        y_points = [y for angle, (distance, (x, y)) in sorted_room]

        max_x = max(x_points)
        max_y = max(y_points)
        min_x = min(x_points)
        min_y = min(y_points)

        self.zoom = min(self.screen_size[0] / (max_x - min_x), self.screen_size[1] / (max_y - min_y))

        self.x_correction = - min_x
        self.y_correction = - min_y
        # TODO: check why that's not working properly
        # self.x_correction = (self.screen_size[0] - (max_x - min_x) * self.zoom) / 2
        # self.y_correction = (self.screen_size[1] - (max_y - min_y) * self.zoom) / 2

    def draw_room(self, sorted_room):
        arr = []
        for angle, (distance, coordinates) in sorted_room:
            x, y = self.measure_to_x_y(coordinates)
            arr.append((x, y))
            pygame.draw.circle(self.screen, "grey", (int(x), int(y)), self.radius)
        if len(arr) > 0:
            pygame.draw.lines(self.screen, "grey", True, arr)
            # print(str(min(arr)) + " " + str(max(arr)))

    def update_min_max(self, x, y, min_max):
        min_max[0] = min(x, min_max[0])
        min_max[1] = min(y, min_max[1])
        min_max[2] = max(x, min_max[2])
        min_max[3] = max(y, min_max[3])
        return min_max

    def draw_persons(self):
        font = pygame.freetype.SysFont("Arial", 20)  # Choose your font and size
        for person in mappedData.persons:
            situation, person_coordinates, probability = person
            min_max = [float('inf'), float('inf'), float('-inf'), float('-inf')]

            for coordinates in person_coordinates:
                x, y = self.measure_to_x_y(coordinates)
                min_max = self.update_min_max(x, y, min_max)
                pygame.draw.circle(self.screen, "blue", (int(x), int(y)), 4)

            rect_padding = 15
            rect_color = "green" if situation == Situation.STAND else "red"
            rect = pygame.Rect(
                min_max[0] - rect_padding, min_max[1] - rect_padding,
                min_max[2] - min_max[0] + rect_padding * 2,
                min_max[3] - min_max[1] + rect_padding * 2
            )
            pygame.draw.rect(self.screen, rect_color, rect, 2)

            # Render the probability text
            prob_text = f"{probability * 100:.0f}%"  # Format the probability to 2 decimal places
            text_rect = rect.move(0, -20)  # Adjust the position as needed
            font.render_to(self.screen, (text_rect.left, text_rect.top), prob_text, "white")

    def draw_fps(self):
        font = pygame.freetype.SysFont("Arial", 35)
        fps_text = f"FPS: {mappedData.classify_fps:.8f}"
        font.render_to(self.screen, (10, 10), fps_text, (255, 255, 255))  # Renders the text in white color

    def measure_to_x_y(self, coordinates):
        x, y = coordinates
        return (x + self.x_correction) * self.zoom, (y + self.y_correction) * self.zoom
