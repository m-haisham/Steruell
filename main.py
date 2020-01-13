import sys
import time

import pygame

from core import colors, Switch, Vector2D, Color
from widgets import Text, WidgetManager, Button, Hover

from grid import GridManager

pygame.init()
size = width, height = 650, 670
screen = pygame.display.set_mode(size)

pygame.display.set_caption('A* visualizer')

info = Text('', color=colors.WHITE)
manager = WidgetManager([info])

grid = GridManager(Vector2D(40, 40), info)

framerate = 0
t0 = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        grid.event(event)
        manager.event(event)

    screen.fill(colors.BLACK)

    grid.update()
    grid.draw(screen)

    manager.update()
    manager.draw(screen)

    t1 = time.time()
    framerate = 1 / (t1 - t0)
    t0 = t1

    Text(f'{framerate:.2f} fps', position=Vector2D.custom(screen, 60, 0, invertx=True), color=colors.WHITE).draw(screen)

    pygame.display.flip()
