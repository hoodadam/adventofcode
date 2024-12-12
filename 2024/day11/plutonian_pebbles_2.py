DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


class Database:
    def __init__(self):
        self.cache: dict[tuple[int, int], int] = {}

    def _count_stones(self, val: int, blinks: int) -> int:
        if blinks == 0:
            return 1
        if (val, blinks) not in self.cache:
            self.cache[(val, blinks)] = self._count_stones_uncached(val, blinks)
        return self.cache[(val, blinks)]

    def _count_stones_uncached(self, val: int, blinks: int) -> int:
        if val == 0:
            return self._count_stones(1, blinks - 1)
        elif len(str(val)) % 2 == 0:
            s = str(val)
            l = len(s)
            left = int(s[:l//2])
            right = int(s[l//2:])
            return self._count_stones(left, blinks - 1) + self._count_stones(right, blinks - 1)
        else:
            return self._count_stones(val * 2024, blinks - 1)

    def count_stones(self, pebbles: list[int], blinks: int):
        return sum(self._count_stones(val, blinks) for val in pebbles)


db = Database()
pebbles = [int(s) for s in raw_data[0].split()]
print(db.count_stones(pebbles, 75))
