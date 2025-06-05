from collections import defaultdict


class Grid:
    x_max: int
    y_max: int
    robots: list[tuple[int, int, int, int]]

    def __init__(self, x_max: int, y_max: int, robots: list[tuple[int, int, int, int]]):
        self.x_max = x_max
        self.y_max = y_max
        self.robots = robots

    @staticmethod
    def parse(input_str: list[str]) -> 'Grid':
        x_max, y_max = [int(n) for n in input_str[0].split()]
        robots = [Grid._parse_robot(robot_str) for robot_str in input_str[1:]]
        return Grid(x_max, y_max, robots)

    @staticmethod
    def _parse_robot(robot_str: str) -> tuple[int, int, int, int]:
        position, velocity = robot_str.split()
        p_x, p_y = [int(n) for n in position[2:].split(",")]
        v_x, v_y = [int(n) for n in velocity[2:].split(",")]
        return p_x, p_y, v_x, v_y

    def print(self) -> None:
        robots_by_y: dict[int, set[int]] = defaultdict(set)
        for x, y, _, _ in self.robots:
            robots_by_y[y].add(x)

        for y in range(self.y_max):
            print("".join("*" if x in robots_by_y[y] else "." for x in range(self.x_max)))
        print()

    def move(self) -> None:
        self.robots = [
            ((p_x + v_x) % self.x_max, (p_y + v_y) % self.y_max, v_x, v_y)
            for p_x, p_y, v_x, v_y in self.robots
        ]


DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

grid = Grid.parse(raw_data)
grid.print()
for i in range(grid.x_max * grid.y_max):
    grid.move()
    print(f"{i + 1}:")
    grid.print()