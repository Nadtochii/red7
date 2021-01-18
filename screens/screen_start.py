import pygame
import pygame_gui

from . import screen_base
from . import screen_lobby


class ScreenStart(screen_base.ScreenBase):

    games = None
    create_btn = None
    join_btn = None

    def __init__(self, application, game_ids=None):
        self.game_ids = game_ids or []
        super().__init__(application)

    def enter_screen(self):
        self.games = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((100, 30), (200, 500)),
                                                         item_list=self.game_ids, manager=self.application.manager)
        self.create_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 30), (100, 50)), text='Create',
                                                       manager=self.application.manager)
        self.join_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 100), (100, 50)), text='Join',
                                                     manager=self.application.manager)

    def exit_screen(self):
        self.games.kill()
        self.create_btn.kill()
        self.join_btn.kill()

    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.create_btn:
                    self.application.network.send({'type': 'create_game', 'body': ''})
                if event.ui_element == self.join_btn:
                    game_id = self.games.get_single_selection()
                    self.application.network.send({'type': 'join_game', 'body': {'game_id': game_id}})

    def process_network_message(self, data):
        msg = data['msg']
        if msg == 'lobby':
            games = [str(g) for g in data['game_ids']]
            self.games.set_item_list(games)
        if msg == 'join':
            self.application.open_screen(screen_lobby.ScreenLobby, data['players'], data['game_id'])
        if msg == 'full room':
            pygame_gui.windows.UIMessageWindow(rect=pygame.Rect((300, 300), (200, 50)),
                                               html_message='This room is full. Please, choose another one.',
                                               manager=self.application.manager)

