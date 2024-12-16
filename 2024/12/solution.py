from dataclasses import dataclass, field
from itertools import product
import typing as t
from pathlib import Path

from coord import Coord


@dataclass
class Model:
    patches: t.List[str]

    @property
    def height(self) -> int:
        return len(self.patches)

    @property
    def width(self) -> int:
        return len(self.patches[0])

    def withinBounds(self, coord: Coord) -> bool:
        return (
            coord.row >= 0
            and coord.col >= 0
            and coord.row < self.height
            and coord.col < self.width
        )

    def __getitem__(self, key: Coord) -> str:
        return self.patches[key.row][key.col]


@dataclass
class Region:
    letter: str
    plots: t.Set[Coord] = field(default_factory=set)


def parse(inputString: str) -> Model:
    return Model(patches=inputString.splitlines())


DIRECTIONS = [Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)]


def getNeighbours(
    coord: Coord, outOf: t.Optional[t.Collection[Coord]] = None
) -> t.Set[Coord]:
    neighbours = set([coord + direction for direction in DIRECTIONS])
    if not outOf:
        return neighbours
    return set([n for n in neighbours if n in outOf])


def floodFill(coord: Coord, model: Model) -> Region:
    region = Region(letter=model[coord])
    region.plots.add(coord)

    candidates = getNeighbours(coord)
    while candidates:
        nextCandidates: t.Set[Coord] = set()

        for candidate in candidates:
            if candidate in region.plots:
                continue
            if not model.withinBounds(candidate):
                continue
            if model[candidate] != region.letter:
                continue

            region.plots.add(candidate)
            nextCandidates |= getNeighbours(candidate)
        candidates = nextCandidates
    return region


def regionCost(region: Region) -> int:
    perimiter = 0
    for plot in region.plots:
        perimiter += sum(1 for n in getNeighbours(plot) if n not in region.plots)
    return perimiter * len(region.plots)


def clusterAdjacent(plots: t.Set[Coord]) -> t.List[t.Set[Coord]]:
    clusters: t.List[t.Set[Coord]] = list()
    handled: t.Set[Coord] = set()
    for plot in plots:
        if plot in handled:
            continue
        cluster: t.Set[Coord] = set([plot])
        candidates: t.Set[Coord] = getNeighbours(plot, outOf=plots)
        while candidates:
            nextCandidates: t.Set[Coord] = set()
            for candidate in candidates:
                if candidate in cluster:
                    continue
                if candidate not in plots:
                    continue
                cluster.add(candidate)
                nextCandidates |= getNeighbours(candidate, outOf=plots)
            candidates = nextCandidates
        clusters.append(cluster)
        handled |= cluster
    return clusters


def regionCost2(region: Region) -> int:
    totalSides = 0
    for direction in DIRECTIONS:
        perimiterCandidates = [inlier + direction for inlier in region.plots]
        perimiterPlots = set([c for c in perimiterCandidates if c not in region.plots])
        clusters = clusterAdjacent(perimiterPlots)
        assert sum(len(c) for c in clusters) == len(perimiterPlots)
        totalSides += len(clusters)

    cost = totalSides * len(region.plots)
    print(f"{region.letter}: {len(region.plots)} X {totalSides} = {cost}")
    return cost


def segment(model: Model) -> t.List[Region]:
    visited: t.Set[Coord] = set()
    regions: t.List[Region] = list()
    for row, col in product(range(model.height), range(model.width)):
        coord = Coord(row, col)
        if coord in visited:
            continue
        region = floodFill(coord, model)
        visited |= region.plots
        regions.append(region)
    return regions


def solve1(input: str) -> int:
    model = parse(input)
    # print(model)
    regions = segment(model)
    totalCost = 0
    for region in regions:
        cost = regionCost(region)
        # print(region, cost)
        totalCost += cost
    return totalCost


def solve2(input: str) -> int:
    model = parse(input)
    # print(model)
    regions = segment(model)
    totalCost = 0
    for region in regions:
        cost = regionCost2(region)
        # print(region, cost)
        totalCost += cost
    return totalCost


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
    testString1 = solutionDirectory.joinpath("test1.txt").read_text()
    testString2 = solutionDirectory.joinpath("test2.txt").read_text()
    testString3 = solutionDirectory.joinpath("test3.txt").read_text()
    dataString = solutionDirectory.joinpath("data.txt").read_text()

    # run(solve1, testString1, expected=140)
    # run(solve1, testString2, expected=772)
    # run(solve1, testString3, expected=1930)

    # run(solve1, dataString)

    # run(solve2, testString1, expected=80)
    # run(solve2, testString2, expected=436)
    # run(solve2, testString3, expected=1206)

    run(solve2, dataString)
