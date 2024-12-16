import itertools
import typing as t
from pathlib import Path
from dataclasses import dataclass, field


# === Utility and constants ===================================================


class Coord(t.NamedTuple):
    row: int
    col: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.row + other.row, self.col + other.col)


Direction = Coord
UP = Direction(-1, 0)
DOWN = Direction(+1, 0)
LEFT = Direction(0, -1)
RIGHT = Direction(0, +1)

SymbolToDirection = {"<": LEFT, "^": UP, ">": RIGHT, "v": DOWN}
DirectionToSymbol = {
    direction: symbol for symbol, direction in SymbolToDirection.items()
}


def directionsToString(directions: t.List[Direction]):
    strings = [DirectionToSymbol[direction] for direction in directions]
    return "".join(strings)


# === Model ================================================================


@dataclass
class Stage:
    nCols: int
    nRows: int
    robot: Coord
    boxes: t.Set[Coord] = field(default_factory=set)
    walls: t.Set[Coord] = field(default_factory=set)

    @classmethod
    def parseStage1(cls, rawMap: str) -> "Stage":
        rawLines = rawMap.splitlines()
        nRows, nCols = len(rawLines), len(rawLines[0])

        robot: Coord
        boxes: t.Set[Coord] = set()
        walls: t.Set[Coord] = set()

        for row, line in enumerate(rawLines):
            for col, char in enumerate(line):
                coord = Coord(row, col)
                if char == "@":
                    robot = coord
                elif char == "#":
                    walls.add(coord)
                elif char == "O":
                    boxes.add(coord)

        return Stage(nRows=nRows, nCols=nCols, robot=robot, boxes=boxes, walls=walls)

    @classmethod
    def parseStage2(cls, rawMap: str) -> "Stage":
        rawLines = rawMap.splitlines()
        nRows, nCols = len(rawLines), len(rawLines[0]) * 2

        robot: Coord
        boxes: t.Set[Coord] = set()
        walls: t.Set[Coord] = set()

        for row, line in enumerate(rawLines):
            for col, char in enumerate(line):
                if char == "@":
                    robot = Coord(row, col * 2)
                elif char == "#":
                    walls.add(Coord(row, col * 2))
                    walls.add(Coord(row, col * 2 + 1))
                elif char == "O":
                    boxes.add(Coord(row, col * 2))

        return Stage(nRows=nRows, nCols=nCols, robot=robot, boxes=boxes, walls=walls)

    def stepStage1(self, direction: Direction) -> "Stage":
        positionToCheck = self.robot + direction
        affectedBoxes: t.Set[Coord] = set()
        while True:
            if positionToCheck in self.walls:
                return self

            if positionToCheck not in self.boxes:
                break

            affectedBoxes.add(positionToCheck)
            positionToCheck = positionToCheck + direction

        newBoxes = [
            box + direction if box in affectedBoxes else box for box in self.boxes
        ]

        return Stage(
            nRows=self.nRows,
            nCols=self.nCols,
            robot=self.robot + direction,
            boxes=newBoxes,
            walls=self.walls,
        )

    def stepStage2(self, direction: Direction) -> "Stage":
        positionsToCheck: t.List[Coord] = [self.robot + direction]
        affectedBoxes: t.Set[Coord] = set()

        while positionsToCheck:
            nextPositions: t.List[Coord] = list()
            for position in positionsToCheck:
                if position in self.walls:
                    return self  # Wall, no movement

                if position in self.boxes:
                    leftPos, rightPos = position, position + RIGHT
                    if leftPos in affectedBoxes:
                        continue
                    nextPositions.append(leftPos + direction)
                    nextPositions.append(rightPos + direction)
                    affectedBoxes.add(leftPos)

                elif (position + LEFT) in self.boxes:
                    leftPos, rightPos = position + LEFT, position
                    if leftPos in affectedBoxes:
                        continue
                    nextPositions.append(leftPos + direction)
                    nextPositions.append(rightPos + direction)
                    affectedBoxes.add(leftPos)

            positionsToCheck = nextPositions

        newBoxes = [
            box + direction if box in affectedBoxes else box for box in self.boxes
        ]

        return self.__class__(
            nRows=self.nRows,
            nCols=self.nCols,
            robot=self.robot + direction,
            boxes=newBoxes,
            walls=self.walls,
        )

    def gpsScore(self) -> int:
        return sum(box.row * 100 + box.col for box in self.boxes)

    def modelToString(self, stage: t.Literal["stage1", "stage2"] = "stage1") -> str:
        result = [["." for _ in range(self.nCols)] for _ in range(self.nRows)]
        for row, col in self.boxes:
            if stage == "stage1":
                result[row][col] = "O"
            elif stage == "stage2":
                result[row][col] = "["
                result[row][col + 1] = "]"
        for row, col in self.walls:
            result[row][col] = "#"
        result[self.robot.row][self.robot.col] = "@"
        return "\n".join(["".join(row) for row in result])


# === Parsing ==============================================================


def parse(
    inputString: str, stage: t.Literal["stage1", "stage2"] = "stage1"
) -> t.Tuple["Stage", t.List[Direction]]:
    rawMap, rawInstructions = inputString.split("\n\n")

    stage = (
        Stage.parseStage1(rawMap) if stage == "stage1" else Stage.parseStage2(rawMap)
    )

    instructions: t.List[Direction] = list()
    for char in rawInstructions.replace("\n", ""):
        instruction = SymbolToDirection.get(char)
        instructions.append(instruction)

    return stage, instructions


# === Solving ===============================================================


def solve1(input: str) -> int:
    model, instructions = parse(input, "stage1")
    # print(model.modelToString("stage1"))
    for instruction in instructions:
        model = model.stepStage1(instruction)
        # print(f"Direction: {DirectionToSymbol[instruction]}\n" + str(model))
        # print(model.modelToString("stage1"))
    return model.gpsScore()


def solve2(input: str) -> int:
    model, instructions = parse(input, "stage2")
    # print(model.modelToString("stage2"))
    for instruction in instructions:
        model = model.stepStage2(instruction)
        # print(f"Direction: {DirectionToSymbol[instruction]}\n" + str(model))
        # print(model.modelToString("stage2"))
    return model.gpsScore()


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
    smallTestString = solutionDirectory.joinpath("small_test.txt").read_text()
    largeTestString = solutionDirectory.joinpath("large_test.txt").read_text()
    dataString = solutionDirectory.joinpath("data.txt").read_text()

    run(solve1, smallTestString, expected=2028)
    run(solve1, largeTestString, expected=10092)
    run(solve1, dataString, expected=10092)
    run(solve2, largeTestString, expected=9021)
    run(solve2, dataString, expected=1463160)
