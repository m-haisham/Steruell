import pygame

from core import Vector2D, Color, colors
from .hover import DIM_LIGHT, ORIGINAL_COLOR
from ..text import Text
from ..widget import Widget, Hover


class Button(Widget):
    def __init__(self, text: Text, size: Vector2D = None, position: Vector2D = Vector2D.zero(), color: Color = None,
                 onclick=None):
        super(Button, self).__init__()

        # look
        self.text = text
        self.size = size
        if self.size is None:
            self.size = Vector2D(100, 35)
        self._position = position

        self.text.center(Vector2D.center(self.position, self.size))

        # color
        if color is None:
            color = colors.TRANSPARENT
        self._mutable_color = color
        self._original_color = color

        # behaviour
        self.onhover = Hover(DIM_LIGHT, ORIGINAL_COLOR)
        self.onclick = onclick

        if self.onclick is None:
            self.onclick = lambda button: None

    @property
    def original_color(self):
        return self._original_color

    @property
    def color(self):
        return self._mutable_color

    @color.setter
    def color(self, other):
        self._original_color = other
        self.mutate_color(other)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self.text.center(Vector2D.center(self.position, self.size))

    def mutate_color(self, other):
        self._mutable_color = other

    def apply_hover(self, onhover: Hover):
        self.onhover = Hover(onhover.onenter, onhover.onexit)
        return self

    def draw(self, surface: pygame.SurfaceType):
        s = pygame.Surface(self.size, pygame.SRCALPHA)
        s.fill(self.color)

        surface.blit(s, self.position)
        self.text.draw(surface)

    def inbound(self, mouse_pos: Vector2D):
        return self.position.x + self.size.x > mouse_pos.x > self.position.x and \
               self.position.y + self.size.y > mouse_pos.y > self.position.y

    def enter(self):
        super(Button, self).enter()
        self.onhover.enter(self)

    def exit(self):
        super(Button, self).exit()
        self.onhover.exit(self)

    def clicked(self):
        self.onclick(self)
