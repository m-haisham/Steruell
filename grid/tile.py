from core import Vector2D, Color, colors
from widgets import Button, Text

from .mutual import MutualDict


class Tile(Button):
    UNVISITED = colors.WHITE
    VISITED = colors.BLUE
    NEIGHBOURS = colors.RED
    PATH = colors.GREEN
    WALL = colors.BLACK
    START = colors.YELLOW
    END = colors.PURPLE

    STATE_INT_MAP = MutualDict({
        UNVISITED: 0,
        VISITED: 1,
        NEIGHBOURS: 2,
        PATH: 3,
        WALL: 4,
        START: 5,
        END: 6,
    })

    def __init__(
            self,
            state,
            gridpos: Vector2D,
            padding: Vector2D = None,
            position: Vector2D = Vector2D.zero(),
            onclick=None
    ):
        super(Tile, self).__init__(Text('', size=10), padding, position, state, onclick)

        self.gridpos = gridpos

    @property
    def state(self):
        return self.original_color

    @state.setter
    def state(self, other):
        self.color = other

    @staticmethod
    def state_to_int(state: Color):
        return Tile.STATE_INT_MAP[state]

    @staticmethod
    def int_to_state(n):
        return Tile.STATE_INT_MAP[n]
