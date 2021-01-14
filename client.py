import json
import socket

import pygame
import pygame_gui


pygame.init()
s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 5555

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


def game_window(data):
    create_game_button.hide()
    join_game_button.hide()
    joining_game_id_input.hide()

    pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (100, 50)),
        text=str(data['game_id']), manager=manager)


def main():
    clock = pygame.time.Clock()
    is_running = True

    s_client.connect((host, int(port)))

    try:
        data = s_client.recv(4096).decode()
        print(data)
    except socket.error as e:
        print(e)

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == create_game_button:
                        s_client.send(str.encode(json.dumps({'msg': 'create'})))
                        data = s_client.recv(4096).decode()
                        data = json.loads(data)
                        if data['msg'] == 'new game created':
                            print(f"Got the new id: {data['game_id']}")
                            pygame_gui.elements.UIButton(
                                relative_rect=pygame.Rect((10, 10), (100, 50)),
                                text=str(data['game_id']), manager=manager)
                    if event.ui_element == join_game_button:
                        game_id = joining_game_id_input.get_text()
                        s_client.send(str.encode(json.dumps({'msg': 'join', 'game_id': game_id})))

            manager.process_events(event)
        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


while True:
    main()
