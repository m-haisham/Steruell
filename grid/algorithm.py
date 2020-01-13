import bisect

from core import Vector2D
from .tile import Tile


class AStarAlgorithm:
    def __init__(self, grid):
        self.grid = grid

        self.start = None
        self.end = None
        self.walls = []

        self.queue = []
        self.parent = {}
        self.gcost = {}

        self.path = ()

        self.current = None

        self.costgrid = []

        size = Vector2D(len(self.grid), len(self.grid[0]))
        for x in range(size.x):
            self.costgrid.append([-1] * size.y)

            for y in range(size.y):
                tile = self.grid[x][y]

                if Tile.int_to_state(tile) == Tile.START:
                    self.start = Vector2D(x, y)
                    self.costgrid[x][y] = 0

                elif Tile.int_to_state(tile) == Tile.END:
                    self.end = Vector2D(x, y)

                elif Tile.int_to_state(tile) == Tile.WALL:
                    self.walls.append(Vector2D(x, y))

        self.current = self.start
        self.gcost[tuple(self.current)] = 0

        self.solution_found = False
        self.solution_length = 0

    def g(self, vector):
        return self.gcost[tuple(vector)]

    def h(self, vector):
        return self.distance(vector, self.end)

    def distance(self, v1, v2):
        return v1.euclidean(v2)

    def get_viable_neigbours(self):

        vectors = []

        size = Vector2D(len(self.grid), len(self.grid[0]))
        for x in [self.current.x - 1, self.current.x, self.current.x + 1]:
            for y in [self.current.y - 1, self.current.y, self.current.y + 1]:

                # index out of range
                if x < 0 or x > size.x - 1 or y < 0 or y > size.y - 1:
                    continue

                # current pos
                if x == self.current.x and y == self.current.y:
                    continue

                tile = self.grid[x][y]
                state = Tile.int_to_state(tile)

                if state in [Tile.UNVISITED, Tile.NEIGHBOURS, Tile.END]:
                    vectors.append(Vector2D(x, y))

                    # update cost
                    grid_cost = self.costgrid[x][y]

                    g = self.g(self.current) + self.distance(self.current, Vector2D(x, y))
                    if grid_cost == -1:
                        self.gcost[(x, y)] = self.g(self.current) + self.distance(self.current, Vector2D(x, y))
                    else:
                        if self.gcost[(x, y)] > g:
                            self.gcost[(x, y)] = g

                    calculated_cost = self.g(Vector2D(x, y)) + self.h(Vector2D(x, y))

                    if grid_cost == -1 or grid_cost > calculated_cost:
                        self.costgrid[x][y] = calculated_cost
                        self.parent[(x, y)] = self.current

                    if state != Tile.END:
                        self.grid[x][y] = Tile.state_to_int(Tile.NEIGHBOURS)

        return vectors

    def inqueue(self, position):
        for point in self.queue:
            if point.position == position:
                return point

        return None

    def next(self):
        if self.solution_found:
            raise StopIteration()

        neigbours = self.get_viable_neigbours()

        for neigbour in neigbours:
            gridcost = self.costgrid[neigbour.x][neigbour.y]

            # enqueue and sort
            queued = self.inqueue(neigbour)
            if queued is not None:
                if queued.cost > gridcost:
                    queued.cost = gridcost
                    self.queue.sort()
            else:
                bisect.insort_right(self.queue, Point(neigbour, gridcost))
        try:
            next_point = self.queue.pop(0)
        except IndexError:
            self.solution_found = True
            self.solution_length = -1
            return []

        if self.current != self.start:
            self.grid[self.current.x][self.current.y] = Tile.state_to_int(Tile.VISITED)

        if next_point.position == self.end:
            self.solution_found = True

            current = self.current
            self.grid[current.x][current.y] = Tile.state_to_int(Tile.PATH)

            tiles = neigbours + [current]

            while current != self.start:

                tiles.append(current)
                current = self.parent[tuple(current)]
                self.grid[current.x][current.y] = Tile.state_to_int(Tile.PATH)

            self.solution_length = self.g(self.end)
            return tiles

        memory = self.current
        self.current = next_point.position

        return neigbours + [memory]


class Point:
    def __init__(self, position, cost):
        self.position = position
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost
