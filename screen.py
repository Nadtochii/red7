# import pygame
# import pygame_gui
#
#
# class ScreenBase:
#
#     def __init__(self, application):
#         self.application = application
#
#     def enter_screen(self):
#         pass
#
#     def exit_screen(self):
#         pass
#
#     def process_event(self, event):
#         pass
#
#     def process_network_message(self, data):
#         pass
#
#
# class StartScreen(ScreenBase):
#
#     games = None
#     create_btn = None
#     join_btn = None
#
#     def __init__(self, application, game_ids=None):
#         self.game_ids = game_ids or []
#         super().__init__(application)
#
#     def enter_screen(self):
#         self.games = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((100, 30), (200, 500)),
#                                                          item_list=self.game_ids, manager=self.application.manager)
#         self.create_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 30), (100, 50)), text='Create',
#                                                        manager=self.application.manager)
#         self.join_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 100), (100, 50)), text='Join',
#                                                      manager=self.application.manager)
#
#     def exit_screen(self):
#         self.games.kill()
#         self.create_btn.kill()
#         self.join_btn.kill()
#
#     def process_event(self, event):
#         if event.type == pygame.USEREVENT:
#             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
#                 if event.ui_element == self.create_btn:
#                     self.application.network.send({'type': 'create_game', 'body': ''})
#                 if event.ui_element == self.join_btn:
#                     game_id = self.games.get_single_selection()
#                     self.application.network.send({'type': 'join_game', 'body': {'game_id': game_id}})
#
#     def process_network_message(self, data):
#         msg = data['msg']
#         if msg == 'lobby':
#             games = [str(g) for g in data['game_ids']]
#             self.games.set_item_list(games)
#         if msg == 'join':
#             self.application.open_screen(LobbyScreen, data['players'], data['game_id'])
#         if msg == 'full room':
#             pygame_gui.windows.UIMessageWindow(rect=pygame.Rect((300, 300), (200, 50)),
#                                                html_message='This room is full. Please, choose another one.',
#                                                manager=self.application.manager)
#
#
# class LobbyScreen(ScreenBase):
#     x, y = 10, 10
#     back_btn = None
#     start_btn = None
#
#     def __init__(self, application, players, game_id):
#         self.players = {p: None for p in players}
#         self.game_id = game_id
#         super().__init__(application)
#
#     def enter_screen(self):
#         for p in self.players:
#             p_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (100, 50)), text=str(p),
#                                                  manager=self.application.manager)
#             self.players[p] = p_btn
#             self.x += 150
#         self.back_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 500), (100, 50)), text='Back',
#                                                      manager=self.application.manager)
#         self.start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 500), (100, 50)), text='Start',
#                                                       manager=self.application.manager)
#
#     def exit_screen(self):
#         self.start_btn.kill()
#         self.back_btn.kill()
#         for i in self.players.values():
#             i.kill()
#
#     def process_event(self, event):
#         if event.type == pygame.USEREVENT:
#             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
#                 if event.ui_element == self.back_btn:
#                     self.application.network.send({'type': 'leave_game', 'body': {'game_id': self.game_id}})
#                 if event.ui_element == self.start_btn:
#                     self.application.network.send({'type': 'start_game', 'body': {'players': list(self.players.keys()),
#                                                    'game_id': self.game_id}})
#
#     def process_network_message(self, data):
#         msg = data['msg']
#         if msg == 'new player':
#             p = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (100, 50)),
#                                              text=str(data['new_player']), manager=self.application.manager)
#             self.x += 150
#             self.players[data['new_player']] = p
#         if msg == 'lobby':
#             self.application.open_screen(StartScreen, data['game_ids'])
#         if msg == 'drop':
#             drop_player = self.players[data['player']]
#             drop_player.kill()
#
#         if msg == 'play':
#             self.application.open_screen(GameScreen, data)
#
#
# class GameScreen(ScreenBase):
#     go_btn = None
#     pass_btn = None
#     canvas = None
#     opponents = None
#     players_objects = dict()
#     to_canvas = True
#     to_palette = True
#     to_canvas_btn = None
#     to_palette_btn = None
#     action_data = {
#         'to_canvas': {'color': None, 'number': None},
#         'to_palette': {'color': None, 'number': None},
#     }
#     chosen_card = None
#
#     def __init__(self, application, data):
#         self.players_info = data['players_info']
#         self.game_id = data['game_id']
#         self.current_player_id = data['current_player_id']
#         self.active_player = data['active_player']
#         super().__init__(application)
#
#     def enter_screen(self):
#         self.canvas = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((350, 200), (100, 200)),
#                                                     html_text='start card', manager=self.application.manager)
#         self.go_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 400), (100, 50)),
#                                                    text='Go', manager=self.application.manager)
#         self.pass_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 500), (100, 50)),
#                                                    text='Lose', manager=self.application.manager)
#         self.go_btn.disable()
#         self.pass_btn.disable()
#
#         for player in self.players_info:
#             player_id = player['player_id']
#             self.players_objects[player_id] = {}
#             if player_id == self.current_player_id:
#                 self.players_objects[player_id]['hand'] = []
#                 x, y = 100, 400
#                 for card in player['hand']:
#                     card_info = str(card['number']) + ' ' + str(card['color'])
#                     c = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((x, y), (50, 100)),
#                                                       html_text=card_info, manager=self.application.manager)
#                     # to_palette = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y + 110), (50, 25)),
#                     #                                           text='To palette', manager=self.application.manager)
#                     # to_canvas = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x + 25, y + 110), (50, 25)),
#                     #                                          text='To canvas', manager=self.application.manager)
#                     # self.players_objects[player_id]['hand'].append({'card': c, 'to_palette': to_palette, 'to_canvas': to_canvas})
#                     self.players_objects[player_id]['hand'].append(c)
#
#                     x, y = x + 60, y
#             else:
#                 x, y = 10, 10
#                 pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((x, y), (100, 100)), html_text='111', manager=self.application.manager)
#
#         if self.active_player == self.current_player_id:
#             self.go_btn.enable()
#             self.pass_btn.enable()
#
#     def exit_screen(self):
#         pass
#
#     def process_event(self, event):
#         if event.type == pygame.USEREVENT:
#             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
#                 if event.ui_element in self.players_objects[self.current_player_id]['hand']:
#                     self.chosen_card = event.ui_element
#                     pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect((400, 400), (200, 200)),
#                                                                             action_long_desc='Action',
#                                                                             object_id='action_window',
#                                                                             manager=self.application.manager)
#                     if self.to_canvas:
#                         self.to_canvas_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (100, 50)),
#                                                                      text='To Canvas',
#                                                                      object_id='to_canvas',
#                                                                      manager=self.application.manager)
#                     if self.to_palette:
#                         self.to_palette_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 50), (100, 50)),
#                                                                       text='To Palette',
#                                                                       object_id='to_palette',
#                                                                       manager=self.application.manager)
#
#                 if event.ui_element == self.to_canvas_btn:
#                     number, color = self.chosen_card.html_text.split(' ')
#                     self.action_data['to_canvas']['number'] = number
#                     self.action_data['to_canvas']['color'] = color
#                     self.to_canvas = False
#
#                 if event.ui_element == self.to_palette_btn:
#                     number, color = self.chosen_card.html_text.split(' ')
#                     self.action_data['to_canvas']['number'] = number
#                     self.action_data['to_canvas']['color'] = color
#                     self.to_palette = False
#
#                 if event.ui_element == self.go_btn:
#                     # make a move
#                     pass
#
#                 if event.ui_element == self.pass_btn:
#                     # lose
#                     pass
#
#     def process_network_message(self, data):
#         # user lose
#         # user made a move
#         pass
