import re
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import numpy.typing as npt


# === Utility and constants ===================================================

Vector = t.Annotated[npt.NDArray[np.int32], (2,)]


@dataclass
class Robot:
    pos: Vector
    vel: Vector

    def __repr__(self):
        return f"p={self.pos[0]},{self.pos[1]} v={self.vel[0]},{self.vel[1]}"


# === Model ================================================================


@dataclass
class Stage:
    size: Vector
    robots: t.List[Robot] = field(default_factory=list)

    def step(self, n: int) -> "Stage":
        stage = Stage(self.size)

        for robot in self.robots:
            newPos = robot.pos + robot.vel * n
            newPos %= self.size
            stage.robots.append(Robot(newPos, robot.vel))
        return stage

    def __repr__(self):
        intMap = [[0 for _ in range(self.size[0])] for _ in range(self.size[1])]
        for robot in self.robots:
            x, y = robot.pos
            intMap[y][x] += 1
        strMap = [[str(min(9, v)) if v else " " for v in intRow] for intRow in intMap]
        return "\n".join(["".join(row) for row in strMap])

    def securityFactor(self) -> int:
        midPoint = self.size // 2
        preFactor = [r.pos - midPoint for r in self.robots]

        result = 1
        quadrants = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        for quadrant in quadrants:
            quadResult = sum(all(pos * quadrant > (0, 0)) for pos in preFactor)
            print(f"{quadrant}: {quadResult}")
            result *= quadResult
        return result


# === Parsing ==============================================================


def parse(inputString: str, size: Vector = None) -> Stage:
    if size is None:
        size = np.array([11, 7])
    stage = Stage(size=size)
    for match in re.finditer(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", inputString):
        p_x, p_y, v_x, v_y = match.groups()
        robot = Robot(np.array([int(p_x), int(p_y)]), np.array([int(v_x), int(v_y)]))
        stage.robots.append(robot)

    return stage


# === Solving ===============================================================


def solve1(input: str) -> int:
    # stage = parse(input, np.array([11, 7]))
    stage = parse(input, np.array([101, 103]))
    print(stage)
    stage = stage.step(100)
    print(stage)
    score = stage.securityFactor()

    return score


def solve2(_input: str) -> int:
    import os

    stage = parse(_input, np.array([101, 103]))
    delta = 1
    try:
        n = 0
        while True:
            os.system("clear")
            print(stage.step(n))
            res = input(f"Count at {n} Press enter")
            if not res:
                n += delta
            else:
                try:
                    delta = int(res)
                    n += delta
                except ValueError:
                    print(f"{res} is not an integer")
    except KeyboardInterrupt:
        pass
    return 0


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

    # run(solve1, testString, expected=None)
    # run(solve1, dataString, expected=221142636)
    # run(solve2, testString, expected=None)
    run(solve2, dataString)
