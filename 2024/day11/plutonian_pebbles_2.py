from utils.memoize import MemoizedOperation

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


class PebbleOp(MemoizedOperation[tuple[int, int], int]):

    def execute_uncached(self, key: tuple[int, int]) -> int:
        val, blinks = key
        if blinks == 0:
            return 1
        if val == 0:
            return self.execute((1, blinks - 1))
        elif len(str(val)) % 2 == 0:
            s = str(val)
            l = len(s)
            left = int(s[:l//2])
            right = int(s[l//2:])
            return self.execute((left, blinks - 1)) + self.execute((right, blinks - 1))
        else:
            return self.execute((val * 2024, blinks - 1))


op = PebbleOp()
pebbles = [int(s) for s in raw_data[0].split()]
print(sum(op.execute((val, 75)) for val in pebbles))
