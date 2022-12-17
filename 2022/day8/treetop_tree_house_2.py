from typing import List, Tuple

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


grid = [[int(c) for c in s] for s in raw_data]
m, n = len(grid), len(grid[0])


def tree_score(i, j):
    height = grid[i][j]

    def trees_in_direction(coords: List[Tuple[int, int]]) -> int:
        count = 0
        for ii, jj in coords:
            count += 1
            if grid[ii][jj] >= height:
                break

        return count

    below = trees_in_direction([(ii, j) for ii in range(i - 1, -1, -1)])
    above = trees_in_direction([(ii, j) for ii in range(i + 1, m)])
    left = trees_in_direction([(i, jj) for jj in range(j - 1, -1, -1)])
    right = trees_in_direction([(i, jj) for jj in range(j + 1, n)])
    return below * above * left * right


best_tree_score = max(tree_score(i, j) for i in range(m) for j in range(n))
print(best_tree_score)