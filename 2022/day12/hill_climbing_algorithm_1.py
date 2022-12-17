from typing import Tuple, List

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


def parse_grid(raw_data: List[str]) -> Tuple[List[List[int]], int, int, Tuple[int, int], Tuple[int, int]]:
    grid = [[ord(c) for c in line] for line in raw_data]
    m = len(grid)
    n = len(grid[0])

    start = None
    end = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 83:
                start = (i, j)
                grid[i][j] = 97
            elif grid[i][j] == 69:
                end = (i, j)
                grid[i][j] = 122

    return grid, m, n, start, end


grid, m, n, start, end = parse_grid(raw_data)

if start is None or end is None:
    raise AssertionError


def get_neighbors(i, j):
    curr_height = grid[i][j]
    all_neighbors = [
        (i + 1, j),
        (i - 1, j),
        (i, j + 1),
        (i, j - 1),
    ]
    return [
        (ii, jj) for ii, jj in all_neighbors
        if (0 <= ii < m) and (0 <= jj < n) and grid[ii][jj] <= curr_height + 1
    ]


visited = set()
frontier = {start}

steps = 0
while frontier:
    steps += 1
    visited.update(frontier)
    new_frontier = {(ii, jj) for i, j in frontier for ii, jj in get_neighbors(i, j) if (ii, jj) not in visited}
    if end in new_frontier:
        print(steps)

    frontier = new_frontier

