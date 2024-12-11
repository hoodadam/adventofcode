DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


class Map:
    def __init__(self, grid: list[str]):
        self.grid = [[int(c) for c in line.strip()] for line in grid]
        self.height = len(grid)
        self.width = len(grid[0].strip())

    def _find_adjacent(self, i: int, j: int, target_val: int) -> list[tuple[int, int]]:
        return [
            (ii, jj)
            for ii, jj in [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
            if (-1 < ii < self.height) and (-1 < jj < self.width) and self.grid[ii][jj] == target_val
        ]

    def _map_trailhead_to_peaks(self, i: int, j: int) -> set[tuple[int, int]]:
        current = {(i, j)}
        for level in range(1, 10):
            current = {(iii, jjj) for ii, jj in current for iii, jjj in self._find_adjacent(ii, jj, level)}
        return current

    def calculate_score(self) -> int:
        trailheads = [(i, j) for i in range(self.height) for j in range(self.width) if self.grid[i][j] == 0]
        trailhead_to_peaks = {trailhead: self._map_trailhead_to_peaks(*trailhead) for trailhead in trailheads}
        return sum(len(peaks) for peaks in trailhead_to_peaks.values())


print(Map(raw_data).calculate_score())
