from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import List, Tuple


class Direction(Enum):
    RIGHT = (1, 0, '>')
    DOWN = (0, 1, 'v')
    LEFT = (-1, 0, '<')
    UP = (0, -1, '^')

    @property
    def symbol(self):
        _, _, symbol = self.value
        return symbol


@dataclass
class Blizzard:
    x: int
    y: int
    d: Direction

    def next(self, height: int, width: int) -> Tuple[int, int]:
        dx, dy, _ = self.d.value
        return (self.x + dx) % width, (self.y + dy) % height

    def move(self, height: int, width: int):
        self.x, self.y = self.next(height, width)


class Map:
    def __init__(
            self,
            width: int,
            height: int,
            blizzards: List[Blizzard]
    ):
        self.width = width
        self.height = height
        self.blizzards = blizzards
        self.x = 0
        self.y = -1

    def solve(self, start: Tuple[int, int], goal: Tuple[int, int]) -> int:
        turn = 0
        states = {start}
        while goal not in states:
            blizzard_moves = {blizzard.next(self.height, self.width) for blizzard in self.blizzards}

            def is_valid(x: int, y: int):
                if (x, y) in blizzard_moves:
                    return False
                if (0 <= x < self.width) and (0 <= y < self.height):
                    return True
                return (x, y) == start or (x, y) == goal

            states = {
                (x + dx, y + dy)
                for x, y in states
                for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]
                if is_valid(x + dx, y + dy)
            }
            for blizzard in self.blizzards:
                blizzard.move(self.height, self.width)
            turn += 1
        return turn


DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


all_blizzards = []
grid_height = len(raw_data) - 2
grid_width = len(raw_data[0]) - 3
for y, s in enumerate(raw_data[1:-1]):
    for x, c in enumerate(s[1:-2]):
        if c == '>':
            all_blizzards.append(Blizzard(x, y, Direction.RIGHT))
        elif c == '<':
            all_blizzards.append(Blizzard(x, y, Direction.LEFT))
        elif c == '^':
            all_blizzards.append(Blizzard(x, y, Direction.UP))
        elif c == 'v':
            all_blizzards.append(Blizzard(x, y, Direction.DOWN))

map = Map(grid_width, grid_height, all_blizzards)
trip1 = map.solve((0, -1), (grid_width - 1, grid_height))
trip2 = map.solve((grid_width - 1, grid_height), (0, -1))
trip3 = map.solve((0, -1), (grid_width - 1, grid_height))
print(trip1, trip2, trip3)
print(trip1 + trip2 + trip3)
