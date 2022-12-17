import heapq
from collections import defaultdict
from dataclasses import dataclass

from typing import Optional

DATA_FILE = 'data/actual1.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

home_x = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
hallway_x = [0, 1, 3, 5, 7, 9, 10]
costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def dist(self, other):
        # type: (Point, Point) -> int
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y


@dataclass(frozen=True)
class AmphipodState:
    a1: Point
    a2: Point
    a3: Point
    a4: Point
    b1: Point
    b2: Point
    b3: Point
    b4: Point
    c1: Point
    c2: Point
    c3: Point
    c4: Point
    d1: Point
    d2: Point
    d3: Point
    d4: Point

    def all_positions(self):
        # type: (AmphipodState) -> set[Point]
        return {
            self.a1, self.a2, self.a3, self.a4,
            self.b1, self.b2, self.b3, self.b4,
            self.c1, self.c2, self.c3, self.c4,
            self.d1, self.d2, self.d3, self.d4,
        }

    def as_dict(self):
        # type: (AmphipodState) -> dict[str, list[Point]]
        return {
            'A': [self.a1, self.a2, self.a3, self.a4],
            'B': [self.b1, self.b2, self.b3, self.b4],
            'C': [self.c1, self.c2, self.c3, self.c4],
            'D': [self.d1, self.d2, self.d3, self.d4],
        }

    def at_point(self, point):
        # type: (AmphipodState, Point) -> Optional[str]
        for (kind, points) in self.as_dict():
            if point in points:
                return kind
        return None

    @staticmethod
    def from_dict(positions):
        # type: (dict[str, list[Point]]) -> AmphipodState
        return AmphipodState(
            positions['A'][0],
            positions['A'][1],
            positions['A'][2],
            positions['A'][3],
            positions['B'][0],
            positions['B'][1],
            positions['B'][2],
            positions['B'][3],
            positions['C'][0],
            positions['C'][1],
            positions['C'][2],
            positions['C'][3],
            positions['D'][0],
            positions['D'][1],
            positions['D'][2],
            positions['D'][3],
        )

    @staticmethod
    def from_text(lines):
        # type: (list[str]) -> AmphipodState
        positions = defaultdict(list)
        for x in range(3, 11, 2):
            for y in range(2, 4):
                # Our origin is the first empty hallway space, so the amphipod
                # rooms are at x = 2, 4, 6, & 8 and y = -1 & -4
                # Convert 2 to -1 and 3 to -4
                point_y = -3 * y + 5
                positions[lines[y][x]].append(Point(x - 1, point_y))
        # Add the two hidden lines from the diagram.
        positions['D'].append(Point(2, -2))
        positions['C'].append(Point(4, -2))
        positions['B'].append(Point(6, -2))
        positions['A'].append(Point(8, -2))
        positions['D'].append(Point(2, -3))
        positions['B'].append(Point(4, -3))
        positions['A'].append(Point(6, -3))
        positions['C'].append(Point(8, -3))
        for c in positions:
            positions[c].sort()
        return AmphipodState.from_dict(positions)

    def is_terminal_state(self):
        # type: (AmphipodState) -> bool
        return all(set(points) == {Point(home_x[kind], y) for y in range(1, 5)} for kind, points in (self.as_dict()))

    def heuristic(self):
        # type: (AmphipodState) -> int
        total = 0
        for kind, points in self.as_dict():
            def sorting_key(point):
                return 100 + point.y if point.x == home_x[kind] else point.x + point.y

            for i, point in enumerate(sorted(points, key=sorting_key, reverse=True)):
                j = 4 - i
                if point.x == home_x[kind]:
                    if point.y != j:
                        total += costs[kind] * (point.y + 2 + j)
                else:
                    total += costs[kind] * (point.y + abs(point.x - home_x[kind]) + j)
        return total

    def print(self):
        # type: (AmphipodState) -> None
        print('#############')
        print('#', end='')
        for x in range(0, 11):
            c = self.at_point(Point(x, 0))
            print(c if c else '.', end='')
        print('#')
        # Third thru sixth rows
        for y in range(-1, -5, -1):
            print('###' if y == -1 else '  #', end='')
            for x in range(2, 10, 2):
                c = self.at_point(Point(x, y))
                print(c if c else '.', end='')
                print('#', end='')
            print('##' if y == -1 else '')
        # Bottom row
        print('  #########\n')

    def cost(self, next_state):
        # type: (AmphipodState, AmphipodState) -> int
        start = self.all_positions().difference(next_state.all_positions())
        end = next_state.all_positions().difference(self.all_positions())
        if len(start) != 1 or len(end) != 1:
            raise AssertionError()

        start_point = start.pop()
        end_point = end.pop()
        start_amphipod = self.at_point(start_point)
        end_amphipod = next_state.at_point(end_point)
        assert start_amphipod is not None and start_amphipod == end_amphipod
        return start_point.dist(end_point) * costs[start_amphipod]


