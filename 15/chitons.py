from typing import Dict, Final, List, Tuple
import numpy as np


# Priority queue which prioritizes nodes with minimum distance
class Queue:
    def __init__(self) -> None:
        self.data: Dict[int, List[int]] = {}

    def pop(self) -> int:
        selected = min(self.data.keys())
        node = self.data[selected].pop()
        if len(self.data[selected]) == 0:
            self.data.pop(selected)
        return node

    def push(self, distance: int, node: int) -> None:
        if distance not in self.data.keys():
            self.data[distance] = [node]
        else:
            self.data[distance].append(node)

    def empty(self) -> bool:
        return len(self.data) == 0


def chitons(input: str) -> None:
    raw = [line.strip() for line in open(input).readlines()]
    map = [int(x) for line in raw for x in line]
    ncols: Final = len(raw[0])

    # Store edges as a dictionary of nodes which contains per each a list of nodes as a tuple (index, distance)
    edges: List[List[Tuple[int, int]]] = [[]] * len(map)
    for index in range(len(map)):
        edges[index] = []
        neighbors = []

        # We store raveled (flattened-like) indexes: check boundaries
        if index - ncols in range(len(map)):
            neighbors.append(index - ncols)
        if index % ncols != 0:
            neighbors.append(index - 1)
        if index + ncols in range(len(map)):
            neighbors.append(index + ncols)
        if (index + 1) % ncols != 0:
            neighbors.append(index + 1)

        for neighbor in neighbors:
            edges[index].append((neighbor, map[neighbor]))

    # Distance from top-left to position
    distance = [max(map) * len(map)] * len(map)
    distance[0] = 0

    queue = Queue()
    queue.push(0, 0)

    processed = [False] * len(map)

    # Dijkstra’s algorithm
    while not queue.empty():
        a = queue.pop()
        if processed[a]:
            continue
        processed[a] = True
        for b, d in edges[a]:
            if (distance[a] + d < distance[b]):
                distance[b] = distance[a] + d
                queue.push(distance[b], b)

    print(f"The lowest total risk is {distance[-1]}")


if __name__ == "__main__":
    chitons("input")
