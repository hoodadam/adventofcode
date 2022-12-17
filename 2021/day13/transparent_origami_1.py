DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

dots_str, instructions = raw_data.split('\n\n')

dots = set()
for dot in dots_str.splitlines():
    (x, y) = [int(s) for s in dot.split(',')]
    dots.add((x, y))

first_fold = instructions.splitlines()[0]
line = first_fold.split()[-1]
dir, val = line.split('=')
val = int(val)


def apply_fold(axis, val, x, y):
    xx, yy = x, y
    if axis == 'y':
        if y > val:
            yy = 2 * val - y
    elif axis == 'x':
        if x > val:
            xx = 2 * val - x
    else:
        raise AssertionError()
    return xx, yy


dots = {apply_fold(dir, val, x, y) for (x, y) in dots}
print(len(dots))