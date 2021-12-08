from typing import Dict


class School:
    REPRODUCTION_PERIOD = 7
    BORN_TIMER = 8

    def __init__(self, days: int) -> None:
        self.days = days
        self.cache: Dict[int, Dict[int, int]] = {}

    def future(self, init_timer: int) -> int:
        """
        Returns amount of fish that would end up being in self.days if a fish with init_timer was present on day 0
        """
        return self.__future(init_timer, self.days) + 1

    def __future(self, init_timer: int, days: int) -> int:
        """
        Returns amount of times a fish will reproduce
        """
        if init_timer >= days:
            return 0  # This fish will never reproduce

        if days not in self.cache.keys():
            self.cache[days] = {}

        if init_timer in self.cache[days].keys():
            return self.cache[days][init_timer]

        # Amount of times this fish will reproduce
        progeny = (days - init_timer - 1) // School.REPRODUCTION_PERIOD + 1
        for i in range(progeny):  # Per newborn fish...
            # Days left until final request when this fish is born
            days_left = (days - init_timer) - (i *
                                               School.REPRODUCTION_PERIOD) - 1
            progeny += self.__future(School.BORN_TIMER, days_left)

        self.cache[days][init_timer] = progeny
        return progeny


def lanternfish(input: str, days: int) -> None:
    school = School(days)
    future = 0
    with open(input) as f:
        for fish in f.readline().strip().split(','):
            future += school.future(int(fish))

    print(f"There will be {future} lanternfish after {days} days")


if __name__ == "__main__":
    lanternfish("input", 80)
