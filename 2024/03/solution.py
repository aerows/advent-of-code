import typing as t
from pathlib import Path
import re


def parse(inputString: str):
    regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    matches = regex.findall(inputString)
    return [(int(a), int(b)) for a, b in matches]


def parse2(inputString: str):
    regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))")
    enabled = True
    matches = regex.findall(inputString)
    data: t.List[t.Tuple[int, int]] = list()
    for f1, f2, do, dont in matches:
        if do:
            enabled = True
            continue
        if dont:
            enabled = False
            continue
        if enabled:
            data.append((int(f1), int(f2)))

    return data


def solve1(input: str) -> int:
    print(input)
    data = parse(input)
    print(data)
    return sum(a * b for a, b in data)


def solve2(input: str) -> int:
    print(input)
    data = parse2(input)
    print(data)
    return sum(a * b for a, b in data)


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
    testString2 = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )

    # run(solve1, testString, 161)
    # run(solve1, dataString)
    run(solve2, testString2, 48)
    run(solve2, dataString)
