from typing import Dict, Final, List, Tuple


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


def dijkstra(map: List[int], ncols: int) -> int:
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

    return distance[-1]


def chitons(input: str) -> None:
    raw = [line.strip() for line in open(input).readlines()]

    # Part 1
    map = [int(x) for line in raw for x in line]
    ncols: Final = len(raw[0])
    print(f"The lowest total risk is {dijkstra(map, ncols)}")

    # Part 2: in a 5x5 grid
    rep: Final = 5
    nexteight: Final = lambda x: [
        n % 10 + 1 if n > 9 else n for n in range(x, x + (2 * rep - 1))
    ]
    ravelbig: Final = lambda r, c: r * (rep * ncols) + c

    bigmap = [0] * (ncols**2) * rep**2
    for i, n in enumerate(map):
        row, col = i // (ncols), i % (ncols)
        next = nexteight(n)
        for c in range(rep):
            for r in range(rep):
                bigmap[ravelbig(row + (r * ncols),
                                col + (c * ncols))] = next[r + c]

    print(f"The lowest total risk is {dijkstra(bigmap, ncols * rep)}")


if __name__ == "__main__":
    chitons("input")
