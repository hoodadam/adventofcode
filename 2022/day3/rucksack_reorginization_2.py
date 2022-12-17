from utils.chunk import chunk

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


def pri(c):
    b = ord(c)
    if b < 91:
        return b - 38
    else:
        return b - 96


tot = 0
for s1, s2, s3 in chunk(raw_data, 3):
    result = set(s1).intersection(set(s2)).intersection(set(s3))
    tot += pri(next(iter(result)))

print(tot)