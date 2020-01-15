class Widget:
    def __init__(self):
        self.hover = False

    def update(self, mouse_input):
        pass

    def inbound(self, mouse_pos):
        """
        :return: whether :param pos: is inside bounding box of widget
        """
        raise NotImplementedError('Not implemented')

    def enter(self):
        self.hover = True

    def exit(self):
        self.hover = False

    def draw(self, surface):
        """
        draws the widget onto the surface

        :param surface: surface to draw the widget
        :return: None
        """
        raise NotImplementedError('Not implemented')


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
