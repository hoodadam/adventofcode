import re

DATA_FILE = 'data/data.txt'
ROW = 2000000

with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


PATTERN = re.compile("-?[0-9]+")
ranges = []
beacons = set()
for sensor_data in raw_data:
    s_x, s_y, b_x, b_y = [int(s) for s in PATTERN.findall(sensor_data)]
    distance = abs(s_x - b_x) + abs(s_y - b_y)
    if distance >= abs(ROW - s_y):
        delta = distance - abs(ROW - s_y)
        ranges.append((s_x - delta, s_x + delta))

    if b_y == ROW:
        beacons.add(b_x)

ranges.sort()
merged_ranges = []
curr_lo, curr_hi = ranges[0]
for next_lo, next_hi in ranges[1:]:
    # we can merge (a, b) with (b+1, c) b/c there are integer ranges
    if curr_hi >= next_lo - 1:
        curr_hi = max(curr_hi, next_hi)
    else:
        merged_ranges.append((curr_lo, curr_hi))
        curr_lo, curr_hi = next_lo, next_hi

merged_ranges.append((curr_lo, curr_hi))
tot = 0
for lo, hi in merged_ranges:
    tot += hi - lo + 1 - sum(1 for b in beacons if lo <= b <= hi)

print(tot)