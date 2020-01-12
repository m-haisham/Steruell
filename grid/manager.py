import pygame

from core import Vector2D, Switch, Color
from grid.tile import Tile


class GridManager:
    def __init__(self, size: Vector2D, position=Vector2D(0, 20), padding=Vector2D(5, 5)):

        self.size = size
        self.position = position
        self.padding = padding
        self.tilesize = Vector2D(20, 20)

        self.grid = []
        for x in range(size.x):
            l = [Tile.UNVISITED] * size.y
            self.grid.append(l)

        self.tiles = []
        self.update_tiles(self.grid)

        self.mouse_left_down = Switch(False)

        self.start = None
        self.end = None

    def update_tiles(self, grid):
        padding = 1
        size = Vector2D(len(grid), len(grid[0]))

        for x in range(size.x):
            l = [None] * size.y
            self.tiles.append(l)

        for x in range(size.x):
            for y in range(size.y):

                def onclick(tile):
                    tile.state = Tile.WALL

                position = Vector2D(
                    y * self.tilesize.y + y * padding + self.position.x + self.padding.x,
                    x * self.tilesize.x + x * padding + self.position.y + self.padding.y,
                )

                tile = Tile(self.grid[x][y], gridpos=Vector2D(x, y), position=position, size=self.tilesize,
                            onclick=onclick)

                self.tiles[x][y] = tile

    def event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            # left
            if event.button == 1:
                self.mouse_left_down.set(True)

                for tile in self.all_tiles():
                    if tile.inbound(Vector2D.tuple(event.pos)):
                        tile.clicked()

            # right
            if event.button == 3:
                if self.start is not None and self.end is not None:
                    print('Start and end has been selected')
                    return

                for tile in self.all_tiles():
                    if tile.inbound(Vector2D.tuple(event.pos)):

                        if self.start is None:
                            self.start = tile
                        else:
                            self.end = tile

                        tile.state = Tile.ANCHOR

        if event.type == pygame.MOUSEBUTTONUP:
            # left
            if event.button == 1:
                self.mouse_left_down.set(False)

        if event.type == pygame.MOUSEMOTION:
            # left
            if self.mouse_left_down.get():

                for tile in self.all_tiles():
                    if tile.inbound(Vector2D.tuple(event.pos)):
                        tile.clicked()

    def update(self):
        mouse_pos = Vector2D.tuple(pygame.mouse.get_pos())

        size = Vector2D(len(self.tiles), len(self.tiles[0]))
        for x in range(size.x):
            for y in range(size.y):
                tile = self.tiles[x][y]

                mouse_is_over = tile.inbound(mouse_pos)

                if not tile.hover and mouse_is_over:
                    tile.enter()

                if tile.hover and not mouse_is_over:
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