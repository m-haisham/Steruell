from core import Vector2D, Color, colors
from widgets import Button, Text


class Tile(Button):
    UNVISITED = colors.WHITE
    VISITED = colors.BLUE
    NEIGHBOURS = colors.RED
    PATH = colors.GREEN
    WALL = colors.BLACK
    START = colors.YELLOW
    END = colors.PURPLE

    def __init__(self, state, gridpos: Vector2D, size: Vector2D = None, position: Vector2D = Vector2D.zero(),
                 onclick=None):
        super(Tile, self).__init__(Text('', size=10), size, position, state, onclick)

        self.gridpos = gridpos

    @property
    def state(self):
        return self.original_color

    @state.setter
    def state(self, other):
        self.color = other

    @staticmethod
    def state_to_int(state: Color):
        if state == Tile.UNVISITED:
            return 0
        elif state == Tile.VISITED:
            return 1
        elif state == Tile.NEIGHBOURS:
            return 2
        elif state == Tile.PATH:
            return 3
        elif state == Tile.WALL:
            return 4
        elif state == Tile.START:
            return 5
        elif state == Tile.END:
            return 6

    @staticmethod
    def int_to_state(n):
        if n == 0:
            return Tile.UNVISITED
        elif n == 1:
            return Tile.VISITED
        elif n == 2:
            return Tile.NEIGHBOURS
        elif n == 3:
            return Tile.PATH
        elif n == 4:
            return Tile.WALL
        elif n == 5:
            return Tile.START
        elif n == 6:
            return Tile.END
