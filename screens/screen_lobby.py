import pygame
import pygame_gui

from . import screen_base
from . import screen_game
from . import screen_start


class ScreenLobby(screen_base.ScreenBase):
    x, y = 10, 10
    back_btn = None
    start_btn = None

    def __init__(self, application, players, game_id):
        self.players = {p: None for p in players}
        self.game_id = game_id
        super().__init__(application)

    def enter_screen(self):
        for p in self.players:
            p_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (100, 50)), text=str(p),
                                                 manager=self.application.manager)
            self.players[p] = p_btn
            self.x += 150
        self.back_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 500), (100, 50)), text='Back',
                                                     manager=self.application.manager)
        self.start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 500), (100, 50)), text='Start',
                                                      manager=self.application.manager)

    def exit_screen(self):
        self.start_btn.kill()
        self.back_btn.kill()
        for i in self.players.values():
            i.kill()

    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_btn:
                    self.application.network.send({'type': 'leave_game', 'body': {'game_id': self.game_id}})
                if event.ui_element == self.start_btn:
                    self.application.network.send({'type': 'start_game', 'body': {'players': list(self.players.keys()),
                                                   'game_id': self.game_id}})

    def process_network_message(self, data):
        msg = data['msg']
        if msg == 'new player':
            p = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (100, 50)),
                                             text=str(data['new_player']), manager=self.application.manager)
            self.x += 150
            self.players[data['new_player']] = p
        if msg == 'lobby':
            self.application.open_screen(screen_start.ScreenStart, data['game_ids'])
        if msg == 'drop':
            drop_player = self.players[data['player']]
            drop_player.kill()
        if msg == 'play':
            self.application.open_screen(screen_game.ScreenGame, data)
