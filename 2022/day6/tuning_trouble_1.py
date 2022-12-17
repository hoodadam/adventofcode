DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


def solve(s: str) -> int:
    for i in range(4, len(s) + 1):
        if len(set(s[i-4:i])) == 4:
            return i
    raise AssertionError


for s in raw_data:
    print(solve(s))
