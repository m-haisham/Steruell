
class Vector2D(tuple):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __new__(cls, x, y):
        return super(Vector2D, cls).__new__(cls, (x, y))

    @staticmethod
    def custom(surface, x, y, invertx=False, inverty=False):
        rect = surface.get_rect()

        if invertx:
            x = rect.size[0] - x

        if inverty:
            y = rect.size[1] - y

        return Vector2D(x, y)

    @staticmethod
    def center(position, size):

        if type(position) == tuple:
            position = Vector2D.tuple(position)
        if type(size) == tuple:
            size = Vector2D.tuple(size)

        return Vector2D(
            position.x + (size.x / 2),
            position.y + (size.y / 2)
        )

    @staticmethod
    def tuple(t):
        return Vector2D(t[0], t[1])

    @staticmethod
    def zero():
        """
        Factory method
        :return: x=0, y=0
        """
        return Vector2D(0, 0)