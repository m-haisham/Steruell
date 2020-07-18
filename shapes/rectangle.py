import pygame

from core import Vector2D, Color
from .shape import Shape


class Rectangle(Shape):
    def __init__(self, position: Vector2D, size: Vector2D, color: Color):
        self._position = position
        self.size = size
        self.color = color
        self.size_color = color[:]

        self.rect = pygame.Rect(
            self._position.x, self._position.y,
            self.size.x, self.size.y
        )

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Vector2D):
        self._position = value

        # move rect
        self.rect.x = value.x

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
