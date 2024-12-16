import typing as t
from pathlib import Path
from collections import defaultdict


def parse(inputString: str):
    def parseLine(line: str) -> t.Tuple[int, int]:
        res = list(map(int, line.split()))
        return res

    return list(
        zip(*[parseLine(line) for line in inputString.split("\n") if line.strip()])
    )


def solve1(input: str) -> int:
    list1, list2 = parse(input)
    list1 = sorted(list1)
    list2 = sorted(list2)
    return sum(abs(a - b) for a, b in zip(list1, list2))


def solve2(input: str) -> int:
    list1, list2 = parse(input)
    counts = defaultdict(int)
    for number in list2:
        counts[number] += 1
    return sum(number * counts[number] for number in list1)


if __name__ == "__main__":
    solutionDirectory = Path(__file__).parent
    print(
        f'Solution 1 (test):{solve1((solutionDirectory / "data-01-test.txt").read_text())}'
    )
    print(
        f'Solution 1:       {solve1((solutionDirectory / "data-01.txt").read_text())}'
    )
    print(
        f'Solution 2 (test):{solve2((solutionDirectory / "data-01-test.txt").read_text())}'
    )
    print(
        f'Solution 2:       {solve2((solutionDirectory / "data-01.txt").read_text())}'
    )
