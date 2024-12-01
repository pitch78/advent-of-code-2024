from common.Puzzle import Puzzle


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[str | None, bool]:
        return None, False

    def solve_step2(self) -> tuple[str | None, bool]:
        return None, False


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
    today_s_puzzle.resolve()

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
