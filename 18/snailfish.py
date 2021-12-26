from typing import Any, Final, List, final


def get(number: List[Any], idx: List[int]) -> Any:
    n = number
    for i in idx:
        n = n[i]
    return n


def parse(line: str) -> List[Any]:
    number: List[Any] = []
    indexes: List[int] = [0]

    line = line.strip()[1:]
    for char in line:
        if char == "[":
            get(number, indexes[:-1]).append([])
            indexes.append(0)
        elif char == "]":
            indexes.pop()
        elif char == ",":
            indexes[-1] += 1
        else:
            get(number, indexes[:-1]).append(int(char))

    return number


def add_numbers(one: None | List[Any], other: List[Any]) -> List[Any]:
    if one is None:
        return other
    else:
        return [one, other]


def add_value(number: List[Any], index: List[int], positive: int,
              counter: int) -> None:
    vidx = index.copy()
    vidx.append(positive)
    value: Final = get(number, vidx)

    if not isinstance(value, int):
        raise Exception(
            f"Index {index} is {value} in {number} but must be a value")

    # If left or rightmost, return
    if len(set(index)) == 1 and index[0] == positive:
        return

    idx: List[int] = index.copy()
    while counter != idx.pop():
        continue
    idx.append(positive)

    leftidx: List[int] = []
    for i in idx:
        leftidx.append(i)
        if isinstance(get(number, leftidx), int):
            leftidx.pop()
            get(number, leftidx)[i] += value
            return

    # Deeper than provided
    while isinstance(get(number, leftidx), list):
        leftidx.append(counter)
    leftidx.pop()
    get(number, leftidx)[counter] += value


def add_left(number: List[Any], index: List[int]) -> None:
    add_value(number, index, 0, 1)


def add_right(number: List[Any], index: List[int]) -> None:
    add_value(number, index, 1, 0)


def explode(number: List[Any]) -> bool:
    index = [0]
    while len(index):
        if isinstance(get(number, index), list):
            if len(index) == 4:
                # If still contains nesting levels we cannot explode...
                if not isinstance(get(number, index)[0], int):
                    index.append(0)
                    continue
                if not isinstance(get(number, index)[1], int):
                    index.append(1)
                    continue

                # Explode!
                add_left(number, index)
                add_right(number, index)
                i = index.pop()
                get(number, index)[i] = 0
                return True
            index.append(0)
        else:
            if index[-1] == 0:
                index[-1] = 1
            else:
                while index.pop() == 1:
                    if not len(index):
                        return False
                    continue
                index.append(1)
    return False


def split(number: List[Any]) -> bool:
    index = [0]
    while len(index):
        if isinstance(get(number, index), list):
            index.append(0)
        else:
            value = get(number, index)
            if not isinstance(value, int):
                raise Exception("Never happening but mypy is happy!")
            if value > 9:
                i = index.pop()
                get(number, index)[i] = [value // 2, (value + 1) // 2]
                return True

            if index[-1] == 0:
                index[-1] = 1
            else:
                while index.pop() == 1:
                    if not len(index):
                        return False
                    continue
                index.append(1)
    return False


def magnitude(number: List[Any], index: List[int] = []) -> int:
    if isinstance(get(number, index), int):
        return get(number, index)

    return (3 * magnitude(number, index + [0])) + (
        2 * magnitude(number, index + [1]))


def reduce(number) -> None:
    while True:
        if explode(number):
            continue
        if split(number):
            continue
        return


def snailfish(input: str) -> None:
    number: None | List[Any] = None
    with open(input) as f:
        for line in f:
            if not len(line.split()):
                break
            number = add_numbers(number, parse(line))
            reduce(number)

    if number is None:
        raise Exception("Empty input?")

    print(f"The magnitude of the final sum is {magnitude(number)}")


if __name__ == "__main__":
    snailfish("input")
