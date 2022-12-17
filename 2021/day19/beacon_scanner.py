DATA_FILE = 'data/actual.txt'


class Location:
    def __init__(self, x, y, z):
        # type: (Location, int, int, int) -> None
        self.x = x
        self.y = y
        self.z = z

    def dist(self, other):
        # type: (Location, Location) -> int
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def get_rotation(self, i):
        # type: (Location, int) -> Location
        x, y, z = self.x, self.y, self.z
        a = i // 8
        if a == 1:
            x, y, z = y, z, x
        elif a == 2:
            x, y, z = z, x, y

        b = (i % 8) // 2
        if b == 1:
            x, y = -x, -y
        if b == 2:
            x, z = -x, -z
        if b == 3:
            y, z = -y, -z

        c = i % 2
        if c == 1:
            x, y, z = -z, -y, -x

        return Location(x, y, z)

    def __eq__(self, other):
        return isinstance(other, Location) and self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return self.x * 1000000 + self.y * 1000 + self.z

    def __repr__(self):
        return f'({self.x},{self.y},{self.z})'


class Universe:
    def __init__(self, beacons):
        # type: (Universe, list[Location]) -> None
        self.beacons = set(beacons)
        self.scanners = [Location(0, 0, 0)]
        pass

    def assimilate(self, other_universe):
        # type: (Universe, Universe) -> bool
        for known_beacon in self.beacons:
            for i in range(24):
                unknown_beacons = [beacon.get_rotation(i) for beacon in other_universe.beacons]
                for unknown_beacon in unknown_beacons:
                    dx, dy, dz = (
                        unknown_beacon.x - known_beacon.x,
                        unknown_beacon.y - known_beacon.y,
                        unknown_beacon.z - known_beacon.z
                    )
                    transformed_beacons = {
                        Location(beacon.x - dx, beacon.y - dy, beacon.z - dz) for beacon in unknown_beacons
                    }
                    matches = len(transformed_beacons.intersection(self.beacons))
                    if matches >= 12:
                        self.beacons.update(transformed_beacons)
                        self.scanners.append(Location(dx, dy, dz))
                        return True
        return False


def parse_beacons(scanner):
    # type: (str) -> list[Location]
    return [Location(*(int(s) for s in line.split(','))) for line in scanner.splitlines()[1:]]


with open(DATA_FILE) as f:
    raw_data = f.read()

universes = [Universe(parse_beacons(scanner)) for scanner in raw_data.split('\n\n')]
n = len(universes)
unassimilated = set(range(1, n))


def merge_two_universes():
    # type: () -> None
    for i in range(n - 1):
        if i > 0 and i not in unassimilated:
            continue
        for j in unassimilated:
            if i == j:
                continue
            if universes[i].assimilate(universes[j]):
                unassimilated.remove(j)
                return
    raise AssertionError('Failed to merge any universes')


while unassimilated:
    merge_two_universes()
    print(f'{len(unassimilated)} universes left to assimilate')

full_universe = universes[0]
print(f'{len(full_universe.beacons)} total beacons')

max_dist = max(scanner1.dist(scanner2) for scanner1 in full_universe.scanners for scanner2 in full_universe.scanners)
print(f'Max distance: {max_dist}')
