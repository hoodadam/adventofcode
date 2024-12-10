import re

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

PATTERN = re.compile("mul\\(([0-9]{1,3}),([0-9]{1,3})\\)")
print(sum(int(s1) * int(s2) for line in raw_data for s1, s2 in re.findall(PATTERN, line)))