class Node:
    def __init__(self, label):
        # type: (Node, str) -> None
        self.label = label

    def __eq__(self, other):
        return isinstance(other, Node) and self.label == other.label

    def __hash__(self):
        return hash(self.label)

    def __repr__(self):
        return f'Node[{self.label}]'


class Amphipod:
    def __init__(self, label, cost, node):
        # type: (Amphipod, str, int, Node) -> None
        self.label = label
        self.cost = cost
        self.node = node

    def is_at_terminal_node(self):
        return self.node.label[1] == self.label[0].lower()

    def can_travel_to(self, node):
        # type: (Amphipod, Node) -> bool
        if self.node.label.startswith('r'):
            return self.node.label[0:2] != node.label[0:2]
        elif self.node.label.startswith('h'):
            return node.label.startswith('r' + self.label.lower())
        else:
            raise AssertionError()

    def move_to(self, node):
        # type: (Amphipod, Node) -> Amphipod
        return Amphipod(self.label, self.cost, node)

    def is_same_type(self, other):
        # type: (Amphipod, Amphipod) -> bool
        return self.label[0] == other.label[0]

    def __repr__(self):
        return self.label


class AmphipodGraph:
    def __init__(self, nodes, edges, amphipods, cost=0):
        # type: (AmphipodGraph, list[Node], list[tuple[Node, Node, int]], list[Amphipod], int) -> None
        self.nodes = {node.label: node for node in nodes}
        self.nodes_to_edges = {node: [] for node in nodes}
        for node1, node2, dist in edges:
            self.nodes_to_edges[node1].append((node2, dist))
            self.nodes_to_edges[node2].append((node1, dist))
        self.distances = self._calc_all_distances()

        self.amphipods = {amphipod.label: amphipod for amphipod in amphipods}
        self.occupied_nodes = {amphipod.node: amphipod for amphipod in amphipods}
        assert len(self.occupied_nodes) == len(amphipods)

        self.cost = cost

    def _calc_all_distances(self):
        # type: (AmphipodGraph) -> dict[tuple[Node, Node], int]
        return {
            (node1, node2): dist for node1 in self.nodes.values()
            for (node2, dist) in self._calc_all_distances_for_node(node1)
        }

    def _calc_all_distances_for_node(self, node):
        # type: (AmphipodGraph, Node) -> list[tuple[Node, int]]
        visited = {node}
        result = []
        frontier = {neighbor: dist for neighbor, dist in self.nodes_to_edges[node] if neighbor not in visited}
        while frontier:
            result.extend(frontier.items())
            new_frontier = {}
            visited.update(frontier.keys())
            for frontier_node, current_dist in frontier.items():
                new_frontier.update({
                    neighbor: current_dist + dist
                    for neighbor, dist in self.nodes_to_edges[frontier_node]
                    if neighbor not in visited
                })
            frontier = new_frontier
        return result

    def get_valid_moves(self):
        # type: (AmphipodGraph) -> list[AmphipodGraph]
        return [
            self._move_to(amphipod, node, dist) for amphipod in self.amphipods.values()
            for (node, dist) in self._find_possible_moves(amphipod)
        ]

    def _find_possible_moves(self, amphipod):
        # type: (AmphipodGraph, Amphipod) -> list[tuple[Node, int]]
        frontier = {node for node, _ in self.nodes_to_edges[amphipod.node]}
        visited = {amphipod.node}
        possible_destinations = []
        while frontier:
            new_frontier = []
            for node in frontier:
                if node not in self.occupied_nodes and node not in visited:
                    visited.add(node)
                    possible_destinations.append(node)
                    new_frontier.extend([node for node, _ in self.nodes_to_edges[node]])
            frontier = new_frontier
        return [
            (node, self.distances[(amphipod.node, node)])
            for node in possible_destinations if amphipod.can_travel_to(node)
        ]

    def _move_to(self, moving_amphipod, node, dist):
        # type: (AmphipodGraph, Amphipod, Node, int) -> AmphipodGraph
        amphipods = [
            amphipod.move_to(node) if amphipod == moving_amphipod
            else amphipod
            for amphipod in self.amphipods.values()
        ]
        return AmphipodGraph(nodes, edges, amphipods, self.cost + dist * moving_amphipod.cost)

    def is_terminal_state(self):
        return all(amphipod.is_at_terminal_node() for amphipod in self.amphipods.values())

    def _total_cost(self):
        return self.cost + self._heuristic()

    def _heuristic(self):
        total = 0
        curr = {c: 0 for c in 'ABCD'}

        def find_nearest_hallway(room_node):
            best = 100
            best_node = None
            for i in range(1, 8):
                hallway_node = self.nodes[f'h{i}']
                dist = self.distances[(room_node, hallway_node)]
                if dist < best:
                    best = dist
                    best_node = hallway_node
            return best_node

        def get_end_pos(amphipod):
            kind = amphipod.label[0]
            curr[kind] += 1
            node_label = 'r' + kind.lower() + str(curr[kind])
            return self.nodes[node_label]

        for amphipod in self.amphipods.values():
            if amphipod.is_at_terminal_node():
                node = amphipod.node
                pos = int(node.label[-1])
                for i in range(4, pos, -1):
                    if node not in self.occupied_nodes:
                        total += 1000000  # so that we always ignore these
                        break
                    elif not amphipod.is_same_type(self.occupied_nodes[node]):
                        hallway = find_nearest_hallway(amphipod.node)
                        end_pos = get_end_pos(amphipod)
                        total_dist = self.distances[(amphipod.node, hallway)] + self.distances[hallway, end_pos]
                        total += amphipod.cost * total_dist
                        break
            else:
                end_pos = get_end_pos(amphipod)
                total += amphipod.cost * self.distances[(amphipod.node, end_pos)]
        return total

    def __lt__(self, other):
        assert isinstance(other, AmphipodGraph)
        return self._total_cost() < other._total_cost()

    def __repr__(self):
        cost = self._total_cost()
        return f'AmphipodGraph(cost={cost})'


