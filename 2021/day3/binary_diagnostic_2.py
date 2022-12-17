DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read().splitlines()

n = len(raw_data)
m = len(raw_data[0])


def find_num(keep_high):
    current = range(n)
    for i in range(m):
        tot = 0
        ones = []
        zeros = []
        for j in current:
            if int(raw_data[j][i]):
                ones.append(j)
                tot += 1
            else:
                zeros.append(j)

        if (tot >= len(current) / 2 and keep_high) or (tot < len(current) / 2 and not keep_high):
            current = ones
        else:
            current = zeros

        if len(current) == 1:
            return to_int(current[0])
    raise AssertionError('Failed to find num')


def to_int(index):
    tot = 0
    for c in raw_data[index]:
        tot *= 2
        tot += int(c)
    return tot


ox = find_num(keep_high=True)
co2 = find_num(keep_high=False)
print(ox * co2)