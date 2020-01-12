class Widget:
    def __init__(self):
        self.hover = False

    def update(self, mouse_input):
        pass

    def inbound(self, mouse_pos):
        raise Exception('Not implemented')

    def enter(self):
        self.hover = True

    def exit(self):
        self.hover = False

    def draw(self, surface):
        raise Exception('Not implemented')


class Hover:
    def __init__(self, onenter, onexit):
        self.onenter = onenter
        self.onexit = onexit

    def enter(self, widget):
        self.onenter(widget)

    def exit(self, widget):
        self.onexit(widget)

    @staticmethod
    def none():
        return Hover(lambda widget: None, lambda widget: None)
