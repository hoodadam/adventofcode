from falling_sand import draw, parse, simulate


DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


obstructions, _, _, y_min, y_max = parse(raw_data)


def min_x_from_obstruction(x, y):
    return x - 1 - (y_max + 1 - y)


def max_x_from_obstruction(x, y):
    return x + 1 + (y_max + 1 - y)


x_min = 500 - (y_max + 3)
x_max = 500 + (y_max + 3)
for x in range(x_min - 1, x_max + 2):
    obstructions[(x, y_max + 2)] = '#'

count = 0
while simulate(obstructions, y_max + 2):
    count += 1

draw(obstructions, x_min, x_max, y_min, y_max)
print(count)

