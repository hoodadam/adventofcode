from dataclasses import dataclass
from enum import IntEnum


class Direction(IntEnum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


CODE_TO_DIRECTION = {
    'U': Direction.UP,
    'R': Direction.RIGHT,
    'D': Direction.DOWN,
    'L': Direction.LEFT,
}


@dataclass
class Position:
    x: int
    y: int

    def move(self, direction: Direction) -> None:
        if direction == Direction.UP:
            self.y += 1
        elif direction == Direction.RIGHT:
            self.x += 1
        elif direction == Direction.DOWN:
            self.y -= 1
        elif direction == Direction.LEFT:
            self.x -= 1
        else:
            raise AssertionError

    def is_adjacent(self, other: 'Position') -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def follow(self, other: 'Position') -> None:
        if self.is_adjacent(other):
            return

        if self.x - other.x == 2:
            self.x = other.x + 1
            if self.y - other.y == 2:
                self.y = other.y + 1
            elif self.y - other.y == -2:
                self.y = other.y - 1
            else:
                self.y = other.y
        elif self.x - other.x == -2:
            self.x = other.x - 1
            if self.y - other.y == 2:
                self.y = other.y + 1
            elif self.y - other.y == -2:
                self.y = other.y - 1
            else:
                self.y = other.y
        elif self.y - other.y == 2:
            self.x = other.x
            self.y = other.y + 1
        elif self.y - other.y == -2:
            self.x = other.x
            self.y = other.y - 1
        else:
            raise AssertionError