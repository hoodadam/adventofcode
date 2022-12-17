from filesystem import File, Folder


DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]

tot = 0
curr = []

for line in raw_data:
    parts = line.split(' ')
    if parts[0] == '$':
        if parts[1] == 'cd':
            if parts[2] == '..':
                curr.pop()
            else:
                folder = Folder(parts[2])
                if curr:
                    curr[-1].add_folder(folder)
                curr.append(folder)
    elif parts[0] != "dir":
        size = int(parts[0])
        name = parts[1]
        curr[-1].add_file(File(name=name, size=size))


root = curr[0]
print(root.sum_folders_no_bigger_than(100000))

