import typing as t
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Block:
    startIndex: int
    length: int
    id: int = -1

    @property
    def isFile(self) -> bool:
        return self.id != -1

    def __repr__(self):
        if self.isFile:
            return f"({self.id}) {self.startIndex}: {self.length}"

        return f"{self.startIndex}: {self.length}"


@dataclass
class Model:
    length: int
    fileBlocks: t.List[Block] = field(default_factory=list)
    freeBlocks: t.List[Block] = field(default_factory=list)

    def asIntList(self) -> t.List[int]:
        result: t.List[int] = list()
        for block in self.iterblocks():
            for _ in range(block.startIndex, block.startIndex + block.length):
                result.append(block.id)
        return result

    def iterblocks(self):
        totalLength = len(self.fileBlocks) + len(self.freeBlocks)
        for idx in range(totalLength):
            yieldFile = idx % 2 == 0
            blockIdx = idx // 2
            if yieldFile:
                yield self.fileBlocks[blockIdx]
            else:
                yield self.freeBlocks[blockIdx]

    def __repr__(self):
        modelRepr = ""
        for block in self.iterblocks():
            if block.isFile:
                modelRepr = modelRepr + str(block.id) * block.length
            else:
                modelRepr = modelRepr + "." * block.length
        return f"length: {self.length}:\n" + modelRepr


def parse(inputString: str) -> Model:
    data = list(map(int, inputString))
    model = Model(length=0)
    for idx, number in enumerate(data):
        block = Block(startIndex=model.length, length=number)
        model.length += number
        isFile = idx % 2 == 0
        if isFile:
            block.id = idx // 2
            model.fileBlocks.append(block)
        else:
            model.freeBlocks.append(block)
    print(model.freeBlocks)
    print(model.fileBlocks)
    assert len(model.fileBlocks) - 1 == len(model.freeBlocks)
    return model


def solve1(input: str) -> int:
    model = parse(input)

    intList = model.asIntList()

    print(model)

    sourcePointer = len(intList) - 1
    targetPointer = 0
    while targetPointer <= sourcePointer:
        if intList[targetPointer] != -1:
            targetPointer += 1
            continue
        if intList[sourcePointer] == -1:
            sourcePointer -= 1
            continue
        source = intList[sourcePointer]
        intList[sourcePointer] = -1
        intList[targetPointer] = source

        # print(intList)

        sourcePointer -= 1
        targetPointer += 1

    hash = 0
    for idx, id in enumerate(intList):
        if id == -1:
            break
        hash += idx * id

    return hash


def solve2(input: str) -> int:
    model = parse(input)

    intList = model.asIntList()
    freeBlocks = [Block(b.startIndex, b.length) for b in model.freeBlocks]

    for block in reversed(model.fileBlocks):
        # print("".join([str(i) if i != -1 else "." for i in intList]))
        # print(freeBlocks)
        targetFreeBlockIdx: t.Optional[int] = None
        for freeBlockIdx, freeBlock in enumerate(freeBlocks):
            if freeBlock.startIndex > block.startIndex:
                break
            if freeBlock.length >= block.length:
                targetFreeBlockIdx = freeBlockIdx
                break
        if targetFreeBlockIdx is None:
            continue

        freeBlock = freeBlocks[targetFreeBlockIdx]

        # Move file block
        for idx in range(block.length):
            source = intList[block.startIndex + idx]
            intList[block.startIndex + idx] = -1
            intList[freeBlock.startIndex + idx] = source

        # Update spaces
        lengthDiff = freeBlock.length - block.length
        if lengthDiff == 0:
            freeBlocks.pop(targetFreeBlockIdx)
            # Or set length to zero
        else:
            newFreeBlock = Block(freeBlock.startIndex + block.length, length=lengthDiff)
            freeBlocks[targetFreeBlockIdx] = newFreeBlock

    # print("".join([str(i) if i != -1 else "." for i in intList]))
    hash = 0
    for idx, id in enumerate(intList):
        if id == -1:
            continue
        hash += idx * id

    return hash


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
    testString = "2333133121414131402"
    dataString = solutionDirectory.joinpath("data.txt").read_text()

    # run(solve1, testString, expected=1928)
    # run(solve1, dataString)
    # run(solve2, testString, expected=2858)
    run(solve2, dataString)