def find_optimal_path(initial_graph):
    # type: (AmphipodGraph) -> int
    queue = [initial_graph]
    heapq.heapify(queue)
    while queue:
        graph = heapq.heappop(queue)
        if graph.is_terminal_state():
            return graph.cost
        for move in graph.get_valid_moves():
            heapq.heappush(queue, move)
    raise AssertionError()


ra1 = Node('ra1')
ra2 = Node('ra2')
ra3 = Node('ra3')
ra4 = Node('ra4')
rb1 = Node('rb1')
rb2 = Node('rb2')
rb3 = Node('rb3')
rb4 = Node('rb4')
rc1 = Node('rc1')
rc2 = Node('rc2')
rc3 = Node('rc3')
rc4 = Node('rc4')
rd1 = Node('rd1')
rd2 = Node('rd2')
rd3 = Node('rd3')
rd4 = Node('rd4')
h1 = Node('h1')
h2 = Node('h2')
h3 = Node('h3')
h4 = Node('h4')
h5 = Node('h5')
h6 = Node('h6')
h7 = Node('h7')
nodes = [
    ra1, ra2, ra3, ra4,
    rb1, rb2, rb3, rb4,
    rc1, rc2, rc3, rc4,
    rd1, rd2, rd3, rd4,
    h1, h2, h3, h4, h5, h6, h7
]
edges = [
    (ra4, ra3, 1),
    (ra3, ra2, 1),
    (ra2, ra1, 1),
    (ra1, h2, 2),
    (ra1, h3, 2),
    (rb4, rb3, 1),
    (rb3, rb2, 1),
    (rb2, rb1, 1),
    (rb1, h3, 2),
    (rb1, h4, 2),
    (rc4, rc3, 1),
    (rc3, rc2, 1),
    (rc2, rc1, 1),
    (rc1, h4, 2),
    (rc1, h5, 2),
    (rd4, rd3, 1),
    (rd3, rd2, 1),
    (rd2, rd1, 1),
    (rd1, h5, 2),
    (rd1, h6, 2),
    (h1, h2, 1),
    (h2, h3, 2),
    (h3, h4, 2),
    (h4, h5, 2),
    (h5, h6, 2),
    (h6, h7, 1),
]

test_amphipods = [
    Amphipod('A1', 1, ra4),
    Amphipod('A2', 1, rc3),
    Amphipod('A3', 1, rd2),
    Amphipod('A4', 1, rd4),
    Amphipod('B1', 10, ra1),
    Amphipod('B2', 10, rb3),
    Amphipod('B3', 10, rc1),
    Amphipod('B4', 10, rc2),
    Amphipod('C1', 100, rb1),
    Amphipod('C2', 100, rb2),
    Amphipod('C3', 100, rc4),
    Amphipod('C4', 100, rd3),
    Amphipod('D1', 1000, ra2),
    Amphipod('D2', 1000, ra3),
    Amphipod('D3', 1000, rb4),
    Amphipod('D4', 1000, rd1),
]

actual_amphipods = [
    Amphipod('A1', 1, rb4),
    Amphipod('A2', 1, rc3),
    Amphipod('A3', 1, rc4),
    Amphipod('A4', 1, rd2),
    Amphipod('B1', 10, ra1),
    Amphipod('B2', 10, rb1),
    Amphipod('B3', 10, rb3),
    Amphipod('B4', 10, rc2),
    Amphipod('C1', 100, ra4),
    Amphipod('C2', 100, rb2),
    Amphipod('C3', 100, rd3),
    Amphipod('C4', 100, rd4),
    Amphipod('D1', 1000, ra2),
    Amphipod('D2', 1000, ra3),
    Amphipod('D3', 1000, rc1),
    Amphipod('D4', 1000, rd1),
]

test = AmphipodGraph(nodes, edges, test_amphipods)
find_optimal_path(test)
