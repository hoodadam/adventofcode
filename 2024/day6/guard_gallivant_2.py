from dataclasses import dataclass

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


@dataclass(frozen=True)
class Position:
    i: int
    j: int


class Map:
    FACINGS = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]

    def __init__(self, grid: list[str]):
        self.width = len(grid[0].strip())
        self.height = len(grid)
        self.obstacles: set[Position] = set()
        self.position = None
        for i, line in enumerate(raw_data):
            for j, c in enumerate(line):
                if c == "#":
                    self.obstacles.add(Position(i, j))
                elif c == "^":
                    self.position = Position(i, j)
        assert self.position
        self.facing_idx = 0
        self.visited: set[tuple[Position, int]] = {(self.position, self.facing_idx)}

    def _is_inbounds(self) -> bool:
        return (-1 < self.position.i < self.height) and (-1 < self.position.j < self.width)

    def _move(self) -> bool:
        facing_i, facing_j = self.FACINGS[self.facing_idx]
        new_pos = Position(self.position.i + facing_i, self.position.j + facing_j)

        if new_pos in self.obstacles:
            self.facing_idx = (self.facing_idx + 1) % 4
        else:
            self.position = new_pos

        if (self.position, self.facing_idx) in self.visited:
            return True
        if self._is_inbounds():
            self.visited.add((self.position, self.facing_idx))
        return False

    def simulate(self) -> int:
        initial_pos = self.position
        total = 0

        for i in range(self.height):
            for j in range(self.width):
                print(f"Trying with obstacle at ({i}, {j}) ...")
                candidate_pos = Position(i, j)
                if candidate_pos == initial_pos or candidate_pos in self.obstacles:
                    print("  ... skipped")
                    continue

                self.obstacles.add(candidate_pos)

                while self._is_inbounds():
                    if self._move():
                        total += 1
                        break

                print(f"  ... done (found {total} so far)")

                self.obstacles.remove(candidate_pos)
                self.position = initial_pos
                self.facing_idx = 0
                self.visited = {(self.position, self.facing_idx)}

        return total


print(Map(raw_data).simulate())
