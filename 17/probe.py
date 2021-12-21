from re import findall
from typing import Final, List, Tuple


class Shot:
    target: Tuple[complex, complex] = complex(), complex()

    def __init__(self, v0: complex) -> None:
        self.v0: Final = v0
        self.cache: List[complex] = []
        self.dm: Final = self.domain()

    def at(self, s: int) -> complex:
        return self.cache[s]

    def domain(self) -> int:
        if hasattr(self, "dm"):
            return self.dm

        pastTarget: Final = lambda p: ((p.real > Shot.target[
            0].real + Shot.target[1].real) or (p.imag < Shot.target[0].imag))

        v = self.v0
        s, p = 0, complex(0)
        while True:
            p += v
            v -= complex(1 if v.real > 0 else -1 if v.real < 0 else 0, 1)
            if pastTarget(p):
                return s
            self.cache.append(p)
            s += 1

    def highest(self) -> float:
        return max([self.at(s).imag for s in range(self.domain())])

    def hitsTarget(self) -> bool:
        for s in range(self.domain()):
            p = self.at(s)
            if ((p.real >= Shot.target[0].real)
                    and (p.real <= Shot.target[0].real + Shot.target[1].real)
                    and (p.imag >= Shot.target[0].imag)
                    and (p.imag <= Shot.target[0].imag + Shot.target[1].imag)):
                return True
        return False

    def __gt__(self, other):
        return self.highest() > other.highest()

    def __lt__(self, other):
        return self.highest() < other.highest()

    def __ge__(self, other):
        return self.highest() >= other.highest()

    def __le__(self, other):
        return self.highest() <= other.highest()
    
    def __repr__(self)->str:
        return (f"({self.v0.real}, {self.v0.imag})")


def probe(input: str) -> None:
    raw: Final = open(input).readline().strip()

    targetfrom = tuple([int(v) for v in findall("=([-]?[0-9]*)\.\.", raw)])
    targetto = tuple([int(v) for v in findall("\.\.([-]?[0-9]*)", raw)])

    Shot.target = (complex(*targetfrom), complex(*targetto) - complex(*targetfrom))

    shots: List[Shot] = []
    for x in range(int(targetfrom[0] + targetto[0])):
        for y in range(-abs(int(targetfrom[1])), abs(int(targetfrom[1]))):
            shot = Shot(complex(x, y))
            if shot.hitsTarget():
                shots.append(shot)

    print(f"The highest position is {max(shots).highest()}")
    print(f"There are {len(shots)} possible initial positions")


if __name__ == "__main__":
    probe("input")
