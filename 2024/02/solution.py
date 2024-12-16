import typing as t
from pathlib import Path


def parse(inputString: str) -> t.List[t.Tuple[int, ...]]:
    lines = inputString.split("\n")

    def lineToLevel(line: str) -> t.Tuple[int]:
        return tuple(list(map(int, line.split())))

    return list(map(lineToLevel, lines))


def calculate_diffs(ints: t.Iterable[int]) -> t.Iterable[int]:
    prev = ints[0]

    for curr in ints[1:]:
        yield curr - prev
        prev = curr


def solve1(input: str) -> int:
    levels = parse(input)

    def validate_level(level: t.Tuple[int, ...]) -> bool:
        prev = None
        for diff in calculate_diffs(level):
            if abs(diff) > 3 or abs(diff) == 0:
                return False
            if prev is None:
                prev = diff
                continue
            if prev * diff < 0:
                return False
        return True

    total = 0
    for idx, level in enumerate(levels):
        res = validate_level(level)
        print(f"line {idx+1}: {['invalid', 'valid'][res]} ({level})")
        total += res

    return total


def solve2(input: str) -> int:
    levels = parse(input)

    def validate_level(level: t.Tuple[int, ...]) -> t.Tuple[bool, int]:
        prev = None
        for idx, diff in enumerate(calculate_diffs(level)):
            if abs(diff) > 3 or abs(diff) == 0:
                return False, idx
            if prev is None:
                prev = diff
                continue
            if prev * diff < 0:
                return False, idx
        return True, idx

    total = 0
    for lineNr, level in enumerate(levels):
        res, idx = validate_level(level)
        print(f"line {lineNr+1}: {['invalid', 'valid'][res]} ({idx}) ({level})")
        if res:
            total += res
            continue
        for idx in range(len(level)):
            _level = [val for _idx, val in enumerate(level) if _idx != idx]
            _res, _ = validate_level(_level)
            print(f" line {lineNr+1}:{idx}: {['invalid', 'valid'][_res]} ({_level})")
            if _res:
                total += 1
                break

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

    # run(solve1, testString, 2)
    # run(solve1, dataString)
    run(solve2, testString, 4)
    run(solve2, dataString, 363)
