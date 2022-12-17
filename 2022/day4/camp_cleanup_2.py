from typing import Tuple

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


def overlaps(s: str) -> bool:
    (s1, e1), (s2, e2) = parse_ranges(s)
    return (s2 <= s1 <= e2) or (s2 <= e1 <= e2) or (s1 <= s2 <= e1) or (s1 <= e2 <= e1)


def parse_ranges(s: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    r1, r2 = s.split(',')
    return parse_range(r1), parse_range(r2)


def parse_range(r: str) -> Tuple[int, int]:
    s, e = r.split('-')
    return int(s), int(e)


print(sum(overlaps(s) for s in raw_data))