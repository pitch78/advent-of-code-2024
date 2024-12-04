from enum import Enum

from platformdirs.android import Android

from common.Puzzle import Puzzle


class Side(Enum):
    TOP = (-1, 0)
    LEFT = (0, -1)
    BOTTOM = (1, 0)
    RIGHT = (0, 1)


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()
        self.x_max: int = -1
        self.y_max: int = -1
        self.data_as_array: list[list[str]] = []

    def solve_step1(self) -> tuple[str | None, bool]:
        self.data_as_array: list[list[str]] = self.get_data_as_array()
        self.x_max = len(self.data_as_array[0])
        self.y_max = len(self.data_as_array)
        nb_xmas_found = 0
        for y, line in enumerate(self.data_as_array):
            for x, char in enumerate(line):
                for delta_y in [-1, 0, 1]:
                    for delta_x in [-1, 0, 1]:
                        if self.find_x(x, y) and self.find_m(x, y, delta_x, delta_y) and self.find_a(x, y, delta_x, delta_y) and self.find_s(x, y, delta_x, delta_y):
                            nb_xmas_found += 1
        return nb_xmas_found, True

    def solve_step2(self) -> tuple[str | None, bool]:
        self.data_as_array: list[list[str]] = self.get_data_as_array()
        self.x_max = len(self.data_as_array[0])
        self.y_max = len(self.data_as_array)
        nb_x_mas_found = 0
        for y, line in enumerate(self.data_as_array):
            for x, char in enumerate(line):
                for s in Side:
                    if self.find_x_mas_center(x, y) and self.find_ms_sides(x, y, s):
                        nb_x_mas_found += 1
        return nb_x_mas_found, True

    def find_a_char(self, char: str, x: int, y: int, delta_x: int, delta_y, dist: int):
        d = self.data_as_array
        if 0 <= x + delta_x * dist < self.x_max and 0 <= y + delta_y * dist < self.y_max and d[y + delta_y * dist][x + delta_x * dist] == char:
            return True
        return False

    def find_x(self, x: int, y: int):
        return self.data_as_array[y][x] == "X"

    def find_m(self, x: int, y: int, delta_x: int, delta_y):
        return self.find_a_char("M", x, y, delta_x, delta_y, 1)

    def find_a(self, x: int, y: int, delta_x: int, delta_y):
        return self.find_a_char("A", x, y, delta_x, delta_y, 2)

    def find_s(self, x: int, y: int, delta_x: int, delta_y):
        return self.find_a_char("S", x, y, delta_x, delta_y, 3)

    def find_x_mas_center(self, x: int, y: int):
        return self.data_as_array[y][x] == "A"

    def find_ms_sides(self, x, y, side):
        y_delta, x_delta = side.value
        if y_delta != 0:
            mx1, my1 = x - 1, y + y_delta
            mx2, my2 = x + 1, y + y_delta
            sx1, sy1 = x - 1, y - y_delta
            sx2, sy2 = x + 1, y - y_delta
        else:
            mx1, my1 = x + x_delta, y - 1
            mx2, my2 = x + x_delta, y + 1
            sx1, sy1 = x - x_delta, y - 1
            sx2, sy2 = x - x_delta, y + 1

        if not 0 <= mx1 < self.x_max or not 0 <= mx2 < self.x_max or not 0 <= sx1 < self.x_max or not 0 <= sx2 < self.x_max:
            return False
        if not 0 <= my1 < self.y_max or not 0 <= my2 < self.y_max or not 0 <= sy1 < self.y_max or not 0 <= sy2 < self.y_max:
            return False
        return self.data_as_array[my1][mx1] == "M" and self.data_as_array[my2][mx2] == "M" and self.data_as_array[sy1][sx1] == "S" and self.data_as_array[sy2][sx2] == "S"


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(18)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(9)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
