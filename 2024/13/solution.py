import re
import typing as t
from pathlib import Path
from dataclasses import dataclass


class Vector(t.NamedTuple):
    x: int
    y: int

    def __add__(self, other: int) -> "Vector":
        return Vector(self.x + other, self.y + other)


@dataclass
class Case:
    A: Vector
    B: Vector
    P: Vector

    def __repr__(self):
        return str(
            f"Button A: X{self.A.x}, Y{self.A.y}\n"
            f"Button B: X{self.B.x}, Y{self.B.y}\n"
            f"Prize: X={self.P.x}, Y={self.P.y}"
        )


def parse(inputString: str) -> t.List[Case]:
    pattern = re.compile(
        r"Button A: X(.\d+), Y(.\d+)\nButton B: X(.\d+), Y(.\d+)\nPrize: X=(\d+), Y=(\d+)"
    )

    cases: t.List[Case] = list()
    for match in pattern.finditer(inputString):
        aX, aY, bX, bY, rX, rY = match.groups()
        cases.append(
            Case(
                Vector(int(aX), int(aY)),
                Vector(int(bX), int(bY)),
                Vector(int(rX), int(rY)),
            )
        )

    return cases


def solveCase(c: Case) -> int:
    # p * a_x + q * b_x = r_x
    # p * a_y + q * b_y = r_y

    # p = (r_x - q * b_x) / a_x
    # p = (r_y - q * b_y) / a_y

    # (r_x - q * b_x) / a_x = (r_y - q * b_y) / a_y
    # a_y * (r_x - q * b_x) = a_x * (r_y - q * b_y)
    # a_y * r_x - a_y * q * b_x = a_x * r_y - a_x * q * b_y
    # q * a_x * b_y - q * a_y * b_x = a_x * r_y - a_y * r_x
    # q ( a_x * b_y - a_y * b_x) = a_x * r_y - a_y * r_x
    # q = a_x * r_y - a_y * r_x / ( a_x * b_y - a_y * b_x)

    q = (c.A.x * c.P.y - c.A.y * c.P.x) / (c.A.x * c.B.y - c.A.y * c.B.x)
    p = (c.P.x - q * c.B.x) / c.A.x

    if q != int(q) or p != int(p):
        return 0

    return int(p) * 3 + int(q) * 1


def solve1(input: str) -> int:
    model = parse(input)
    totalTokens = 0
    for case in model:
        totalTokens += solveCase(case)
    return totalTokens


def solve2(input: str) -> int:
    oldModel = parse(input)
    diff = 10000000000000
    model = [Case(case.A, case.B, case.P + diff) for case in oldModel]

    totalTokens = 0
    for case in model:
        # print(case)
        totalTokens += solveCase(case)
    return totalTokens


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

    run(solve1, testString, expected=480)
    run(solve1, dataString, expected=37901)
    run(solve2, testString, expected=None)
    run(solve2, dataString, expected=77407675412647)
