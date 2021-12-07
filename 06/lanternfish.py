from typing import Dict


class School:
    def __init__(self, days: int) -> None:
        self.days = days
        self.fut: Dict[int, int] = {}

    def future(self, timer_init: int) -> int:
        if timer_init in self.fut.keys():
            return self.fut[timer_init]

        lanternfish = [timer_init]
        for i in range(self.days):
            for i, fish in enumerate(lanternfish.copy()):
                if fish == 0:
                    lanternfish[i] = 6
                    lanternfish.append(8)
                else:
                    lanternfish[i] -= 1

        self.fut[timer_init] = len(lanternfish)
        return self.future(timer_init)


def lanternfish(input: str, days: int) -> None:
    school = School(days)
    future = 0
    with open(input) as f:
        for fish in f.readline().strip().split(','):
            future += school.future(int(fish))

    print(f"There will be {future} lanternfish")


if __name__ == "__main__":
    lanternfish("input", 80)
