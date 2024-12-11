from common.Puzzle import Puzzle
from common.Step import Step


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[int | str | None, bool]:
        return self.solve_both_steps()

    def solve_step2(self) -> tuple[int | str | None, bool]:
        return self.solve_both_steps()

    def solve_both_steps(self) -> tuple[int | str | None, bool]:
        stones = [int(stone_number) for stone_number in self.raw_items[0].split()]
        nb_loops = 25 if self.step == Step.STEP_1 else 75
        for i in range(nb_loops):
            new_arrangement: list[int] = []
            for stone in stones:
                if stone == 0:
                    new_arrangement.append(1)
                    continue

                stone_as_str = str(stone)
                if (len(stone_as_str) % 2) == 0:
                    new_arrangement.append(int(stone_as_str[:len(stone_as_str) // 2]))
                    new_arrangement.append(int(stone_as_str[len(stone_as_str) // 2:]))
                else:
                    new_arrangement.append(2024 * stone)
            stones = new_arrangement.copy()
            self.progress(int(100 / nb_loops * (i + 1)))

        return len(stones), True


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(55312)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve()

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
