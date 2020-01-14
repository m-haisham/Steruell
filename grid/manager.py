import math

import pygame
import easygui

from core import Vector2D, Switch, Color
from widgets import Text

from .tile import Tile
from .algorithm import AStarAlgorithm
from .memory import AppDatabase

class GridManager:
    def __init__(self, size: Vector2D, info_text: Text, position=Vector2D(0, 20), padding=Vector2D(0, 0)):

        self.size = size
        self.position = position
        self.padding = padding

        self.info_text = info_text
        self.info_text.text = 'Select start'

        self.tilepadding = Vector2D(0, 0)
        screen_size = Vector2D.tuple(pygame.display.get_surface().get_rect().size)
        space = Vector2D(
            screen_size.x - position.x - padding.x,
            screen_size.y - position.y - padding.y
        )

        self.tilesize = Vector2D(
            int((space.x - (self.size.x * self.tilepadding.x)) / self.size.x),
            int((space.y - (self.size.y * self.tilepadding.y)) / self.size.y),
        )

        self.grid = []
        for x in range(size.x):
            l = [0] * size.y
            self.grid.append(l)

        self.tiles = []
        for x in range(size.x):
            l = [None] * size.y
            self.tiles.append(l)

        self.update_tiles(self.grid)

        self.drawable = Switch(True)

        self.mouse_left_down = Switch(False)
        self.mouse_left_down_type = None

        self.start = None
        self.end = None

        self.algorithm = None

        def onflip(val):
            if self.algorithm.solution_length == -1:
                self.info_text.text = 'No solution found'
                return

            self.info_text.text = 'Running' if val else f'Found solution of length {self.algorithm.solution_length}'

        self.running = Switch(False, onflip=onflip)

        self.misc = {}

    def update_tiles(self, grid):
        size = Vector2D(len(grid), len(grid[0]))

        for x in range(size.x):
            for y in range(size.y):
                position = Vector2D(
                    y * self.tilesize.x + y * self.tilepadding.x + self.position.x + self.padding.x,
                    x * self.tilesize.y + x * self.tilepadding.y + self.position.y + self.padding.y,
                )

                tile = Tile(Tile.int_to_state(self.grid[x][y]), gridpos=Vector2D(x, y), position=position,
                            size=self.tilesize)

                self.tiles[x][y] = tile

    def remake_tiles(self, positions):
        for gridposition in positions:
            x, y = gridposition

            position = Vector2D(
                y * self.tilesize.y + y * self.tilepadding.x + self.position.x + self.padding.x,
                x * self.tilesize.x + x * self.tilepadding.y + self.position.y + self.padding.y,
            )

            tile = Tile(Tile.int_to_state(self.grid[x][y]), gridpos=Vector2D(x, y), position=position,
                        size=self.tilesize)

            # tile.text.text = f'{self.algorithm.costgrid[x][y]:.1f}'
            # tile.text.text = str(self.algorithm.gcost[(x, y)])
            # tile.text.text = f'{self.algorithm.gcost[(x, y)]}+{self.algorithm.h(Vector2D(x, y))}'

            self.tiles[x][y] = tile

    def clean_grid(self, types, to=Tile.UNVISITED):
        if Tile.END in types:
            self.end = None
            self.info_text.text = 'Select end'

        if Tile.START in types:
            self.start = None
            self.info_text.text = 'Select start'

        to = Tile.state_to_int(to)

        size = Vector2D(len(self.grid), len(self.grid[0]))
        for x in range(size.x):
            for y in range(size.y):
                tile = self.grid[x][y]

                if Tile.int_to_state(tile) in types:
                    self.grid[x][y] = to

    def update_grid(self):
        for tile in self.all_tiles():
            x, y = tile.gridpos
            self.grid[x][y] = Tile.state_to_int(tile.state)

    def event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if not self.drawable.get():
                    easygui.msgbox('Press either Left Ctrl or Left Shift to clear the current grid'
                                   '\nLeft Ctrl: Everything excluding walls'
                                   '\nLeft Shift: Everything including walls', 'Clear grid', ok_button='CLOSE')
                    return

                self.update_grid()

                if self.start is None or self.end is None:
                    easygui.msgbox('Starting point or End point not specified', 'Missing inputs', 'CLOSE')
                    return

                # lock input and start the a* algorithm
                self.drawable.set(False)

                self.algorithm = AStarAlgorithm(self.grid)
                self.running.set(True)

            elif event.key == pygame.K_LSHIFT:
                if self.running.get():
                    return

                self.update_grid()
                self.clean_grid([Tile.VISITED, Tile.START, Tile.END, Tile.PATH, Tile.NEIGHBOURS, Tile.WALL])
                self.update_tiles(self.grid)
                self.drawable.set(True)

            elif event.key == pygame.K_LCTRL:
                if self.running.get():
                    return

                self.update_grid()
                self.clean_grid([Tile.VISITED, Tile.START, Tile.END, Tile.PATH, Tile.NEIGHBOURS])
                self.update_tiles(self.grid)
                self.drawable.set(True)

            elif event.key == pygame.K_s:
                self.update_grid()
                AppDatabase.database().save_grid(self.grid)

                easygui.msgbox('Successfully saved the grid', 'Success', 'CLOSE')

            elif event.key == pygame.K_l:
                grid = AppDatabase.database().load_grid()
                if grid is None:
                    easygui.msgbox('Unable to load', 'Missing data', 'CLOSE')
                    return

                self.grid = grid
                self.update_tiles(grid)

                easygui.msgbox('Successfully loaded the grid', 'Success', 'CLOSE')

        if event.type == pygame.MOUSEBUTTONDOWN:

            # left
            if event.button == 1:
                self.mouse_left_down.set(True)

                if self.drawable.get():

                    tile = self.tile(event.pos)
                    if tile is None:
                        return

                    # applying
                    currentstate = tile.state
                    if currentstate == Tile.WALL:
                        self.mouse_left_down_type = Tile.UNVISITED
                    elif currentstate == Tile.UNVISITED:
                        self.mouse_left_down_type = Tile.WALL

                    if self.mouse_left_down_type is not None:
                        tile.state = self.mouse_left_down_type

            # right
            elif event.button == 3:
                if self.drawable.get():

                    if self.start is None or self.end is None:
                        for tile in self.all_tiles():
                            if tile.inbound(Vector2D.tuple(event.pos)):

                                if self.start is None:
                                    self.start = tile
                                    tile.state = Tile.START

                                    self.info_text.text = 'Select end'
                                elif tile.state != Tile.START:
                                    self.end = tile
                                    tile.state = Tile.END
                                    self.info_text.text = 'Ready'

                    else:
                        print('Start and end has been selected')

        if event.type == pygame.MOUSEBUTTONUP:
            # left
            if event.button == 1:
                self.mouse_left_down.set(False)
                self.mouse_left_down_type = None

        if event.type == pygame.MOUSEMOTION:
            # left
            if self.mouse_left_down.get():

                if self.drawable.get():

                    tile = self.tile(event.pos)
                    if tile is None:
                        return

                    # applying
                    if self.mouse_left_down_type is not None:
                        tile.state = self.mouse_left_down_type

    def update(self):
        if self.running.get():
            try:
                affected = self.algorithm.next()
                self.remake_tiles(affected)
            except StopIteration:
                self.running.set(False)
        else:
            mouse_pos = Vector2D.tuple(pygame.mouse.get_pos())

            tile = self.tile(mouse_pos)
            if tile is None:
                return

            try:
                inbound = self.misc['over']
            except KeyError:
                inbound = None

            if not tile.hover:
                tile.enter()

            if inbound is not None and tile.position != inbound.position:
                inbound.exit()

            self.misc['over'] = tile

    def draw(self, surface):
        for x in range(self.size.x):
            for y in range(self.size.y):
                self.tiles[x][y].draw(surface)

    def tile(self, value):
        if isinstance(value, tuple):

            # finding tile
            position = Vector2D.tuple(value)

            x = (position.y - self.position.y - self.padding.y) / (self.tilesize.y + self.tilepadding.y)
            y = (position.x - self.position.x - self.padding.x) / (self.tilesize.x + self.tilepadding.x)

            ix = math.floor(x)
            iy = math.floor(y)

            # out of bounds
            if ix < 0 or ix >= self.size.x or iy < 0 or iy >= self.size.y:
                return

            tile = self.tiles[ix][iy]

        return tile

    def all_tiles(self):
        size = Vector2D(len(self.tiles), len(self.tiles[0]))
        for x in range(size.x):
            for y in range(size.y):
                yield self.tiles[x][y]

    @staticmethod
    def print_grid(grid):
        size = Vector2D(len(grid), len(grid[0]))
        for x in range(size.x):
            print('[', end='')
            for y in range(size.y):
                value = grid[x][y]
                print(value, end='')
                if y != size.y - 1:
                    print(', ', end='')
            print(']')
