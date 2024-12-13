import re

from common.Puzzle import Puzzle
from common.Step import Step


class Equation():
    def __init__(self, a: int, b: int, result: int):
        super().__init__()


class TodaysPuzzle(Puzzle):
    step_2_offset = 10000000000000

    def __init__(self) -> None:
        super().__init__(split_by="\n\n")

    def solve_step1(self) -> tuple[int | str | None, bool]:
        return self.solve_claw_machine()

    def solve_claw_machine(self):
        ab_re = r"Button\s+(A|B)\s*:\s*X\+(\d+)\s*,\s*Y\+(\d+)"
        result_re = r"Prize\s*:\s*X\s*=\s*(\d+)\s*,\s*Y\s*=\s*(\d+)"
        button_pushed_counter = 0
        for machine in self.raw_items:
            # 1) get the params
            infos = machine.split("\n")
            type_eq, a1, a2 = re.findall(ab_re, infos[0])[0]
            a1, a2 = int(a1), int(a2)
            type_eq, b1, b2 = re.findall(ab_re, infos[1])[0]
            b1, b2 = int(b1), int(b2)
            r1, r2 = re.findall(result_re, infos[2])[0]
            offset = 0 if self.step == Step.STEP_1 else self.step_2_offset
            r1, r2 = int(r1) + offset, int(r2) + offset

            # 2) do the math
            b = (r1 * a2 - r2 * a1) / (b1 * a2 - b2 * a1)
            a = (r1 - b * b1) / a1

            if a == int(a) and b == int(b):
                # print(f"Solution: {int(a)}, {int(b)}")
                button_pushed_counter += 3 * a + b

        return button_pushed_counter, True

    def solve_step2(self) -> tuple[int | str | None, bool]:
        return self.solve_claw_machine()


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve()

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(875318608908)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
