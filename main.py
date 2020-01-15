import sys
import time

import pygame

from core import colors, Vector2D
from grid import GridManager, AppDatabase
from widgets import Text, WidgetManager

pygame.init()
size = width, height = 700, 720
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)

# allowed events
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYUP])

pygame.display.set_caption('A* visualizer')

info = Text('', color=colors.WHITE)
manager = WidgetManager([info])

grid = GridManager(Vector2D(50, 50), info)

framerate = 0
t0 = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            AppDatabase.database().save()
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
