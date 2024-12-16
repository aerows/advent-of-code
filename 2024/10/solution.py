import typing as t
from pathlib import Path
from dataclasses import dataclass


class Coord(t.NamedTuple):
    row: int
    col: int


@dataclass
class Model:
    elevations: t.List[t.List[int]]

    def coords(self):
        for row in range(len(self.elevations)):
            for col in range(len(self.elevations[0])):
                yield Coord(row, col)

    def neighbours(self, coord: Coord):
        candidates = [
            Coord(coord.row - 1, coord.col),
            Coord(coord.row, coord.col + 1),
            Coord(coord.row + 1, coord.col),
            Coord(coord.row, coord.col - 1),
        ]
        return [candidate for candidate in candidates if self.withinBounds(candidate)]

    def withinBounds(self, coord: Coord) -> bool:
        nRows, nCols = len(self.elevations), len(self.elevations[0])
        return (
            coord.row >= 0
            and coord.col >= 0
            and coord.row < nRows
            and coord.col < nCols
        )


def parse(inputString: str) -> Model:
    return Model(
        elevations=[[int(char) for char in line] for line in inputString.splitlines()]
    )


def findStarts(model: Model) -> t.List[Coord]:
    res: t.List[Coord] = list()
    for coord in model.coords():
        if model.elevations[coord.row][coord.col] == 0:
            res.append(coord)
    return res


def getNeighboursWithHeight(model: Model, coord: Coord, height: int) -> t.Set[Coord]:
    return set(
        [n for n in model.neighbours(coord) if model.elevations[n.row][n.col] == height]
    )


def solve1(input: str) -> int:
    model = parse(input)
    startPositions = findStarts(model)
    print(model)
    print(startPositions)

    totalTrails = 0
    for start in startPositions:
        currentElevation = 0
        currentPositions: t.Set[Coord] = set([start])
        while currentPositions and currentElevation < 9:
            nextPositions: t.Set[Coord] = set()
            for position in currentPositions:
                nextPositions |= getNeighboursWithHeight(
                    model, position, currentElevation + 1
                )
            currentPositions = nextPositions
            currentElevation += 1
        totalTrails += len(currentPositions)
        # print(f"At {start} found {len(currentPositions)} trails")

    return totalTrails


def trailsLeadingUp(model: Model, start: Coord, elevation: int) -> int:
    if elevation == 9:
        return 1
    score = 0
    for nextPosition in getNeighboursWithHeight(model, start, elevation + 1):
        score += trailsLeadingUp(model, nextPosition, elevation=elevation + 1)
    return score


def solve2(input: str) -> int:
    model = parse(input)
    startPositions = findStarts(model)
    print(model)
    print(startPositions)

    totalRatings = 0
    for start in startPositions:
        rating = trailsLeadingUp(model, start=start, elevation=0)
        print(f"{start}: {rating}")
        totalRatings += rating

    return totalRatings


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

    # run(solve1, testString, expected=36)
    # run(solve1, dataString)
    # run(solve2, testString, expected=81)
    run(solve2, dataString)
