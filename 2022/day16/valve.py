import re
from collections import defaultdict
from typing import List, Tuple, Dict

NAME_PATTERN = re.compile('[A-Z]{2}')
NUM_PATTERN = re.compile('[0-9]+')


def _parse_valve(s: str) -> Tuple[str, int, List[str]]:
    name, *tunnels = NAME_PATTERN.findall(s)
    flow = int(NUM_PATTERN.findall(s)[0])
    return name, flow, tunnels


def parse_graph(raw_data: List[str]) -> Tuple[Dict[str, int], Dict[str, Dict[str, int]]]:
    flow_rates: Dict[str, int] = {}
    edges: Dict[str, List[str]] = {}
    distances: Dict[str, Dict[str, int]] = defaultdict(dict)

    for s in raw_data:
        name, flow, tunnels = _parse_valve(s)
        if flow > 0:
            flow_rates[name] = flow
        edges[name] = tunnels

    for valve in edges:
        path = {valve}
        frontier = set(edges[valve])
        curr_distance = 2
        while frontier:
            for v in frontier:
                distances[valve][v] = curr_distance
            path.update(frontier)
            frontier = {vv for v in frontier for vv in edges[v] if vv not in path}
            curr_distance += 1

    return flow_rates, distances


def find_paths(
        flow_rates: Dict[str, int],
        distances: Dict[str, Dict[str, int]],
        max_time: int
) -> List[Tuple[int, List[str]]]:
    stack = [(['AA'], 0, 0)]
    all_paths: List[Tuple[int, List[str]]] = []
    while stack:
        path, pressure, time = stack.pop()
        all_paths.append((pressure, path))
        last_valve = path[-1]
        for valve in flow_rates.keys() - path:
            dist = distances[last_valve][valve]
            if dist + time < max_time:
                new_pressure = (max_time - dist - time) * flow_rates[valve]
                stack.append((path + [valve], pressure + new_pressure, dist + time))

    return all_paths
