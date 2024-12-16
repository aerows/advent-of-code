import typing as t
from pathlib import Path
from collections import defaultdict


def parse(inputString: str):
    orderingStr, contentStr = inputString.split("\n\n")

    def parseOrdering(s: str) -> t.Tuple[int, int]:
        a, b = s.strip().split("|")
        return int(a), int(b)

    def parseContent(s: str) -> t.List[int]:
        return list(map(int, s.split(",")))

    orderings = list(map(parseOrdering, orderingStr.strip().split("\n")))
    # print(orderings)
    contents = list(map(parseContent, contentStr.strip().split("\n")))

    leading = defaultdict(list)
    trailing = defaultdict(list)

    for first, second in orderings:
        trailing[first].append(second)
        leading[second].append(first)

    return contents, leading, trailing


def validateContent(
    content: t.List[int],
    leading: t.Dict[int, t.List[int]],
    trailing: t.Dict[int, t.List[int]],
):
    for idx, number in enumerate(content):
        leadingNumbers = content[:idx]
        for leadingNumber in leadingNumbers:
            if leadingNumber in trailing[number]:
                print(f"{leadingNumber} came before {number}")
                return False

        trailingNumbers = content[idx + 1 :]
        for trailingNumber in trailingNumbers:
            if trailingNumber in leading[number]:
                print(f"{trailingNumber} came after {number}")
                return False
    return True


def solve1(input: str) -> int:
    contents, leading, trailing = parse(input)
    total = 0
    for idx, content in enumerate(contents):
        valid = validateContent(content, leading, trailing)
        if not valid:
            print(f"Row {idx} is not valid: {content}")
            continue
        print(f"Row {idx} is valid: {content}")
        middleIndex = len(content) // 2
        middleNumber = content[middleIndex]
        print(f"Middle number: {middleNumber}")
        total += content[middleIndex]
    return total


def reorderContent(
    content: t.List[int],
    leading: t.Dict[int, t.List[int]],
    trailing: t.Dict[int, t.List[int]],
):
    numberToIndex = defaultdict(int)

    for number in content:
        order = sum(1 for num in content if num in leading[number])
        numberToIndex[order] = number

    middleIndex = len(content) // 2
    return numberToIndex[middleIndex]


def solve2(input: str) -> int:
    contents, leading, trailing = parse(input)
    total = 0
    for idx, content in enumerate(contents):
        valid = validateContent(content, leading, trailing)
        if valid:
            continue
        val = reorderContent(content, leading, trailing)
        total += val
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

    # run(solve1, testString, expected=143)
    # run(solve1, dataString)
    # run(solve2, testString, expected=123)
    run(solve2, dataString)
