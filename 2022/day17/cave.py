SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # Horizontal line
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],  # Plus
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # Reverse L
    [(0, 0), (0, 1), (0, 2), (0, 3)],  # Vertical line
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # Square
]


class Cave:
    def __init__(self, jet_pattern: str):
        self._rocks = set()
        self._height = 0
        self._jet_idx = 0
        self._jet_pattern = jet_pattern
        self._curr_rock = None
        self._shape_idx = 0

    def simulate_rock(self) -> None:
        self._gen_new_rock()
        while self._simulate_single_fall():
            pass

    def _simulate_single_fall(self) -> bool:
        self._move_lateral()
        return self._move_down()

    def _gen_new_rock(self):
        assert self._curr_rock is None
        shape = SHAPES[self._shape_idx]
        self._shape_idx = (self._shape_idx + 1) % 5
        self._curr_rock = [(x + 2, y + self._height + 3) for x, y in shape]

    def _move_lateral(self) -> None:
        def _is_valid(x: int, y: int):
            return (0 <= x < 7) and (x, y) not in self._rocks

        direction = 1 if self._jet_pattern[self._jet_idx] == '>' else -1
        self._jet_idx = (self._jet_idx + 1) % len(self._jet_pattern)
        if all(_is_valid(x + direction, y) for x, y in self._curr_rock):
            self._curr_rock = [(x + direction, y) for (x, y) in self._curr_rock]

    def _move_down(self) -> bool:
        def _is_valid(x: int, y: int) -> bool:
            return y >= 0 and (x, y) not in self._rocks

        if all(_is_valid(x, y - 1) for x, y in self._curr_rock):
            self._curr_rock = [(x, y - 1) for x, y in self._curr_rock]
            return True
        else:
            self._rocks.update((x, y) for x, y in self._curr_rock)
            self._height = max(self._height, *(y + 1 for _, y in self._curr_rock))
            self._curr_rock = None
            return False

    @property
    def height(self) -> int:
        return self._height

    def draw(self):
        def char(x, y):
            if (x, y) in self._rocks:
                return '#'
            elif self._curr_rock is not None and (x, y) in self._curr_rock:
                return '@'
            else:
                return '.'

        for y in range(self._height + 6, -1, -1):
            chars = [char(x, y) for x in range(7)]
            print('|' + ''.join(chars) + '|')
        print('+-------+')
        print()
