DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

algorithm, image_str = raw_data.split('\n\n')
image_lines = image_str.split()
outside = 0
m = len(image_lines)
n = len(image_lines[0])

image = [[c == '#' for c in line] for line in image_lines]


def enhance():
    def compute(i, j):
        val = 0
        for ii in range(i - 2, i + 1):
            for jj in range(j - 2, j + 1):
                val *= 2
                val += image[ii][jj] if (0 <= ii < m - 2) and (0 <= jj < n - 2) else outside
        return algorithm[val] == '#'

    global m, n, image, outside
    m += 2
    n += 2

    image = [[compute(i, j) for j in range(n)] for i in range(m)]
    if algorithm[0] == '#' and outside == 0:
        outside = 1
    elif algorithm[-1] == '.' and outside == 1:
        outside = 0


def print_image():
    for i in range(m):
        print(''.join('#' if image[i][j] else '.' for j in range(n)))


for _ in range(50):
    enhance()
print(sum(sum(row) for row in image))
