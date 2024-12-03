import re
from threading import activeCount

from common.Puzzle import Puzzle


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[str | None, bool]:
        mul_regex = r"mul\((?P<X>\d{1,3}),(?P<Y>\d{1,3})\)"
        sum = 0
        for line in self.raw_items:
            matches = re.finditer(mul_regex, line)
            for match in matches:
                x = int(match.group("X"))
                y = int(match.group("Y"))
                sum+= x * y
        return sum, True

    def solve_step2(self) -> tuple[str | None, bool]:
        mul_regex = r"mul\((?P<X>\d{1,3}),(?P<Y>\d{1,3})\)|do\(\)|don't\(\)"
        sum = 0
        active = True
        for line in self.raw_items:
            matches = re.finditer(mul_regex, line)
            for match in matches:
                if match.group(0) == "don't()":
                    active = False
                elif match.group(0) == "do()":
                    active = True
                else:
                    if active:
                        x = int(match.group("X"))
                        y = int(match.group("Y"))
                        sum+= x * y
        return sum, True


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(161)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(48)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
