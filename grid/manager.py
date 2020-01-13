import pygame
import easygui

from core import Vector2D, Switch, Color
from widgets import Text
from .tile import Tile
from .algorithm import AStarAlgorithm

class GridManager:
    def __init__(self, size: Vector2D, info_text: Text, position=Vector2D(0, 20), padding=Vector2D(5, 5)):

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

    def update_tiles(self, grid):
        size = Vector2D(len(grid), len(grid[0]))

        for x in range(size.x):
            for y in range(size.y):
                position = Vector2D(
                    y * self.tilesize.y + y * self.tilepadding.x + self.position.x + self.padding.x,
                    x * self.tilesize.x + x * self.tilepadding.y + self.position.y + self.padding.y,
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

            if event.key == pygame.K_LSHIFT:
                if self.running.get():
                    return

                self.update_grid()
                self.clean_grid([Tile.VISITED, Tile.START, Tile.END, Tile.PATH, Tile.NEIGHBOURS, Tile.WALL])
                self.update_tiles(self.grid)
                self.drawable.set(True)

            if event.key == pygame.K_LCTRL:
                if self.running.get():
                    return

                self.update_grid()
                self.clean_grid([Tile.VISITED, Tile.START, Tile.END, Tile.PATH, Tile.NEIGHBOURS])
                self.update_tiles(self.grid)
                self.drawable.set(True)

        if event.type == pygame.MOUSEBUTTONDOWN:

            # left
            if event.button == 1:
                self.mouse_left_down.set(True)

                if self.drawable.get():
                    # for all tiles check and initiate drawing
                    for tile in self.all_tiles():
                        if tile.inbound(Vector2D.tuple(event.pos)):
                            currentstate = tile.state
                            if currentstate == Tile.WALL:
                                self.mouse_left_down_type = Tile.UNVISITED
                            elif currentstate == Tile.UNVISITED:
                                self.mouse_left_down_type = Tile.WALL

                            if self.mouse_left_down_type is not None:
                                tile.state = self.mouse_left_down_type

            # right
            if event.button == 3:
                if self.drawable.get():

                    if self.start is None or self.end is None:
                        for tile in self.all_tiles():
                            if tile.inbound(Vector2D.tuple(event.pos)):

                                if self.start is None:
                                    self.start = tile
                                    tile.state = Tile.START

                                    self.info_text.text = 'Select end'
                                else:
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
                    # for all tiles draw / change state
                    for tile in self.all_tiles():
                        if tile.state == Tile.START or tile.state == Tile.END:
                            continue

                        if tile.inbound(Vector2D.tuple(event.pos)):
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

            for tile in self.all_tiles():
                inbound = tile.inbound(mouse_pos)

                if not tile.hover and inbound:
                    tile.enter()

                if tile.hover and not inbound:
                    tile.exit()

    def draw(self, surface):
        size = Vector2D(len(self.tiles), len(self.tiles[0]))

        for x in range(size.x):
            for y in range(size.y):
                self.tiles[x][y].draw(surface)

    def all_tiles(self):
        size = Vector2D(len(self.tiles), len(self.tiles[0]))
        for x in range(size.x):
            for y in range(size.y):
                yield self.tiles[x][y]

    def print_grid(self):
        size = Vector2D(len(self.tiles), len(self.tiles[0]))
        for x in range(size.x):
            print('[', end='')
            for y in range(size.y):
                value = self.grid[x][y]
                print(value, end='')
                if y != size.y - 1:
                    print(', ', end='')
            print(']')
