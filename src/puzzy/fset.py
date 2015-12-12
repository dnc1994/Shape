__author__ = 'Linghao Zhang'
__version__ = '0.1.0'


class Point(object):
    def __init__(self, *coordinate):
        coordinate = coordinate[0]
        self.x = float(coordinate[0])
        self.y = float(coordinate[1])


class FuzzySet(object):
    def __init__(self, name):
        self.name = name


class Triangle(FuzzySet):
    """
           _
          / \
         / | \
        /  |  \
       /   |   \
     _/    |    \_
      |    |    |
      a    b    c
    """
    def __init__(self, name, *points):
        super(Triangle, self).__init__(name)
        self.a = Point(points[0])
        self.b = Point(points[1])
        self.c = Point(points[2])
        assert self.a.y == self.c.y
        assert self.a.x < self.b.x
        assert self.b.x < self.c.x
        self.kab = (self.b.y - self.a.y) / (self.b.x - self.a.x)
        self.kbc = (self.c.y - self.b.y) / (self.c.x - self.b.x)

    def membership(self, x):
        x = float(x)
        if x < self.a.x:
            return 0
        elif x < self.b.x:
            return self.kab * (x - self.a.x) + self.a.y
        elif x < self.c.x:
            return self.kbc * (x - self.b.x) + self.b.y
        else:
            return 0


class Trapezoid(FuzzySet):
    """
           _____
          /     \
         /|     |\
        / |     | \
       /  |     |  \
     _/   |     |   \_
      |   |     |   |
      a   b     c   d
    """
    def __init__(self, name, *points):
        super(Trapezoid, self).__init__(name)
        self.a = Point(points[0])
        self.b = Point(points[1])
        self.c = Point(points[2])
        self.d = Point(points[3])
        assert self.a.y == self.d.y
        assert self.b.y == self.c.y
        assert self.a.x < self.b.x
        assert self.b.x < self.c.x
        assert self.c.x < self.d.x
        self.kab = (self.b.y - self.a.y) / (self.b.x - self.a.x)
        self.kcd = (self.d.y - self.c.y) / (self.d.x - self.c.x)

    def membership(self, x):
        x = float(x)
        if x < self.a.x:
            return 0
        elif x < self.b.x:
            return self.kab * (x - self.a.x) + self.a.y
        elif x < self.c.x:
            return self.b.y
        elif x < self.d.x:
            return self.kcd * (x - self.c.x) + self.c.y
        else:
            return 0


class LeftSkewTrapezoid(FuzzySet):
    """
       _____
      |     \
      |     |\
      |     | \
      |     |  \
     _|     |   \_
      |     |   |
      a     b   c
    """
    def __init__(self, name, *points):
        super(LeftSkewTrapezoid, self).__init__(name)
        self.a = Point(points[0])  # lower point
        self.b = Point(points[1])
        self.c = Point(points[2])
        assert self.a.y == self.c.y
        assert self.a.x < self.b.x
        assert self.b.x < self.c.x
        self.kbc = (self.c.y - self.b.y) / (self.c.x - self.b.x)

    def membership(self, x):
        x = float(x)
        if x < self.a.x:
            return 0
        elif x < self.b.x:
            return self.b.y
        elif x < self.c.x:
            return self.kbc * (x - self.b.x) + self.b.y
        else:
            return 0


class RightSkewTrapezoid(FuzzySet):
    """
           _____
          /     |
         /|     |
        / |     |
       /  |     |
     _/   |     |_
      |   |     |
      a   b     c
    """
    def __init__(self, name, *points):
        super(RightSkewTrapezoid, self).__init__(name)
        self.a = Point(points[0])
        self.b = Point(points[1])
        self.c = Point(points[2])  # lower point
        assert self.a.y == self.c.y
        assert self.a.x < self.b.x
        assert self.b.x < self.c.x
        self.kab = (self.b.y - self.a.y) / (self.b.x - self.a.x)

    def membership(self, x):
        x = float(x)
        if x < self.a.x:
            return 0
        elif x < self.b.x:
            return self.kab * (x - self.a.x) + self.a.y
        elif x < self.c.x:
            return self.b.y
        else:
            return 0


if __name__ == '__main__':
    tr = Triangle('1', (2, 0), (5, 1), (8, 0))
    print tr.membership(6)

    tp = Trapezoid('2', (0, 0), (1, 1), (3, 1), (4, 0))
    print tp.membership(3.5)

    lt = LeftSkewTrapezoid('3', (0, 0), (2, 1), (3, 0))
    print lt.membership(2.5)

    rt = RightSkewTrapezoid('4', (0, 0), (1, 1), (3, 0))
    print rt.membership(0.5)
