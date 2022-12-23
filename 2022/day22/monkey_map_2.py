from enum import IntEnum
from typing import Tuple, List, cast
import math


class Heading(IntEnum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4


class CubeMap:
    def __init__(self, grid: List[str]):
        self.x = next(i for i, c in enumerate(grid[0]) if c == '.')
        self.y = 0
        self.heading = Heading.RIGHT
        self.grid = grid
        self.edge_length = int(math.sqrt(sum(1 for s in grid for c in s if c != ' ') // 6))

    def move(self, amount: int):
        for _ in range(amount):
            next_x, next_y, next_heading = self._find_next_loc()
            if self.grid[next_y][next_x] == '#':
                break
            else:
                self.x, self.y, self.heading = next_x, next_y, next_heading

    def _find_next_loc(self) -> Tuple[int, int, Heading]:
        if self.heading == Heading.RIGHT:
            return self._transform(self.x + 1, self.y, self.heading)
        elif self.heading == Heading.DOWN:
            return self._transform(self.x, self.y + 1, self.heading)
        elif self.heading == Heading.LEFT:
            return self._transform(self.x - 1, self.y, self.heading)
        elif self.heading == Heading.UP:
            return self._transform(self.x, self.y - 1, self.heading)

    def _transform(self, x: int, y: int, heading: Heading) -> Tuple[int, int, Heading]:
        if (
                (0 <= y < len(self.grid))
                and (0 <= x < len(self.grid[y]))
                and self.grid[y][x] != ' '
        ):
            return x, y, heading
        if self.edge_length == 4:
            if y == -1:
                return 11 - x, 4, Heading.DOWN
            elif x == 7 and y < 4 and heading == Heading.LEFT:
                return 4 + y, 4, Heading.DOWN
            elif y == 3 and (4 <= x < 8) and heading == Heading.UP:
                return 8, x - 4, Heading.RIGHT
            elif y == 3 and (0 <= x < 4):
                return 11 - x, 0, Heading.DOWN
            elif x == -1:
                return 19 - y, 11, Heading.UP
            elif y == 8 and (0 <= x < 4):
                return 11 - x, 11, Heading.UP
            elif y == 8 and (4 <= x < 8) and heading == Heading.DOWN:
                return 8, 15 - x, Heading.RIGHT
            elif x == 7 and y > 7 and heading == Heading.LEFT:
                return 15 - y, 7, Heading.UP
            elif y == 12 and (8 <= x < 12):
                return 11 - x, 7, Heading.UP
            elif y == 12 and x > 12:
                return 0, 19 - x, Heading.RIGHT
            elif x > 16:
                return 11, 11 - y, Heading.LEFT
            elif y == 7 and (12 <= x < 16) and heading == Heading.UP:
                return 7, 19 - x, Heading.LEFT
            elif x == 12 and (4 <= y < 8) and heading == Heading.RIGHT:
                return 19 - y, 8, Heading.DOWN
            elif x == 12 and y < 4:
                return 15, 11 - y, Heading.LEFT
            else:
                raise AssertionError
        elif self.edge_length == 50:
            if y == -1 and (50 <= x < 100):
                return 0, x + 100, Heading.RIGHT
            elif y == -1 and x >= 100:
                return x - 100, 199, Heading.UP
            elif x == 150:
                return 99, 149 - y, Heading.LEFT
            elif y == 50 and x >= 100 and heading == Heading.DOWN:
                return 99, x - 50, Heading.LEFT
            elif x == 100 and (50 <= y < 100) and heading == Heading.RIGHT:
                return y + 50, 49, Heading.UP
            elif x == 100 and (100 <= y < 150):
                return 149, 149 - y, Heading.LEFT
            elif y == 150 and (50 <= x < 100) and heading == Heading.DOWN:
                return 49, x + 100, Heading.LEFT
            elif x == 50 and (150 <= y < 200) and heading == Heading.RIGHT:
                return y - 100, 149, Heading.UP
            elif y == 200:
                return x + 100, 0, Heading.DOWN
            elif x == -1 and (150 <= y < 200):
                return y - 100, 0, Heading.DOWN
            elif x == -1 and (100 <= y < 150):
                return 50, 149 - y, Heading.RIGHT
            elif y == 99 and (0 <= x < 50) and heading == Heading.UP:
                return 50, x + 50, Heading.RIGHT
            elif x == 49 and (50 <= y < 100) and heading == Heading.LEFT:
                return y - 50, 100, Heading.DOWN
            elif x == 49 and (0 <= y < 50):
                return 0, 149 - y, Heading.RIGHT
            else:
                raise AssertionError(f'({x}, {y}, {heading})')

    def turn(self, direction: str):
        if direction == 'R':
            new_heading_id = self.heading.value % 4 + 1
            self.heading = Heading(new_heading_id)
        elif direction == 'L':
            new_heading_id = (self.heading.value + 2) % 4 + 1
            self.heading = Heading(new_heading_id)
        else:
            raise AssertionError

    def password(self):
        return 1000 * (self.y + 1) + 4 * (self.x + 1) + self.heading.value - 1


DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

grid, code = raw_data.split('\n\n')
cube_map = CubeMap(grid.split('\n'))

code = cast(str, code)

moves = []
turns = []
instructions = []
last = 0
for i, c in enumerate(code):
    if c == 'R' or c == 'L':
        moves.append(int(code[last:i]))
        turns.append(c)
        last = i + 1
moves.append(int(code[last:]))

for move, turn in zip(moves, turns):
    cube_map.move(move)
    cube_map.turn(turn)
cube_map.move(moves[-1])

print(cube_map.password())

