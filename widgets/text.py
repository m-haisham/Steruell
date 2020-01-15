import pygame

from core import Color, colors, Vector2D
from core.fonts import Roboto, Font
from .widget import Widget


class Text(Widget):
    surface: pygame.SurfaceType

    def __init__(self, text, size=14, italic=False, position=Vector2D.zero(), color: Color = colors.BLACK, font: Font = Roboto.MEDIUM):
        super(Text, self).__init__()

        self._text = text
        self._color = color

        self.font = font.get(size, italic)
        self.surface = self.font.render(text, True, color)
        self.position = position
        self.autocenter = False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

        prev_rect = self.surface.get_rect()
        self.surface = self.font.render(self.text, True, self.color)

        if self.autocenter:
            # size changes depending on amount of text so position is changed
            self.position = Vector2D(
                self.position.x + (prev_rect.size[0] - self.surface.get_rect().size[0]) / 2,
                self.position.y
            )

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.surface = self.font.render(self.text, True, self.color)

    @property
    def rect(self):
        return self.surface.get_rect()

    def center(self, position):
        size = self.surface.get_rect().size

        self.position = Vector2D(
            position.x - (size[0] / 2),
            position.y - (size[1] / 2)
        )

        self.autocenter = True

    def draw(self, surface):
        surface.blit(self.surface, self.position)