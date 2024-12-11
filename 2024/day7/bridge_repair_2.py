DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


class Database:
    def __init__(self):
        self.cache = {}

    def is_valid_with_cache(self, target: int, vals: tuple[int, ...]) -> bool:
        if (target, vals) not in self.cache:
            self.cache[(target, vals)] = self.is_valid(target, vals)
        return self.cache[(target, vals)]

    def is_valid(self, target: int, vals: tuple[int, ...]) -> bool:
        if len(vals) == 1:
            return target == vals[0]
        last = vals[-1]
        add_result = self.is_valid_with_cache(target - last, vals[:-1])
        if add_result:
            return True

        mult_result = target % last == 0 and self.is_valid_with_cache(target // last, vals[:-1])
        if mult_result:
            return True

        base = 10 ** (len(str(last)))
        if target % base == last:
            return self.is_valid_with_cache(target // base, vals[:-1])

        return False


total = 0
db = Database()
for line in raw_data:
    target_str, *rest = line.split()
    target = int(target_str[:-1])
    vals = tuple([int(s) for s in rest])
    if db.is_valid_with_cache(target, vals):
        total += target

print(total)
