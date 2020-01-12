import pygame

from core import Vector2D, Color
from .shape import Shape


class Rectangle(Shape):
    def __init__(self, position: Vector2D, size: Vector2D, color: Color):
        self.position = position
        self.size = size
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (
            self.position.x, self.position.y,
            self.size.x, self.size.y
        ))
