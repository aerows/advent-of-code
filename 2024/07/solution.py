import typing as t
from pathlib import Path
from dataclasses import dataclass, field
import itertools as it


@dataclass
class Operator:
    name: str
    sign: str
    op: t.Callable[[int, int], int]

    def __repr__(self):
        return self.sign


@dataclass
class Eq:
    total: int = 0
    operands: t.List[int] = field(default_factory=list)

    @property
    def nOperands(self) -> int:
        return len(self.operands)

    def print(self, operators: t.List[Operator]):
        assert len(operators) == self.nOperands - 1
        operandsString = str(self.operands[0])
        for operator, operand in zip(operators, self.operands[1:]):
            operandsString = operandsString + f" {operator.sign} {operand}"
        print(f"  {self.total} = {operandsString}")


def parse(inputString: str):
    data: t.List[Eq] = list()
    for line in inputString.splitlines():
        totalStr, operandStr = line.split(": ")
        operands = list(map(int, operandStr.strip().split(" ")))
        data.append(Eq(total=int(totalStr), operands=operands))
    return data


def solve(
    eq: Eq, operatorSet: t.List[Operator], dropLarge: bool = True
) -> t.List[t.List[Operator]]:
    result: t.List[t.List[Operator]] = list()
    for operators in it.product(operatorSet, repeat=eq.nOperands - 1):
        # print(len(eq.operands), len(operators))
        current = eq.operands[0]
        for operand, operator in zip(eq.operands[1:], operators):
            current = operator.op(current, operand)
            if current > eq.total and dropLarge:
                continue
        if current == eq.total:
            result.append(operators)

    return result


def solve1(input: str) -> int:
    data = parse(input)
    total = 0

    operatorSet = [
        Operator("add", "+", lambda a, b: a + b),
        Operator("mul", "x", lambda a, b: a * b),
    ]
    for idx, eq in enumerate(data):
        solutions = solve(eq, operatorSet=operatorSet)
        if solutions:
            print(f"Found {len(solutions)} for eq {idx+1}")
            for solution in solutions:
                eq.print(solution)
            total += eq.total
    return total


def solve2(input: str) -> int:
    data = parse(input)
    total = 0

    operatorSet = [
        Operator("add", "+", lambda a, b: a + b),
        Operator("mul", "x", lambda a, b: a * b),
        Operator("con", "||", lambda a, b: int(str(a) + str(b))),
    ]
    for idx, eq in enumerate(data):
        solutions = solve(eq, operatorSet=operatorSet)
        if solutions:
            print(f"Found {len(solutions)} for eq {idx+1}")
            for solution in solutions:
                eq.print(solution)
            total += eq.total
    return total


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

    # run(solve1, testString, expected=3749)
    # run(solve1, dataString)
    # run(solve2, testString, expected=11387)
    run(solve2, dataString)
