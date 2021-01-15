import json

import pygame
import pygame_gui

from network import Network

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
joining_game_id_input = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
    relative_rect=pygame.Rect((450, 240), (100, 50)), manager=manager)

x, y = 10, 10


def game_window(player):
    global x, y
    create_game_button.hide()
    join_game_button.hide()
    joining_game_id_input.hide()

    pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((x, y), (100, 50)),
        text=str(player), manager=manager)
    x += 150
    y += 150


def main():
    clock = pygame.time.Clock()
    is_running = True

    n = Network()

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == create_game_button:
                        n.send({'msg': 'create'})
                    if event.ui_element == join_game_button:
                        game_id = joining_game_id_input.get_text()
                        n.send({'msg': 'join', 'game_id': game_id})

            try:
                data = n.receive()
            except Exception as e:
                pass
            else:
                if data['msg'] == 'new game created':
                    print('new game', data)
                    game_window(data['player_id'])
                if data['msg'] == 'join':
                    print('join', data)
                    for p in data['players']:
                        game_window(p)
                if data['msg'] == 'join to game':
                    print('join to game', data)
                    game_window(data['new_player'])

            manager.process_events(event)
        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


main()
