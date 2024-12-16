from collections import defaultdict
import pydantic
import typing as t
from pathlib import Path


class Position(t.NamedTuple):
    row: int
    col: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.row + other.row, self.col + other.col)

    def __repr__(self):
        return f"P({self.row}, {self.col})"


DIRECTIONS = [
    Position(-1, 0),
    Position(0, 1),
    Position(1, 0),
    Position(0, -1),
]
DIRECTION_2_INDEX = {direction: idx for idx, direction in enumerate(DIRECTIONS)}
DIRECTION_NAMES = ["Up", "Right", "Down", "Left"]
DIRECTION_2_NAME = {
    direction: DIRECTION_NAMES[idx] for idx, direction in enumerate(DIRECTIONS)
}


def setCharAt(string: str, pos: int, char: str):
    return string[:pos] + char + string[pos + 1 :]


class Model(pydantic.BaseModel):
    height: int
    width: int
    startingPosition: Position
    obsticles: t.Set[Position]

    def withinBounds(self, pos: Position):
        return (
            pos.row >= 0
            and pos.col >= 0
            and pos.row < self.height
            and pos.col < self.width
        )

    def modelCopyWithStart(self, start: Position) -> "Model":
        return Model(
            height=self.height,
            width=self.width,
            startingPosition=start,
            obsticles=self.obsticles.copy(),
        )

    def isOccupied(self, pos: Position):
        return pos in self.obsticles

    def print(
        self,
        position: t.Optional[Position] = None,
        extraObsticles: t.Optional[t.Set[Position]] = None,
    ):
        _map = ["." * self.width for _ in range(self.height)]
        position = position or self.startingPosition
        _map[position.row] = setCharAt(_map[position.row], position.col, "^")
        for obsticle in self.obsticles:
            _map[obsticle.row] = setCharAt(_map[obsticle.row], obsticle.col, "#")
        for obsticle in extraObsticles or set():
            _map[obsticle.row] = setCharAt(_map[obsticle.row], obsticle.col, "O")

        print("\n".join(_map))


def parse(inputString: str) -> Model:
    lines = inputString.split("\n")
    model = Model(
        height=len(lines),
        width=len(lines[0]),
        startingPosition=Position(-1, -1),
        obsticles=set(),
    )
    for rowIdx, line in enumerate(lines):
        for colIdx, char in enumerate(line):
            if char == "#":
                model.obsticles.add(Position(rowIdx, colIdx))
            if char == "^":
                model.startingPosition = Position(rowIdx, colIdx)

    return model


def solve1(input: str) -> int:
    model = parse(input)
    pos = model.startingPosition
    directionIdx = 0
    visited: t.Set[Position] = set()
    while model.withinBounds(pos):
        visited.add(pos)
        step = DIRECTIONS[directionIdx]
        nextPos = pos + step
        if not model.isOccupied(nextPos):
            pos = nextPos
            continue
        directionIdx = (directionIdx + 1) % len(DIRECTIONS)

    return len(visited)


def walkPath(model: Model, startDirection: Position):
    visitedWithDirections: t.Dict[Position, t.Set[int]] = defaultdict(set)
    pos = model.startingPosition
    directionIdx = DIRECTION_2_INDEX[startDirection]

    while model.withinBounds(pos):
        step = DIRECTIONS[directionIdx]
        if step in visitedWithDirections[pos]:
            return pos, step
        visitedWithDirections[pos].add(step)

        nextPos = pos + step
        if not model.isOccupied(nextPos):
            pos = nextPos
            continue
        directionIdx = (directionIdx + 1) % len(DIRECTIONS)
    return None


def solve2(input: str) -> int:
    model = parse(input)
    pos = model.startingPosition
    directionIdx = 0
    visitedWithDirections: t.Dict[Position, t.List[int]] = defaultdict(list)

    newObsticles: t.Set[Position] = set()

    while model.withinBounds(pos):
        step = DIRECTIONS[directionIdx]

        nextPosition = pos + step

        if (
            not model.isOccupied(nextPosition)
            and nextPosition not in newObsticles
            and not visitedWithDirections[nextPosition]
        ):
            # Original model already has obsticle

            modelCopy = model.modelCopyWithStart(pos)
            modelCopy.obsticles.add(nextPosition)
            res = walkPath(model=modelCopy, startDirection=step)
            if res is not None:
                newObsticles.add(nextPosition)

        visitedWithDirections[pos].append(step)

        if not model.isOccupied(nextPosition):
            pos = nextPosition
            continue
        directionIdx = (directionIdx + 1) % len(DIRECTIONS)

    if model.startingPosition in newObsticles:
        newObsticles.remove(model.startingPosition)
    model.print(extraObsticles=newObsticles)

    return len(newObsticles)


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

    # run(solve1, testString, expected=41)
    # run(solve1, dataString)
    # run(solve2, testString, expected=6)
    run(solve2, dataString)
