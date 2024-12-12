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
                perimeter = 0
                area = 0
                while frontier:
                    ii, jj = frontier.pop()
                    visited.add((ii, jj))
                    region.add((ii, jj))

                    area += 1
                    for iii, jjj in [(ii-1, jj), (ii, jj-1), (ii+1, jj), (ii, jj+1)]:
                        if (iii, jjj) in region:
                            continue

                        if self.padded_grid[iii][jjj] == char:
                            frontier.add((iii, jjj))
                        else:
                            perimeter += 1

                total += perimeter * area
                print(f"Found {char} region with area {area} and perimeter {perimeter} for a price of {area * perimeter}")

        return total


print(Grid(raw_data).calculate())
