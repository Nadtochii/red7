import pygame
import pygame_gui


class ScreenBase:

    def __init__(self, application):
        self.application = application

    def enter_screen(self):
        pass

    def exit_screen(self):
        pass

    def process_event(self, event):
        pass

    def process_network_message(self, data):
        pass


class StartScreen(ScreenBase):

    games = None
    create_btn = None
    join_btn = None

    def enter_screen(self):
        self.games = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((100, 30), (200, 500)), item_list=[],
                                                         manager=self.application.manager)
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
                    self.application.network.send({'msg': 'create'})
                if event.ui_element == self.join_btn:
                    game_id = self.games.get_single_selection()
                    self.application.network.send({'msg': 'join', 'game_id': game_id})

    def process_network_message(self, data):
        msg = data['msg']
        if msg == 'lobby':
            games = [str(g) for g in data['game_ids']]
            self.games.set_item_list(games)
        if msg == 'join':
            self.application.open_screen(LobbyScreen, data['players'])


class LobbyScreen(ScreenBase):
    x, y = 10, 10

    def __init__(self, application, players):
        self.players = players
        super().__init__(application)

    def enter_screen(self):
        for p in self.players:
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (100, 50)), text=str(p),
                                         manager=self.application.manager)
            self.x += 150

    def process_network_message(self, data):
        msg = data['msg']
        if msg == 'new player':
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (100, 50)),
                                         text=str(data['new_player']), manager=self.application.manager)
            self.x += 150
