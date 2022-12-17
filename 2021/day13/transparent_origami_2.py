DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

dots_str, instructions = raw_data.split('\n\n')

dots = set()
for dot in dots_str.splitlines():
    (x, y) = [int(s) for s in dot.split(',')]
    dots.add((x, y))


def apply_fold(dir, val, x, y):
    xx, yy = x, y
    if dir == 'y':
        if y > val:
            yy = 2 * val - y
    elif dir == 'x':
        if x > val:
            xx = 2 * val - x
    else:
        raise AssertionError()
    return xx, yy


folds = instructions.splitlines()
maxes = {'x': 100000, 'y': 100000}
for fold in folds:
    line = fold.split()[-1]
    axis, val = line.split('=')
    val = int(val)
    maxes[axis] = val
    dots = {apply_fold(axis, val, x, y) for (x, y) in dots}

for y in range(maxes['y']):
    print(''.join('#' if (x, y) in dots else '.' for x in range(maxes['x'])))