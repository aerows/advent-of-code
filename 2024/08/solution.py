from collections import defaultdict
import itertools
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

from coord import Coord


@dataclass
class Antenna:
    sign: str
    coord: Coord

    def __repr__(self):
        return f"{self.sign} at: ({self.coord.row}, {self.coord.col})"


@dataclass
class Model:
    height: int
    width: int
    antennas: t.List[Antenna] = field(default_factory=list)

    def __repr__(self):
        chars = [["." for _ in range(self.width)] for _ in range(self.height)]
        for antenna in self.antennas:
            chars[antenna.coord.row][antenna.coord.col] = antenna.sign
        return "\n".join(["".join(line) for line in chars])

    def asStringWithNodes(self, nodes: t.Collection[Coord]) -> str:
        chars = [["." for _ in range(self.width)] for _ in range(self.height)]
        for node in nodes:
            chars[node.row][node.col] = "#"
        for antenna in self.antennas:
            chars[antenna.coord.row][antenna.coord.col] = antenna.sign
        return "\n".join(["".join(line) for line in chars])


def parse(inputString: str):
    lines = inputString.splitlines()
    height = len(lines)
    width = len(lines[0])
    data = Model(height, width)
    for rowIdx, line in enumerate(lines):
        for colIdx, char in enumerate(line):
            if char == ".":
                continue
            data.antennas.append(Antenna(char, Coord(rowIdx, colIdx)))
    return data


def solve1(input: str) -> int:
    model = parse(input)

    antennasBySign: t.Dict[str, t.List[Antenna]] = defaultdict(list)
    [antennasBySign[a.sign].append(a) for a in model.antennas]

    antinodes: t.Set[Coord] = set()

    for sign, antennas in antennasBySign.items():
        print(f"Calculating nodes for {sign} ({len(antennas)})")
        for firstAntenna, secondAntenna in itertools.permutations(antennas, 2):
            c1, c2 = firstAntenna.coord, secondAntenna.coord
            node = 2 * c2 - c1
            if node.row < 0 or node.col < 0:
                continue
            if node.row >= model.height or node.col >= model.width:
                continue
            antinodes.add(node)

    return len(antinodes)


def solve2(input: str) -> int:
    model = parse(input)

    antennasBySign: t.Dict[str, t.List[Antenna]] = defaultdict(list)
    [antennasBySign[a.sign].append(a) for a in model.antennas]

    antinodes: t.Set[Coord] = set()

    for sign, antennas in antennasBySign.items():
        print(f"Calculating nodes for {sign} ({len(antennas)})")
        for firstAntenna, secondAntenna in itertools.permutations(antennas, 2):
            c1, c2 = firstAntenna.coord, secondAntenna.coord
            print(f"Evaulating: {firstAntenna}, {secondAntenna}")

            delta = c1 - c2
            node = c1

            def withinBounds(node: Coord) -> bool:
                return (
                    node.row >= 0
                    and node.col >= 0
                    and node.row < model.height
                    and node.col < model.width
                )

            while withinBounds(node):
                antinodes.add(node)
                node = node + delta

            antinodes.add(c1)

    print(model.asStringWithNodes(antinodes))
    return len(antinodes)


def run(func: t.Callable[[str], int], data: str, expected: t.Optional[int] = None):
    res = func(data)
    if expected is None:
        print(f"{func.__name__} returned: {res}")
        return
    if res == expected:
        print(f"Success! {func.__name__} returned {res}")
    else:
        print(f"{func.__name__} returned {res} (expected: {expected})")


if __name__ == "__main__":
    solutionDirectory = Path(__file__).parent
    testString = solutionDirectory.joinpath("test.txt").read_text()
    dataString = solutionDirectory.joinpath("data.txt").read_text()

    # run(solve1, testString, expected=14)
    # run(solve1, dataString)
    # run(solve2, testString, expected=34)
    run(solve2, dataString)
