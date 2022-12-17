import re


class Range:
    def __init__(self, min, max):
        # type: (Range, int, int) -> None
        self.min = min
        self.max = max

    def __len__(self):
        return self.max - self.min + 1

    def __repr__(self):
        return f'[{self.min},{self.max}]'

    def contains(self, other):
        # type: (Range, Range) -> bool
        return self.min <= other.min and self.max >= other.max

    def contains_point(self, point):
        # type: (Range, int) -> bool
        return self.min <= point <= self.max

    def intersects(self, other):
        # type: (Range, Range) -> bool
        return self.contains_point(other.min) or self.contains_point(other.max) \
               or other.contains_point(self.min) or other.contains_point(self.max)

    def intersection(self, other):
        # type: (Range, Range) -> Range
        assert self.intersects(other)
        return Range(max(self.min, other.min), min(self.max, other.max))

    def break_down(self, other):
        # type: (Range, Range) -> list[Range]
        result = []
        if self.min < other.min:
            result += [Range(self.min, other.min - 1)]
        result += [self.intersection(other)]
        if self.max > other.max:
            result += [Range(other.max + 1, self.max)]
        return result

    def __eq__(self, other):
        return isinstance(other, Range) and self.min == other.min and self.max == other.max

    def __hash__(self):
        return hash((self.min, self.max))


class Box:
    def __init__(self, x_range, y_range, z_range):
        # type: (Box, Range, Range, Range) -> None
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def volume(self):
        # type: (Box) -> int
        return len(self.x_range) * len(self.y_range) * len(self.z_range)

    def contains(self, other):
        # type: (Box, Box) -> bool
        return self.x_range.contains(other.x_range) \
               and self.y_range.contains(other.y_range) \
               and self.z_range.contains(other.z_range)

    def intersects(self, other):
        # type: (Box, Box) -> bool
        return self.x_range.intersects(other.x_range) \
               and self.y_range.intersects(other.y_range) \
               and self.z_range.intersects(other.z_range)

    def intersection(self, other):
        # type: (Box, Box) -> Box
        assert self.intersects(other)
        return Box(
            self.x_range.intersection(other.x_range),
            self.y_range.intersection(other.y_range),
            self.z_range.intersection(other.z_range)
        )

    def break_down(self, other):
        # type: (Box, Box) -> list[Box]
        return [
            Box(x_range, y_range, z_range)
            for x_range in self.x_range.break_down(other.x_range)
            for y_range in self.y_range.break_down(other.y_range)
            for z_range in self.z_range.break_down(other.z_range)
            if not other.contains(Box(x_range, y_range, z_range))
        ]

    def __eq__(self, other):
        return isinstance(other, Box) \
               and self.x_range == other.x_range \
               and self.y_range == other.y_range \
               and self.z_range == other.z_range

    def __hash__(self):
        return hash((self.x_range, self.y_range, self.z_range))

    def __repr__(self):
        return f'Box: {self.x_range} x {self.y_range} x {self.z_range}'


class Grid:
    _pattern = re.compile(
        '(on|off) x=(-?[0-9]+)\\.\\.(-?[0-9]+),y=(-?[0-9]+)\\.\\.(-?[0-9]+),z=(-?[0-9]+)\\.\\.(-?[0-9]+)')

    def __init__(self):
        self.on_boxes = set()

    def total_volume(self):
        return sum(box.volume() for box in self.on_boxes)

    def total_volume_in_box(self, bounds):
        return sum(box.intersection(bounds).volume() for box in self.on_boxes if box.intersects(bounds))

    def instruction(self, instruction):
        # type: (Grid, str) -> None
        on, box = Grid._parse_instruction(instruction)
        if on:
            self._box_on(box)
        else:
            self._box_off(box)

    @staticmethod
    def _parse_instruction(instruction):
        # type: (str) -> (bool, Box)
        match = Grid._pattern.match(instruction)
        on = match.group(1) == 'on'
        x_min = int(match.group(2))
        x_max = int(match.group(3))
        y_min = int(match.group(4))
        y_max = int(match.group(5))
        z_min = int(match.group(6))
        z_max = int(match.group(7))
        return on, Box(Range(x_min, x_max), Range(y_min, y_max), Range(z_min, z_max))

    def _box_on(self, new_box):
        # type: (Grid, Box) -> None
        add = {new_box}

        while add:
            to_process = set()
            remove = set()
            for to_add in add:
                actually_add = True
                for box in self.on_boxes:
                    if box.contains(to_add):
                        actually_add = False
                        break
                    elif to_add.contains(box):
                        actually_add = False
                        remove.add(box)
                        to_process.add(to_add)
                        break
                    elif box.intersects(to_add):
                        actually_add = False
                        to_process.update(to_add.break_down(box))
                        break
                pass
                if actually_add:
                    self.on_boxes.add(to_add)

            add = to_process
            self.on_boxes -= remove
            remove.clear()

    def _box_off(self, new_box):
        # type: (Grid, Box) -> None
        add = set()
        remove = set()
        for box in self.on_boxes:
            if new_box.contains(box):
                remove.add(box)
            elif box.intersects(new_box):
                add.update(box.break_down(new_box))
                remove.add(box)
        self.on_boxes -= remove
        self.on_boxes.update(add)

    def __repr__(self):
        return '\n'.join(str(box) for box in self.on_boxes)


DATA_FILE = 'data/actual.txt'
_pattern = re.compile(
    '(on|off) x=(-?[0-9]+)\\.\\.(-?[0-9]+),y=(-?[0-9]+)\\.\\.(-?[0-9]+),z=(-?[0-9]+)\\.\\.(-?[0-9]+)')

with open(DATA_FILE) as f:
    raw_data = f.read()

grid = Grid()
for i, line in enumerate(raw_data.splitlines()):
    grid.instruction(line)
    print(f'Instruction #{i} completed')

print(grid.total_volume_in_box(Box(Range(-50, 50), Range(-50, 50), Range(-50, 50))))
print(grid.total_volume())
