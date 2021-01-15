import pygame
import pygame_gui

from network import Network
from screen import StartScreen

pygame.init()

pygame.display.set_caption("Red7")
window_width, window_height = 800, 600
window_surface = pygame.display.set_mode((window_width, window_height))

white = (255, 255, 255)

background = pygame.Surface((window_width, window_height))
background.fill(pygame.Color(white))


class Application:

    current_screen = None
    startup_screen = StartScreen

    def __init__(self, window, manager, network):
        self.window = window
        self.manager = manager
        self.network = network

    def open_screen(self, screen_cls, *args, **kwargs):
        self.current_screen.exit_screen()
        self.current_screen = screen_cls(self, *args, **kwargs)
        self.current_screen.enter_screen()

    def run(self):
        clock = pygame.time.Clock()
        is_running = True

        self.current_screen = self.startup_screen(self)
        self.current_screen.enter_screen()

        while is_running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                self.current_screen.process_event(event)

                try:
                    data = self.network.receive()
                except Exception as e:
                    pass
                else:
                    self.current_screen.process_network_message(data)

                self.manager.process_events(event)
            self.manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            self.manager.draw_ui(window_surface)

            pygame.display.update()


def main():
    network = Network()
    manager = pygame_gui.UIManager((window_width, window_height))
    app = Application(window_surface, manager, network)
    app.run()


if __name__ == '__main__':
    main()
