from common.Puzzle import Puzzle
import re


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()
        self.left_list: list[int] = []
        self.right_list: list[int] = []

    def solve_step1(self) -> tuple[str | None, bool]:
        self.load_columns()
        return self.get_total_distance(), True

    def load_columns(self):
        self.left_list = []
        self.right_list = []

        for line in self.raw_items:
            [l, r] = re.split(r"\s+", line)
            self.left_list.append(int(l))
            self.right_list.append(int(r))
        self.left_list.sort()
        self.right_list.sort()

    def solve_step2(self) -> tuple[str | None, bool]:
        return None, False

    def get_total_distance(self):
        total_distance = 0
        for index in range(0, len(self.left_list)):
            delta: int = abs(self.left_list[index] - self.right_list[index])
            total_distance += delta
        return total_distance


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
