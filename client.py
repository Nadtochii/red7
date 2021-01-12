import pygame
import pygame_gui

from game import join_game, create_game


pygame.init()

pygame.display.set_caption("Red7")
window_width, window_height = 800, 600
window_surface = pygame.display.set_mode((window_width, window_height))

white = (255, 255, 255)

background = pygame.Surface((window_width, window_height))
background.fill(pygame.Color(white))

manager = pygame_gui.UIManager((window_width, window_height))
create_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 275), (100, 50)),
                                                  text='Create', manager=manager)
join_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 275), (100, 50)),
                                                text='Join', manager=manager)


def main():
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == create_game_button:
                        res = create_game()
                        print(res)
                    if event.ui_element == join_game_button:
                        res = join_game()
                        print(res)
            manager.process_events(event)
        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


main()
