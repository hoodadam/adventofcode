DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read().splitlines()


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def points(self):
        # type: (Line) -> list[Point]
        x1 = self.p1.v_x
        y1 = self.p1.y
        x2 = self.p2.v_x
        y2 = self.p2.y

        if x1 == x2:
            return [Point(x1, y) for y in Line._range_incl(y1, y2)]
        elif y1 == y2:
            return [Point(x, y1) for x in Line._range_incl(x1, x2)]
        else:
            return [Point(x, y) for (x, y) in zip(Line._range_incl(x1, x2), Line._range_incl(y1, y2))]

    @staticmethod
    def parse(line_str):
        # type: (str) -> Line
        [p1, p2] = line_str.split(' -> ')
        return Line(Point.parse(p1), Point.parse(p2))

    @staticmethod
    def _range_incl(i, j):
        # type: (int, int) -> range
        return range(i, j + 1) if i < j else range(i, j - 1, -1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return 1000 * self.x + self.y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    @staticmethod
    def parse(point_str):
        # type: (str) -> Point
        [x, y] = point_str.split(',')
        return Point(int(x), int(y))


one_line = set()
avoid = set()
for line_str in raw_data:
    line = Line.parse(line_str)
    for point in line.points():
        if point in one_line:
            one_line.remove(point)
            avoid.add(point)
        else:
            one_line.add(point)

print(len(avoid))
