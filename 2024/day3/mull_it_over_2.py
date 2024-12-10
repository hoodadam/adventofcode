import re

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

PATTERN = re.compile("mul\\(([0-9]{1,3}),([0-9]{1,3})\\)|(do)\\(\\)|(don't)\\(\\)")

total = 0
enabled = True
for line in raw_data:
    for s1, s2, do, dont in re.findall(PATTERN, line):
        if do:
            enabled = True
        elif dont:
            enabled = False
        elif enabled:
            total += int(s1) * int(s2)

print(total)