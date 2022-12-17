from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from typing import Optional


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def distance(self, other):
        # type: (Point, Point) -> int
        return abs(self.x - other.x) + abs(self.y - other.y)


home_x_positions = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
hall_x_positions = [0, 1, 3, 5, 7, 9, 10]


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
            self.a1, self.a2, self.b1, self.b2, self.c1, self.c2, self.d1, self.d2,
            self.a3, self.a4, self.b3, self.b4, self.c3, self.c4, self.d3, self.d4
        }

    def as_dict(self):
        # type: (AmphipodState) -> dict[str, list[Point]]
        return {'A': [self.a1, self.a2, self.a3, self.a4],
                'B': [self.b1, self.b2, self.b3, self.b4],
                'C': [self.c1, self.c2, self.c3, self.c4],
                'D': [self.d1, self.d2, self.d3, self.d4],
                }

    def at_point(self, p):
        # type: (AmphipodState, Point) -> Optional[str]
        dict = self.as_dict()
        for c in dict:
            if p in dict[c]:
                return c
        return None

    @staticmethod
    def from_text(lines):
        # type: (list[str]) -> AmphipodState
        positions = defaultdict(list)
        for x in range(3, 11, 2):
            for y in range(2, 4):
                # Our origin is the first empty hallway space, so the amphipod
                # rooms are at x = 2, 4, 6, & 8 and y = -1 & -4
                # Convert 2 to -1 and 3 to -4
                pointY = -3 * y + 5
                positions[lines[y][x]].append(Point(x - 1, pointY))
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

    def is_complete(self):
        # type: (AmphipodState) -> bool
        dict = self.as_dict()
        for c in dict.keys():
            for y in range(-4, 0, 1):
                if Point(home_x_positions[c], y) not in dict[c]:
                    return False
        return True

    def heuristic(self):
        # type: (AmphipodState) -> int
        """
        The heuristic cost is the shortest path of each amphipod to its home.
        """
        cost = 0
        for c, positions in self.as_dict().items():
            for i, position in enumerate(positions):
                # The home y positions are -4 thru -1, so they are i - 4 since i will be 0 thru 3.
                cost += position.distance(Point(home_x_positions[c], i - 4)) * costs[c]
        return cost

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
        # type: (AmphipodState, AmphipodState) -> float
        start_points = self.all_positions().difference(next_state.all_positions())
        end_points = next_state.all_positions().difference(self.all_positions())
        if len(start_points) != 1 or len(end_points) != 1:
            raise ValueError(
                "There can only be one amphipod in a different location between successive states.")
        start_point = start_points.pop()
        end_point = end_points.pop()
        start_value = self.at_point(start_point)
        end_value = next_state.at_point(end_point)
        if start_value is None:
            raise ValueError(f"Nothing found at {start_point}.")
        if end_value is None:
            raise ValueError(f"Nothing found at {end_point}.")
        if start_value != end_value:
            raise ValueError(
                f"Value at {start_point} ({start_value}) doesn't match value at {end_point} ({end_value}).")
        return start_point.distance(end_point) * costs[start_value]

    def replace_position(self, c, x, y, i):
        # type: (AmphipodState, str, int, int, int) -> AmphipodState
        new_state = self.as_dict()
        new_state[c][i] = Point(x, y)
        new_state[c].sort()
        return AmphipodState.from_dict(new_state)

    def move_home(self, c, i, position):
        # type: (AmphipodState, str, int, Point) -> Optional[AmphipodState]
        """
        Given an amphipod in the hall, move it home if possible. This isn't iterable
        because there's only one possible move.
        """
        target_y = -4
        while target_y < 0:
            value_at_target = self.at_point(Point(home_x_positions[c], target_y))
            # If the character at the target position is a character that isn't at
            # home, return None because we can't move into the room.
            if value_at_target is None:
                # There is nothing at this location so it is the target location.
                break
            if value_at_target != c:
                return None
            # This is a character at home so look in the next higher slot.
            target_y += 1

        # At this point, target_y is the highest open spot in the room and all the lower
        # slots are characters at home.
        for testX in range(position.x - 1, home_x_positions[c], -1) if position.x > home_x_positions[c] else range(
                position.x + 1, home_x_positions[c]):
            # Look to see if there's something between here and the home position.
            if self.at_point(Point(testX, 0)):
                return None
        return self.replace_position(c, home_x_positions[c], target_y, i)

    def move_to_hall(self, c, i, position):
        # type: (AmphipodState, str, int, Point) -> Iterable[Optional[AmphipodState]]
        """
        Given an amphipod in a side room, return any hall positions it can move to.
        """
        if position.y < -1 and self.at_point(Point(position.x, position.y + 1)) is not None:
            # There's something above this in the room so it can't move.
            return None
        if position.x == home_x_positions[c]:
            # This is in its home room and there's nothing above it. If everything below it
            # is in it's home room, it can't move.
            if all(self.at_point(Point(position.x, y)) == c for y in range(position.y - 1, -5, -1)):
                return None

        # At this point we know the amphipod can get out of the room. Now we return all the
        # hallway positions it can reach.
        for testX in range(position.x - 1, -1, -1):
            # Look at the positions to the left.
            if Point(testX, 0) in self.all_positions():
                # If we've encountered another amphipod in the hall, stop looking in this direction.
                break
            if testX in hall_x_positions:
                yield self.replace_position(c, testX, 0, i)
        for testX in range(position.x + 1, 11):
            # Look at the positions to the right.
            if Point(testX, 0) in self.all_positions():
                # If we've encountered another amphipod in the hall, stop looking in this direction.
                break
            if testX in hall_x_positions:
                yield self.replace_position(c, testX, 0, i)

    def Successors(self) -> Iterable[AmphipodState]:
        # Find amphipods in side rooms that can move to the hall.
        dict = self.as_dict()
        for c in dict:
            for i, position in enumerate(dict[c]):
                if position.y == 0:
                    # This one is in the hall so see if it can move home.
                    newState = self.move_home(c, i, position)
                    if newState is not None:
                        yield newState
                else:
                    # This one is in a side room so see if it can move to the hall.
                    for s in self.move_to_hall(c, i, position):
                        if s:
                            yield s
