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

manager = WidgetManager()

grid = GridManager(Vector2D(40, 40))

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

    t1 = time.time()
    framerate = 1 / (t1 - t0)
    t0 = t1

    Text(f'{framerate:.2f} fps', color=colors.WHITE).draw(screen)

    pygame.display.flip()
