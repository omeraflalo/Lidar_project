import threading

import pygame
import pygame.freetype
from fall_classifier import Situation


class DataVisualizer:
    def __init__(self, room_monitor, system_state):
        self.room_monitor = room_monitor
        self.system_state = system_state
        self.screen_size = (1000, 600)
        self.radius = 2
        self.zoom = 1 / 15
        self.correction_x = 400
        self.correction_y = 300
        self.show_initialization_progress = True
        self.running = True
        pygame.init()
        self.font = pygame.freetype.SysFont("Arial", 20)
        self.progress_font = pygame.freetype.SysFont("Arial", 30)
        button_width, button_height = 100, 40
        padding = 10  # Padding from the top and right edges
        self.button_rect = pygame.Rect(self.screen_size[0] - button_width - padding, padding, button_width,
                                       button_height)

        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Room Plotter')
        self.clock = pygame.time.Clock()

    def start_visualization(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_visualization()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_button_clicked(event.pos):
                        self.show_initialization_progress = True
                        threading.Thread(target=self.room_monitor.initialize_room).start()

            self.draw()

            pygame.display.flip()
            self.clock.tick(25)

    def stop_visualization(self):
        self.running = False
        pygame.quit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.room_monitor.initialization_progress < 100:
            self.draw_initialization_progress()
        else:
            self.show_initialization_progress = False
            self.draw_room()
            self.draw_persons()
        self.draw_fps()
        self.draw_button()

    def draw_room(self):
        if not self.room_monitor.room_polygon:
            return

        room_points = [(x * self.zoom + self.correction_x, y * self.zoom + self.correction_y)
                       for x, y in self.room_monitor.room_polygon.exterior.coords]

        pygame.draw.polygon(self.screen, "grey", room_points, 1)

    def update_min_max(self, x, y, min_max):
        min_max[0] = min(x, min_max[0])
        min_max[1] = min(y, min_max[1])
        min_max[2] = max(x, min_max[2])
        min_max[3] = max(y, min_max[3])
        return min_max

    def draw_persons(self):
        for person in self.system_state.persons:
            situation, person_coordinates, probability = person
            min_max = [float('inf'), float('inf'), float('-inf'), float('-inf')]

            for x, y in person_coordinates:
                screen_x, screen_y = x * self.zoom + self.correction_x, y * self.zoom + self.correction_y
                pygame.draw.circle(self.screen, "blue", (int(screen_x), int(screen_y)), 4)
                min_max = self.update_min_max(int(screen_x), int(screen_y), min_max)

            self.display_classification(situation, min_max, probability)

    def display_classification(self, situation, min_max, probability):
        color = "green" if situation == Situation.STAND else "red"
        rect_padding = 15
        rect = pygame.Rect(
            min_max[0] - rect_padding, min_max[1] - rect_padding,
            min_max[2] - min_max[0] + rect_padding * 2,
            min_max[3] - min_max[1] + rect_padding * 2
        )
        pygame.draw.rect(self.screen, color, rect, 2)

        prob_text = f"{probability * 100:.0f}%"
        text_rect = rect.move(0, -20)
        self.font.render_to(self.screen, (text_rect.left, text_rect.top), prob_text, color)

    def draw_fps(self):
        fps_text = f"FPS: {self.system_state.classify_fps:.2f}"
        self.font.render_to(self.screen, (10, 10), fps_text, (255, 255, 255))

    def draw_initialization_progress(self):
        if not self.show_initialization_progress:
            return

        progress_text = f"Initializing Room: {self.room_monitor.initialization_progress}%"
        text_surface, text_rect = self.progress_font.render(progress_text, (255, 255, 255))
        text_width, text_height = text_surface.get_size()
        x = (self.screen_size[0] - text_width) // 2
        y = (self.screen_size[1] - text_height) // 2
        self.screen.blit(text_surface, (x, y))

    def draw_button(self):
        pygame.draw.rect(self.screen, (20, 100, 200), self.button_rect)
        text_surface, _ = self.font.render("Reinitialize", (255, 255, 255))  # White text
        self.screen.blit(text_surface, (self.button_rect.x + 10, self.button_rect.y + 10))

    def is_button_clicked(self, pos):
        return self.button_rect.collidepoint(pos)
