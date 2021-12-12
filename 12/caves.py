from typing import Dict, List


def paths(map: Dict[str, List[str]], path: List[str] = ["start"]) -> int:
    visited = 0
    for bifurcation in map[path[-1]]:
        thispath = path.copy()
        if bifurcation.islower():  # small cave or start/end
            if bifurcation in path:
                continue  # already visited small cave
            if bifurcation == "end":
                thispath.append(bifurcation)
                visited += 1
        thispath.append(bifurcation)
        visited += paths(map, thispath)

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

    # make map unique
    for cave, connections in map.items():
        map[cave] = list(set(connections))

    print(f"There are {paths(map)} paths")


if __name__ == "__main__":
    caves("input")
