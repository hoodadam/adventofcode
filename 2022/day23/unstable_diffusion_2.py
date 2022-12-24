from collections import Counter
from dataclasses import dataclass
from typing import Set, Tuple, List


@dataclass(frozen=True)
class Attempt:
    move: Tuple[int, int]
    check: List[Tuple[int, int]]


def simulate_round(elves: Set[Tuple[int, int]], priorities: List[Attempt]) -> bool:
    proposals_by_elf = {}
    all_proposals = Counter()
    for elf in elves:
        x, y = elf
        if sum(1 for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (x + dx, y + dy) in elves) == 1:
            continue

        for attempt in priorities:
            if all((x + dx, y + dy) not in elves for dx, dy in attempt.check):
                xx, yy = attempt.move
                proposals_by_elf[(x, y)] = (x + xx, y + yy)
                all_proposals[(x + xx, y + yy)] += 1
                break

    an_elf_moved = False
    for elf, proposal in proposals_by_elf.items():
        if all_proposals[proposal] > 1:
            continue
        elves.remove(elf)
        elves.add(proposal)
        an_elf_moved = True
    return an_elf_moved


def draw(elves: Set[Tuple[int, int]]):
    x_min = min(x for x, _ in elves) - 3
    x_max = max(x for x, _ in elves) + 3
    y_min = min(y for _, y in elves) - 3
    y_max = max(y for _, y in elves) + 3
    for y in range(y_min, y_max + 1):
        print(''.join('#' if (x, y) in elves else '.' for x in range(x_min, x_max + 1)))
    print()


DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

elves = set()
for y, s in enumerate(raw_data):
    for x, c in enumerate(s):
        if c == '#':
            elves.add((x, y))

priorities = [
    Attempt((0, -1), [(-1, -1), (0, -1), (1, -1)]),
    Attempt((0, 1), [(-1, 1), (0, 1), (1, 1)]),
    Attempt((-1, 0), [(-1, -1), (-1, 0), (-1, 1)]),
    Attempt((1, 0), [(1, -1), (1, 0), (1, 1)]),
]
i = 1
while simulate_round(elves, priorities):
    i += 1
    priorities = priorities[1:] + [priorities[0]]

x_min = min(x for x, _ in elves)
x_max = max(x for x, _ in elves)
x_range = (x_max - x_min) + 1
y_min = min(y for _, y in elves)
y_max = max(y for _, y in elves)
y_range = (y_max - y_min) + 1
print(i)
