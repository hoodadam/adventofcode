from enum import IntEnum
from typing import cast, List


class Heading(IntEnum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4


class Map:
    def __init__(self, grid: List[str]):
        self.grid = grid
        self.x = next(i for i, c in enumerate(grid[0]) if c == '.')
        self.y = 0
        self.heading = Heading.RIGHT

    def move(self, amount: int):
        for _ in range(amount):
            if self.heading == Heading.RIGHT:
                next_x = self.x + 1
                row = self.grid[self.y]
                if next_x == len(row) or row[next_x] == ' ':
                    next_x = next(i for i, c in enumerate(row) if c != ' ')
                if row[next_x] == '#':
                    break
                else:
                    self.x = next_x
            elif self.heading == Heading.DOWN:
                next_y = self.y + 1
                if (
                        next_y == len(self.grid)
                        or len(self.grid[next_y]) <= self.x
                        or self.grid[next_y][self.x] == ' '
                ):
                    next_y = next(
                        i for i, row in enumerate(self.grid)
                        if len(row) > self.x and row[self.x] != ' '
                    )
                if self.grid[next_y][self.x] == '#':
                    break
                else:
                    self.y = next_y
            elif self.heading == Heading.LEFT:
                next_x = self.x - 1
                row = self.grid[self.y]
                if next_x == -1 or row[next_x] == ' ':
                    next_x = next(len(row) - i - 1 for i, c in enumerate(row[::-1]) if c != ' ')
                if row[next_x] == '#':
                    break
                else:
                    self.x = next_x
            elif self.heading == Heading.UP:
                next_y = self.y - 1
                if next_y == -1 or self.grid[next_y][self.x] == ' ':
                    next_y = next(
                        len(self.grid) - i - 1
                        for i, row in enumerate(self.grid[::-1])
                        if len(row) > self.x and row[self.x] != ' '
                    )
                if self.grid[next_y][self.x] == '#':
                    break
                else:
                    self.y = next_y
            else:
                raise AssertionError

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
map = Map(grid.split('\n'))

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
    map.move(move)
    map.turn(turn)
map.move(moves[-1])

print(map.password())
