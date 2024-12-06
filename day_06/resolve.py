from enum import Enum

from common.Puzzle import Puzzle


class Direction(Enum):
    UP = (0, -1, "^")
    RIGHT = (1, 0, ">")
    BOTTOM = (0, 1, "v")
    LEFT = (-1, 0, "<")


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()
        self.area: list[list[str]] = []
        self.guard_pos: tuple[int, int] = (0, 0)
        self.current_direction: Direction = Direction.UP
        self.guards_visited_position: int = 0

    def solve_step1(self) -> tuple[int | None, bool]:
        self.area = self.get_data_as_array()
        return self.get_guard_positions(), True

    def solve_step2(self) -> tuple[int | None, bool]:
        self.area = self.get_data_as_array()
        return None, False

    def find_guard_position(self) -> None:
        directions = "".join([d.value[2] for d in Direction])
        for y, line in enumerate(self.area):
            for x, char in enumerate(line):
                if char in directions:
                    self.guard_pos = (x, y)
                    self.current_direction = list(Direction)[directions.index(char)]
                    return

    def get_next_position(self):
        return tuple(map(lambda i, j: i + j, self.guard_pos, self.current_direction.value))

    def get_next_direction(self):
        direction_list = list(Direction)
        self.current_direction = direction_list[(direction_list.index(self.current_direction) + 1) % len(direction_list)]

    def get_guard_positions(self):
        w, h = len(self.area[0]), len(self.area)
        self.find_guard_position()
        distinct_position = set()

        while True:
            distinct_position.add(self.guard_pos)
            self.area[self.guard_pos[1]][self.guard_pos[0]] = self.current_direction.value[2]
            next_position = self.get_next_position()

            # exit?
            if not next_position[0] in range(w) or not next_position[1] in range(h):
                return len(distinct_position)

            # wall?
            if self.area[next_position[1]][next_position[0]] == "#":
                self.get_next_direction()
            else:
                # ok, valid movement
                self.guard_pos = next_position


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(41)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(6)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
