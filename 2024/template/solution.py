import typing as t
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Model: ...


def parse(inputString: str) -> Model:
    return None


def solve1(input: str) -> int:
    return 0


def solve2(input: str) -> int:
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

    run(solve1, testString, expected=None)
    # run(solve1, dataString)
    # run(solve2, testString, expected=None)
    # run(solve2, dataString)
