from collections import defaultdict

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


class Grid:
    def __init__(self, test_data: list[str]):
        self.width = len(test_data[0].strip())
        self.height = len(test_data)
        self.padded_grid = [
            "." * (self.width + 2),
            *("." + line.strip() + "." for line in test_data),
            "." * (self.width + 2),
        ]

    def calculate(self) -> int:
        visited: set[tuple[int, int]] = set()
        total = 0
        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                if (i, j) in visited:
                    continue

                char = self.padded_grid[i][j]
                region: set[tuple[int, int]] = set()
                frontier = {(i, j)}
                edges: dict[str, dict[int, list[int]]] = defaultdict(lambda: defaultdict(list))
                area = 0
                while frontier:
                    ii, jj = frontier.pop()
                    visited.add((ii, jj))
                    region.add((ii, jj))

                    area += 1
                    for iii, jjj, facing in [(ii-1, jj, "^"), (ii, jj-1, "<"), (ii+1, jj, "v"), (ii, jj+1, ">")]:
                        if (iii, jjj) in region:
                            continue

                        if self.padded_grid[iii][jjj] == char:
                            frontier.add((iii, jjj))
                        else:
                            if facing in "<>":
                                edges[facing][jj].append(ii)
                            else:
                                edges[facing][ii].append(jj)

                sides = 0
                for facing, lines in edges.items():
                    for row, coords in lines.items():
                        coords.sort()
                        sides += 1
                        for last, curr in zip(coords, coords[1:]):
                            if curr > last + 1:
                                sides += 1

                total += sides * area
                print(f"Found {char} region with area {area} and {sides} sides for a price of {area * sides}")

        return total


print(Grid(raw_data).calculate())
