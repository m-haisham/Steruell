import math


class Vector2D(tuple):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __new__(cls, x, y):
        return super(Vector2D, cls).__new__(cls, (x, y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def euclidean(self, other) -> float:
        """
        :return: euclidean distance between two vectors
        """
        return math.sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))

    def manhattan(self, other) -> int:
        """
        :return: manhattan distance between two vectors
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    @staticmethod
    def custom(size, x, y, invertx=False, inverty=False):
        """
        :param size: size of bounding
        :param x: position x
        :param y: position y
        :param invertx: inverts x such that it starts from end (right)
        :param inverty: inverts y such that it starts from end (bottom)
        :return: vector corresponding to above flags
        :rtype: Vector2D
        """

        if invertx:
            x = size[0] - x

        if inverty:
            y = size[1] - y

        return Vector2D(x, y)

    @staticmethod
    def center(position, size):
        """
        :return: center of rect in :param position: of :param size:
        :rtype: Vector2D
        """

        return Vector2D(
            position[0] + (size[0] / 2),
            position[1] + (size[1] / 2)
        )

    @staticmethod
    def tuple(t):
        """
        Create Vector from tuple

        :param t: tuple to parse into vector
        :return: parsed 2d vector
        :rtype: Vector2D
        """
        return Vector2D(t[0], t[1])

    @staticmethod
    def zero():
        """
        Factory method
        :return: x=0, y=0
        :rtype: Vector2D
        """
        return Vector2D(0, 0)