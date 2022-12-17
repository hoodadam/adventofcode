from typing import List, Tuple

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


grid = [[int(c) for c in s] for s in raw_data]
m, n = len(grid), len(grid[0])
visible_trees = set()


def iter_trees(coordinates: List[Tuple[int, int]]) -> None:
    global visible_trees

    tallest = -1
    for i, j in coordinates:
        if grid[i][j] > tallest:
            tallest = grid[i][j]
            visible_trees.add((i, j))


for i in range(m):
    iter_trees([(i, j) for j in range(n)])
    iter_trees([(i, n - j - 1) for j in range(n)])

for j in range(n):
    iter_trees([(i, j) for i in range(m)])
    iter_trees([(m - i - 1, j) for i in range(m)])

print(len(visible_trees))