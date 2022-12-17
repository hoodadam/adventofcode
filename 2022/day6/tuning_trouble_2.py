DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


def solve(s: str) -> int:
    for i in range(14, len(s) + 1):
        if len(set(s[i-14:i])) == 14:
            return i
    raise AssertionError


for s in raw_data:
    print(solve(s))
