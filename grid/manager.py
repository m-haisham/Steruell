import pygame

from core import Vector2D, Switch, Color
from grid.tile import Tile


class GridManager:
    def __init__(self, size: Vector2D, position=Vector2D(0, 20), padding=Vector2D(5, 5)):

        self.size = size
        self.position = position
        self.padding = padding

        self.tilepadding = Vector2D(1, 1)
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

    def update_grid(self):
        for tile in self.all_tiles():
            x, y = tile.gridpos
            self.grid[x][y] = Tile.state_to_int(tile.state)

    def event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.update_grid()

            if event.key == pygame.K_LSHIFT:
                self.drawable.flip()
                # start the a* algorithm

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
                    if self.start is None and self.end is None:
                        for tile in self.all_tiles():
                            if tile.inbound(Vector2D.tuple(event.pos)):

                                if self.start is None:
                                    self.start = tile
                                    tile.state = Tile.START
                                else:
                                    self.end = tile
                                    tile.state = Tile.END

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