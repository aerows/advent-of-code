import typing as t
from pathlib import Path

import numpy as np


def parse(inputString: str):
    return inputString.split("\n")


directions = [
    np.array(coord)
    for coord in [
        (-1, +1),
        (-1, +0),
        (-1, -1),
        (+0, +1),
        (-0, -1),
        (+1, +1),
        (+1, +0),
        (+1, -1),
    ]
]


def getWordAtCordInDirection(data, rowIdx, colIdx, direction) -> t.Optional[str]:
    charIdx = np.array([rowIdx, colIdx])
    word = ""
    for charNr in range(4):
        rowIdx, colIdx = charIdx + direction * charNr
        if rowIdx < 0 or rowIdx >= len(data):
            return None
        row = data[rowIdx]
        if colIdx < 0 or colIdx >= len(row):
            return None
        word += row[colIdx]
    return word


def getXAtCoord(
    data, rowIdx, colIdx, diagonal: bool = False
) -> t.Optional[t.Tuple[str, str]]:
    try:
        if diagonal:
            word1 = (
                data[rowIdx - 1][colIdx - 1]
                + data[rowIdx][colIdx]
                + data[rowIdx + 1][colIdx + 1]
            )
            word2 = (
                data[rowIdx + 1][colIdx - 1]
                + data[rowIdx][colIdx]
                + data[rowIdx - 1][colIdx + 1]
            )
            return word1, word2

        word1 = (
            data[rowIdx][colIdx - 1] + data[rowIdx][colIdx] + data[rowIdx][colIdx + 1]
        )
        word2 = (
            data[rowIdx - 1][colIdx] + data[rowIdx][colIdx] + data[rowIdx + 1][colIdx]
        )
        return word1, word2
    except Exception:
        return None


def evaluateWordAtCoord(data, rowIdx, colIdx) -> int:
    if data[rowIdx][colIdx] != "X":
        return 0
    total = 0
    for direction in directions:
        word = getWordAtCordInDirection(data, rowIdx, colIdx, direction)
        if word != "XMAS":
            continue
        # print(f"Found XMAS at ({rowIdx}, {colIdx}) going {direction}")
        total += 1

    return total


def solve1(input: str) -> int:
    data = parse(input)
    print(data)
    count = 0
    for rowIdx in range(len(data)):
        for colIdx in range(len(data[rowIdx])):
            count += evaluateWordAtCoord(data, rowIdx, colIdx)

    return count


def evaluateXAtCoord(data, rowIdx, colIdx) -> int:
    res = getXAtCoord(data, rowIdx, colIdx, diagonal=True)
    if res is None:
        return 0
    word1, word2 = res
    # print(word1, word2)
    if word1 != "MAS" and word1 != "SAM":
        return 0
    if word2 != "MAS" and word2 != "SAM":
        return 0
    print(f"Found X-MAS at {rowIdx}, {colIdx}")
    return 1


def solve2(input: str) -> int:
    data = parse(input)
    print(data)
    count = 0
    for rowIdx in range(1, len(data) - 1):
        for colIdx in range(1, len(data[rowIdx]) - 1):
            count += evaluateXAtCoord(data, rowIdx, colIdx)

    return count


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

    # run(solve1, testString, expected=18)
    # run(solve1, dataString)
    # run(solve2, testString, expected=9)
    run(solve2, dataString, expected=1976)
