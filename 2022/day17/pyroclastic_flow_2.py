from typing import List, Tuple

from cave import Cave

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

cave = Cave(raw_data)

last = 0
deltas = []
for _ in range(10000):
    cave.simulate_rock()
    deltas.append(cave.height - last)
    last = cave.height

n_rocks = 1000000000000


def calculate_height(pattern_start: int, pattern_len: int, n_rocks: int=1000000000000) -> int:
    pre_pattern_tot = sum(deltas[:pattern_start])
    pattern = deltas[pattern_start:pattern_start + pattern_len]
    n_patterns = (n_rocks - pattern_start) // pattern_len
    pattern_tot = n_patterns * sum(pattern)
    post_pattern_count = n_rocks - (n_patterns * pattern_len + pattern_start)
    post_pattern_tot = sum(pattern[:post_pattern_count])
    return pre_pattern_tot + pattern_tot + post_pattern_tot


def find_pattern(deltas: List[int]) -> Tuple[int, int]:
    for s in range(len(deltas)):
        rest = len(deltas) - s
        for l in range(1, rest // 2):
            count = rest // l
            candidate = deltas[s:s+l]
            if all(candidate == deltas[s+i*l:s+i*l+l] for i in range(count)):
                return s, l
    raise AssertionError("Pattern not found")


start, pattern_len = find_pattern(deltas)
print(start, pattern_len)
print(calculate_height(start, pattern_len))
