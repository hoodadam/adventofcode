from valve import parse_graph, find_paths

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


flow_rates, distances = parse_graph(raw_data)

all_paths = find_paths(flow_rates, distances, 30)
print(max(all_paths))
