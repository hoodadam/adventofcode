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
total_space = 70000000
required_space = 30000000
curr_space = root.size
min_space_to_delete = curr_space - (total_space - required_space)

candidates = [root]

best_option = root

while candidates:
    folder = candidates.pop()
    if min_space_to_delete < folder.size < best_option.size:
        best_option = folder
    candidates.extend(folder.folders)

print(best_option)