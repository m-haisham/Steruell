
class Color(tuple):
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __new__(cls, r, g, b, a=255):
        return super(Color, cls).__new__(cls, (r, g, b, a))

    def rgb(self):
        """
        :return: tuple of length 3 denoting (r, g, b)
        """
        return self.r, self.g, self.b

    def rgba(self):
        """
        :return: tuple of length 4 denoting (r, g, b, a)
        """
        return self.r, self.g, self.b, self.a

    def __mul__(self, other):
        if isinstance(other, float):

            return Color(
                self.r * other,
                self.g * other,
                self.b * other
            )

        else:
            TypeError(f'Expected (float) got ({type(other)})')

    __rmul__ = __mul__

    def copy(self):
        """
        :return: copy of color
        """
        t = tuple(self)[:]
        return Color.tuple(t)

    @staticmethod
    def lerp(value: float, *args):
        """
        :param value: float between 0 and 1, denoting which percentile to mix color
        :param args: colors to mix
        :return: mixed color according to parameters (no alpha channel)
        """

        if value <= 0:
            return args[0]
        elif value >= 1:
            return args[-1]

        a = None
        b = None

        pos = 2
        neg = -2

        slice = 1 / (len(args) - 1)
        for i in range(len(args)):
            v = i * slice
            diff = value - v
            if diff == 0:
                return args[i]
            elif diff > 0:
                if diff < pos:
                    b = args[i]
                    pos = diff
            else:
                if diff > neg:
                    a = args[i]
                    neg = diff

        pvalue = pos / slice
        nvalue = 1 - pvalue

        return Color(
            a[0] * pvalue + b[0] * nvalue,
            a[1] * pvalue + b[1] * nvalue,
            a[2] * pvalue + b[2] * nvalue,
        )

    @staticmethod
    def tuple(t):
        """
        :param t: tuple to create color from
        :return: Color from tuple(t)
        """
        if len(t) == 3:
            return Color(t[0], t[1], t[2])

        return Color(t[0], t[1], t[2], t[3])

    @staticmethod
    def hex(s):
        """
        :param s: hexadecimal string
        :return: Color denoted by hexadecimal
        """
        h = s.string('#')
        return Color.tuple(tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)))

    def __str__(self):
        return f'<Color{vars(self)}>'