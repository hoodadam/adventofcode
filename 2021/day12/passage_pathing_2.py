from typing import Union

DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()


class Node:
    def __init__(self, label):
        # type: (Node, str) -> None
        self.is_small = label.islower()
        self.label = label
        self.edges = []

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return isinstance(other, Node) and self.label == other.label

    def __repr__(self):
        return self.label

    def add_edge(self, node):
        # type: (Node, Node) -> None
        self.edges.append(node)


class Path:
    def __init__(self, path, small_nodes_visited=(), small_double_visit=False):
        # type: (Path, list[Node], Union[tuple[Node], set[Node]], bool) -> None
        self.path = path
        self.small_nodes_visited = set(small_nodes_visited)
        self.small_double_visit = small_double_visit

    def append(self, node):
        # type: (Path, Node) -> Union[Path, None]
        if node.label == 'start':
            return None
        if self.path[-1].label == 'end':
            return None
        if node in self.small_nodes_visited and self.small_double_visit:
            return None
        small_nodes_visited = self.small_nodes_visited.copy()
        small_double_visit = self.small_double_visit or node in small_nodes_visited
        if node.is_small:
            small_nodes_visited.add(node)
        return Path(self.path + [node], small_nodes_visited=small_nodes_visited, small_double_visit=small_double_visit)

    def end(self):
        # type: (Path) -> Node
        return self.path[-1]

    def __repr__(self):
        return '-'.join(str(node) for node in self.path)


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_edge(self, v1, v2):
        # type: (Graph, str, str) -> None
        node1 = self._get_or_create_node(v1)
        node2 = self._get_or_create_node(v2)
        node1.add_edge(node2)
        node2.add_edge(node1)

    def _get_or_create_node(self, label):
        # type: (Graph, str) -> Node
        if label not in self.nodes:
            self.nodes[label] = Node(label)
        return self.nodes[label]

    def __repr__(self):
        nodes_repr = ', '.join(str(node) for node in self.nodes)
        return f'Graph[{nodes_repr}]'

    def find_paths(self):
        found_paths = []
        start = self._get_or_create_node('start')
        end = self._get_or_create_node('end')
        self._find_paths_helper(Path([start]), end, found_paths)
        return found_paths

    def _find_paths_helper(self, current_path, end, found_paths):
        # type: (Graph, Path, Node, list[Path]) -> None
        current_node = current_path.end()
        if current_node == end:
            found_paths.append(current_path)
        else:
            for next_node in current_node.edges:
                next_path = current_path.append(next_node)
                if next_path:
                    self._find_paths_helper(next_path, end, found_paths)


graph = Graph()
for edge in raw_data.splitlines():
    graph.add_edge(*edge.split('-'))

print(len(graph.find_paths()))
