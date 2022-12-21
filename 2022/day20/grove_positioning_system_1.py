from typing import Optional

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

nums = [int(s) for s in raw_data]


class Node:
    def __init__(self, val: int):
        self.val = val
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None

    def connect(self, prev: 'Node') -> None:
        self.prev = prev
        prev.next = self

    def rotate_forward(self) -> None:
        assert self.next is not None
        assert self.prev is not None

        self.next.connect(self.prev)
        tmp = self.next
        self.next.next.connect(self)
        self.connect(tmp)

    def rotate_back(self) -> None:
        assert self.next is not None
        assert self.prev is not None

        self.next.connect(self.prev)
        tmp = self.prev
        self.connect(self.prev.prev)
        tmp.connect(self)

    def _draw(self) -> str:
        l = [str(self.val)]
        node = self.next
        while node is not self:
            l.append(str(node.val))
            node = node.next
        return ' '.join(l)

    def __repr__(self):
        return self._draw()

    def __str__(self):
        return self._draw()


nodes = []
for n in nums:
    node = Node(n)
    if nodes:
        prev = nodes[-1]
        node.connect(prev)
    nodes.append(node)

nodes[0].connect(nodes[-1])

iter_node = None
for i, node in enumerate(nodes):
    if node.val > 0:
        for _ in range(node.val):
            node.rotate_forward()
    elif node.val < 0:
        for _ in range(-node.val):
            node.rotate_back()
    else:
        if iter_node is None:
            iter_node = node
        else:
            raise AssertionError

    if i % 50 == 49:
        print('#', end='')

print()

tot = 0
for i in range(3000):
    iter_node = iter_node.next
    if i % 1000 == 999:
        tot += iter_node.val

print(tot)
