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
        self.games = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((100, 30), (200, 500)),
                                                         item_list=[], manager=self.application.manager)
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
            self.application.open_screen(LobbyScreen, data['players'], data['game_id'])
        if msg == 'full room':
            pygame_gui.windows.UIMessageWindow(rect=pygame.Rect((300, 300), (200, 50)),
                                               html_message='This room is full. Please, choose another one.',
                                               manager=self.application.manager)


class LobbyScreen(ScreenBase):
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
                    self.application.network.send({'msg': 'drop', 'game_id': self.game_id})
                    self.application.open_screen(StartScreen)
                if event.ui_element == self.start_btn:
                    pass

    def process_network_message(self, data):
        msg = data['msg']
        if msg == 'new player':
            p = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (100, 50)),
                                         text=str(data['new_player']), manager=self.application.manager)
            self.x += 150
            self.players[data['new_player']] = p
        if msg == 'drop':
            drop_player = self.players[data['player']]
            drop_player.kill()
