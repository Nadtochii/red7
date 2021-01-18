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
