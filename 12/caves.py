from typing import Dict, List


def paths(map: Dict[str, List[str]],
          small_visited_twice: bool | None = None,
          path: List[str] = ["start"]) -> int:
    visited = 0
    for bifurcation in map[path[-1]]:
        thispath = path.copy()
        if bifurcation.islower():  # small cave or start/end
            if bifurcation == "start":
                continue  # start does not count
            if bifurcation == "end":
                thispath.append(bifurcation)
                visited += 1  # path is done!
                continue
            if bifurcation in path and small_visited_twice is None:
                continue  # already visited small cave (part 1)
            if bifurcation in path and not small_visited_twice:
                # already visited small cave when no other cave has been visited twice (part 2)
                thispath.append(bifurcation)
                # visit this small cave twice then continue resolving paths
                visited += paths(map, True, thispath)
                # do not visit this one twice and then continue resolving paths
                continue
            if bifurcation in path and small_visited_twice:
                # already visited small cave when another cave has already been visited twice (part 2)
                continue
        # visit this cave, then continue resolving paths
        thispath.append(bifurcation)
        visited += paths(map, small_visited_twice, thispath)

    return visited


def caves(input: str) -> None:
    map: Dict[str, List[str]] = {}
    with open(input) as f:
        for line in f:
            pair = line.strip().split('-')
            for a, b in ((0, 1), (1, 0)):  # Add pairs both ways
                if pair[a] not in map:
                    map[pair[a]] = []
                map[pair[a]].append(pair[b])

    print(f"There are {paths(map)} paths when visiting small caves once")
    print(
        f"There are {paths(map, False)} paths when visiting a single small cave twice"
    )


if __name__ == "__main__":
    caves("input")
