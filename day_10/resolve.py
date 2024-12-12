from common.Puzzle import Puzzle
from common.Step import Step


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[int | str | None, bool]:
        return self.find_hiking_path()

    def solve_step2(self) -> tuple[int | str | None, bool]:
        return self.find_hiking_path()

    def find_hiking_path(self) -> tuple[int | str | None, bool]:
        area = self.get_data_as_array(lambda x, y, item: int(item))
        area_width, area_height = len(area[0]), len(area)
        explore_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        nb_trailheads = 0
        for row in range(area_height):
            for col in range(area_width):
                if area[row][col] == 0:
                    # print(f"Found 0 at {col}, {row}, exploring")
                    possible_paths: list[tuple[int, int, int]] = [(col, row, 0)]
                    next_possible_paths: list[tuple[int, int, int]] = []
                    list_trailheads: list[tuple[int, int]] = []
                    while len(possible_paths) > 0:
                        for possible_position in possible_paths:
                            for direction in explore_directions:
                                # x,y
                                test_pox_x, test_pos_y = possible_position[0] + direction[0], possible_position[1] + direction[1]

                                # in area?
                                if test_pox_x in range(area_width) and test_pos_y in range(area_height):
                                    # z
                                    if area[test_pos_y][test_pox_x] == possible_position[2] + 1:
                                        if area[test_pos_y][test_pox_x] == 9:
                                            # print(f"trailhead found: {test_pox_x}x{test_pos_y}")
                                            list_trailheads.append((test_pox_x, test_pos_y))
                                        else:
                                            next_possible_paths.append((test_pox_x, test_pos_y, possible_position[2] + 1))
                        # Done, let go one step higher
                        # print(next_possible_paths)
                        possible_paths = next_possible_paths.copy()
                        next_possible_paths = []
                    if self.step == Step.STEP_1:
                        nb_trailheads += len(set(list_trailheads))
                    else:
                        nb_trailheads += len(list_trailheads)

        return nb_trailheads, True


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(36)

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
