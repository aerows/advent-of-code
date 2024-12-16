import math
from collections import defaultdict
import typing as t
from pathlib import Path


def parse(inputString: str) -> t.List[int]:
    return [int(cmp) for cmp in inputString.split(" ")]


def solve1(input: str, iterations: t.Optional[int]) -> int:
    cache: Cache = defaultdict(int)
    iterations = 25
    model = parse(input)
    print(model)
    res = 0
    for value in model:
        stones = stonesAfterBlinks(value, iterations, cache)
        print(f"{value}: {stones}")
        res += stones
    print(f"Cache size: {len(cache)}")
    return res


Cache = t.Dict[t.Tuple[int, int], int]


def splitNumber(val: int) -> t.Optional[t.Tuple[int, int]]:
    digits = math.floor(math.log10(val)) + 1
    if digits % 2 == 1:
        return None
    denom = 10 ** (digits // 2)
    return val // denom, val % denom


def stonesAfterBlinks(value: int, blinks: int, cache: t.Optional[Cache] = None) -> int:
    if cache and (value, blinks) in cache:
        return cache[value, blinks]

    if blinks == 0:
        return 1

    if value == 0:
        res = stonesAfterBlinks(1, blinks - 1, cache)
        cache[1, blinks - 1] = res
        return res

    if evenParts := splitNumber(value):
        first = stonesAfterBlinks(evenParts[0], blinks - 1, cache)
        cache[evenParts[0], blinks - 1] = first
        second = stonesAfterBlinks(evenParts[1], blinks - 1, cache)
        cache[evenParts[1], blinks - 1] = second
        return first + second

    res = stonesAfterBlinks(value * 2024, blinks - 1, cache)
    cache[value * 2024, blinks - 1] = res
    return res


def solve2(input: str, opt) -> int:
    cache: Cache = defaultdict(int)
    iterations = 75
    model = parse(input)
    print(model)
    res = 0
    for value in model:
        stones = stonesAfterBlinks(value, iterations, cache)
        print(f"{value}: {stones}")
        res += stones
    print(f"Cache size: {len(cache)}")
    return res


def run(
    func: t.Callable[[str, t.Optional[int]], int],
    data: str,
    expected: t.Optional[int] = None,
    extra: t.Optional[int] = None,
):
    res = func(data, extra)
    if expected is None:
        print(f"{func.__name__} returned: {res}")
        return
    if res == expected:
        print(f"Success! {func.__name__} returned {res}")
    else:
        print(f"{func.__name__} returned {res} (expected: {expected})")


if __name__ == "__main__":
    solutionDirectory = Path(__file__).parent
    testString = "125 17"
    dataString = solutionDirectory.joinpath("data.txt").read_text()

    assert splitNumber(1213) == (12, 13), f"12,13 was {splitNumber(1213)}"
    assert splitNumber(9) is None

    # run(solve1, testString, expected=55312)
    # run(solve1, dataString)
    # run(solve2, testString, expected=None)
    run(solve2, dataString)
