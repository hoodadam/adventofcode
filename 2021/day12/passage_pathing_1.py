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
        self._find_paths_helper([start], end, found_paths)
        return found_paths

    def _find_paths_helper(self, current_path, end, found_paths):
        # type: (Graph, list[Node], Node, list[list[Node]]) -> None
        current_node = current_path[-1]
        if current_node == end:
            found_paths.append(current_path)
        else:
            for next_node in current_node.edges:
                if not (next_node.is_small and next_node in current_path):
                    self._find_paths_helper(current_path + [next_node], end, found_paths)


graph = Graph()
for edge in raw_data.splitlines():
    graph.add_edge(*edge.split('-'))

print(len(graph.find_paths()))
