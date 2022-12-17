from typing import Dict, Tuple, List

from utils.math_ext import sign


def parse(raw_data: List[str]):
    obstructions = {}
    x_min, x_max = 500, 500
    y_min, y_max = 0, 0
    for line in raw_data:
        coords = [tuple(int(i) for i in coords.split(',')) for coords in line.split(' -> ')]
        x_min = min(x_min, *(x for x, _ in coords))
        x_max = max(x_max, *(x for x, _ in coords))
        y_min = min(y_min, *(y for _, y in coords))
        y_max = max(y_max, *(y for _, y in coords))
        for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
            if y1 == y2:
                sgn = sign(x2 - x1)
                for x in range(x1, x2 + sgn, sgn):
                    obstructions[(x, y1)] = '#'
            elif x1 == x2:
                sgn = sign(y2 - y1)
                for y in range(y1, y2 + sgn, sgn):
                    obstructions[(x1, y)] = '#'
            else:
                raise AssertionError

    return obstructions, x_min, x_max, y_min, y_max


def draw(obstructions: Dict[Tuple[int, int], str], x_min: int, x_max: int, y_min: int, y_max: int) -> None:
    for y in range(y_min, y_max + 3):
        print(''.join(obstructions.get((x, y), '.') for x in range(x_min - 1, x_max + 2)))


def simulate(obstructions: Dict[Tuple[int, int], str], y_max: int, origin: Tuple[int, int] = (500, 0)) -> bool:
    if origin in obstructions:
        return False

    x, y = origin
    while y < y_max:
        if (x, y + 1) not in obstructions:
            y += 1
        elif (x - 1, y + 1) not in obstructions:
            y += 1
            x -= 1
        elif (x + 1, y + 1) not in obstructions:
            y += 1
            x += 1
        else:
            obstructions[(x, y)] = 'o'
            return True

    return False
