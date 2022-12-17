import re
from dataclasses import dataclass
from typing import Tuple, Iterable

DATA_FILE = 'data/data.txt'
MAX_COORD = 4000000

with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


@dataclass(frozen=True)
class Sensor:
    x: int
    y: int
    rng: int


PATTERN = re.compile("-?[0-9]+")
sensors = []
for sensor_data in raw_data:
    s_x, s_y, b_x, b_y = [int(s) for s in PATTERN.findall(sensor_data)]
    sensor_range = abs(s_x - b_x) + abs(s_y - b_y)
    sensors.append(Sensor(s_x, s_y, sensor_range))


def get_boundary(s1: Sensor, s2: Sensor) -> Iterable[Tuple[int, int]]:
    if s1.x > s2.x:
        return get_boundary(s2, s1)

    start_x = max(s1.x, s2.x - s2.rng - 1)
    end_x = min(s1.x + s1.rng + 1, s2.x)
    x_range = range(start_x, end_x + 1)
    if s2.y > s1.y:
        start_y = s1.x - start_x + s1.y + s1.rng + 1
        end_y = s1.x - end_x + s1.y + s1.rng + 1
        y_range = range(start_y, end_y - 1, -1)
    else:
        start_y = start_x - s1.x + s1.y - s1.rng - 1
        end_y = end_x - s1.x + s1.y - s1.rng - 1
        y_range = range(start_y, end_y + 1)

    return zip(x_range, y_range)


def find_exclusion_spot():
    for i, s1 in enumerate(sensors):
        for s2 in sensors[i + 1:]:
            distance = abs(s2.x - s1.x) + abs(s2.y - s1.y)
            if distance == s1.rng + s2.rng + 2:
                for x, y in get_boundary(s1, s2):
                    if not any(abs(s.x - x) + abs(s.y - y) <= s.rng for s in sensors):
                        return x, y


beacon_x, beacon_y = find_exclusion_spot()
print((beacon_x, beacon_y))
print(beacon_x * MAX_COORD + beacon_y)


