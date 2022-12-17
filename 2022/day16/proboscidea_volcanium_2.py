from collections import defaultdict
from typing import Dict, Set

from valve import parse_graph, find_paths

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


flow_rates, distances = parse_graph(raw_data)
all_paths = find_paths(flow_rates, distances, 26)

exclusion_dict: Dict[str, Set[int]] = defaultdict(set)
for i, (_, path) in enumerate(all_paths):
    for valve in flow_rates.keys() - path:
        exclusion_dict[valve].add(i)

initial_set = set(range(len(all_paths)))
exclusion_dict['AA'] = initial_set

best_pressure = 0
best_paths = None
for i, (pressure, path) in enumerate(all_paths):
    if i % (len(all_paths) // 100) == 0:
        print('#', end='')

    disjoint_path_ids = initial_set
    for valve in path:
        disjoint_path_ids = exclusion_dict[valve] & disjoint_path_ids

    for path_id in disjoint_path_ids:
        other_pressure, other_path = all_paths[path_id]
        if pressure + other_pressure > best_pressure:
            best_pressure = pressure + other_pressure
            best_paths = (path, other_path)
print()
print(best_pressure, best_paths)
