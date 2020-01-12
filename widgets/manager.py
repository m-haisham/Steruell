import pygame

from core import Vector2D


class WidgetManager:
    def __init__(self, widgets: list = None):
        self.widgets = widgets
        if self.widgets is None:
            self.widgets = []

    def draw(self, surface):
        for widget in self.widgets:
            widget.draw(surface)

    def update(self):
        mouse_pos = Vector2D.tuple(pygame.mouse.get_pos())

        for widget in self.widgets:

            mouse_is_over = widget.inbound(mouse_pos)

            if not widget.hover and mouse_is_over:
                widget.enter()

            if widget.hover and not mouse_is_over:
                widget.exit()

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for widget in self.widgets:

                # left button
                if event.button == 1:
                    if widget.inbound(Vector2D.tuple(event.pos)):
                        clicked = getattr(widget, 'clicked', None)
                        if callable(clicked):
                            clicked()