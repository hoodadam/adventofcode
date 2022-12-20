import re
from dataclasses import dataclass
from typing import Tuple, List, Set


@dataclass(frozen=True)
class Blueprint:
    ore_cost: int
    clay_cost: int
    obsidian_cost: Tuple[int, int]
    geode_cost: Tuple[int, int]

    @property
    def max_ore_cost(self):
        obsidian_ore_cost, _ = self.obsidian_cost
        geode_ore_cost, _ = self.geode_cost
        return max(self.ore_cost, self.clay_cost, obsidian_ore_cost, geode_ore_cost)

    @property
    def max_clay_cost(self):
        _, obsidian_clay_cost = self.obsidian_cost
        return obsidian_clay_cost

    @property
    def max_obsidian_cost(self):
        _, geode_obsidian_cost = self.geode_cost
        return geode_obsidian_cost


_NUM_PATTERN = re.compile("[0-9]+")


def parse_blueprint(blueprint: str) -> Blueprint:
    numbers = [int(s) for s in _NUM_PATTERN.findall(blueprint)]
    return Blueprint(
        ore_cost=numbers[1],
        clay_cost=numbers[2],
        obsidian_cost=(numbers[3], numbers[4]),
        geode_cost=(numbers[5], numbers[6]),
    )

@dataclass(frozen=True)
class State:
    ore: int
    clay: int
    obsidian: int
    geode: int

    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int

    time: int

    def all_possible_new_states(self, blueprint: Blueprint) -> List['State']:
        # Ore robot:
        result = []
        self._build_ore_robot(blueprint, result)
        self._build_clay_robot(blueprint, result)
        self._build_obsidian_robot(blueprint, result)
        self._build_geode_robot(blueprint, result)
        return result

    def stop_building(self) -> int:
        return self.geode + self.time * self.geode_robots

    def _build_ore_robot(self, blueprint: Blueprint, result: List['State']) -> None:
        if self.ore_robots * self.time + self.ore >= blueprint.max_ore_cost * self.time:
            return

        time_to_construct = (
            (blueprint.ore_cost - self.ore - 1) // self.ore_robots + 2
            if blueprint.ore_cost > self.ore
            else 1
        )
        if time_to_construct < self.time:
            result.append(
                State(
                    ore=self.ore + self.ore_robots * time_to_construct - blueprint.ore_cost,
                    clay=self.clay + self.clay_robots * time_to_construct,
                    obsidian=self.obsidian + self.obsidian_robots * time_to_construct,
                    geode=self.geode + self.geode_robots * time_to_construct,
                    ore_robots=self.ore_robots + 1,
                    clay_robots=self.clay_robots,
                    obsidian_robots=self.obsidian_robots,
                    geode_robots=self.geode_robots,
                    time=self.time - time_to_construct
                )
            )

    def _build_clay_robot(self, blueprint: Blueprint, result: List['State']) -> None:
        if self.clay_robots * self.time + self.clay >= blueprint.max_clay_cost * self.time:
            return

        time_to_construct = (
            (blueprint.clay_cost - self.ore - 1) // self.ore_robots + 2
            if blueprint.clay_cost > self.ore
            else 1
        )
        if time_to_construct < self.time:
            result.append(
                State(
                    ore=self.ore + self.ore_robots * time_to_construct - blueprint.clay_cost,
                    clay=self.clay + self.clay_robots * time_to_construct,
                    obsidian=self.obsidian + self.obsidian_robots * time_to_construct,
                    geode=self.geode + self.geode_robots * time_to_construct,
                    ore_robots=self.ore_robots,
                    clay_robots=self.clay_robots + 1,
                    obsidian_robots=self.obsidian_robots,
                    geode_robots=self.geode_robots,
                    time=self.time - time_to_construct
                )
            )

    def _build_obsidian_robot(self, blueprint: Blueprint, result: List['State']) -> None:
        if self.clay_robots == 0:
            return

        if self.obsidian_robots * self.time + self.obsidian >= blueprint.max_obsidian_cost * self.time:
            return

        ore_cost, clay_cost = blueprint.obsidian_cost
        time_for_ore = (
            (ore_cost - self.ore - 1) // self.ore_robots + 2
            if ore_cost > self.ore
            else 1
        )
        time_for_clay = (
            (clay_cost - self.clay - 1) // self.clay_robots + 2
            if clay_cost > self.clay
            else 1
        )
        time_to_construct = max(time_for_ore, time_for_clay)
        if time_to_construct < self.time:
            result.append(
                State(
                    ore=self.ore + self.ore_robots * time_to_construct - ore_cost,
                    clay=self.clay + self.clay_robots * time_to_construct - clay_cost,
                    obsidian=self.obsidian + self.obsidian_robots * time_to_construct,
                    geode=self.geode + self.geode_robots * time_to_construct,
                    ore_robots=self.ore_robots,
                    clay_robots=self.clay_robots,
                    obsidian_robots=self.obsidian_robots + 1,
                    geode_robots=self.geode_robots,
                    time=self.time - time_to_construct
                )
            )

    def _build_geode_robot(self, blueprint: Blueprint, result: List['State']) -> None:
        if self.obsidian_robots == 0:
            return

        ore_cost, obsidian_cost = blueprint.geode_cost
        time_for_ore = (
            (ore_cost - self.ore - 1) // self.ore_robots + 2
            if ore_cost > self.ore
            else 1
        )
        time_for_obsidian = (
            (obsidian_cost - self.obsidian - 1) // self.obsidian_robots + 2
            if obsidian_cost > self.obsidian
            else 1
        )
        time_to_construct = max(time_for_ore, time_for_obsidian)
        if time_to_construct < self.time:
            result.append(
                State(
                    ore=self.ore + self.ore_robots * time_to_construct - ore_cost,
                    clay=self.clay + self.clay_robots * time_to_construct,
                    obsidian=self.obsidian + self.obsidian_robots * time_to_construct - obsidian_cost,
                    geode=self.geode + self.geode_robots * time_to_construct,
                    ore_robots=self.ore_robots,
                    clay_robots=self.clay_robots,
                    obsidian_robots=self.obsidian_robots,
                    geode_robots=self.geode_robots + 1,
                    time=self.time - time_to_construct
                )
            )


def optimize_blueprint(blueprint: Blueprint, time: int) -> int:
    possible_states: List[Set[State]] = [set() for _ in range(time + 1)]
    possible_states[time] = {State(0, 0, 0, 0, 1, 0, 0, 0, time)}
    best_outcome = 0
    for t in range(time, -1, -1):
        for state in possible_states[t]:
            best_outcome = max(best_outcome, state.stop_building())
            for s in state.all_possible_new_states(blueprint):
                possible_states[s.time].add(s)

    return best_outcome