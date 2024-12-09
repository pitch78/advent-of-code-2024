from enum import Enum

from common.Puzzle import Puzzle


class Direction(Enum):
    UP = (0, -1, "^")
    RIGHT = (1, 0, ">")
    BOTTOM = (0, 1, "v")
    LEFT = (-1, 0, "<")


def get_next_direction(current_direction) -> Direction:
    direction_list = list(Direction)
    return direction_list[(direction_list.index(current_direction) + 1) % len(direction_list)]


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()
        self.area: list[list[str]] = []

    def solve_step1(self) -> tuple[int | None, bool]:
        self.area = self.get_data_as_array()
        return self.get_guard_visited_positions(), True

    def solve_step2(self) -> tuple[int | None, bool]:
        self.area = self.get_data_as_array()
        return self.get_guard_block_to_loop_positions_count(), True

    def find_guard_position(self) -> tuple[tuple[int, int], Direction] | None:
        directions = "".join([d.value[2] for d in Direction])
        for y, line in enumerate(self.area):
            for x, char in enumerate(line):
                if char in directions:
                    return (x, y), list(Direction)[directions.index(char)]

    def get_guard_visited_positions(self):
        grid_width, grid_height = len(self.area[0]), len(self.area)
        guard_pos: tuple[int, int]
        current_direction: Direction
        guard_pos, current_direction = self.find_guard_position()
        distinct_position = set()

        while True:
            distinct_position.add(guard_pos)
            next_position = guard_pos[0] + current_direction.value[0], guard_pos[1] + current_direction.value[1]

            # exit?
            if not next_position[0] in range(grid_width) or not next_position[1] in range(grid_height):
                return len(distinct_position)

            # wall?
            if self.area[next_position[1]][next_position[0]] == "#":
                current_direction = get_next_direction(current_direction)
            else:
                # ok, valid movement
                guard_pos = next_position

    def get_guard_block_to_loop_positions_count(self):
        guard_pos, current_direction = self.find_guard_position()
        return self.go_to_exit_or_loop(False, None, guard_pos, current_direction)

    def go_to_exit_or_loop(self, is_block_simulation, block_position: tuple[int, int] | None, guard_initial_pos: tuple[int, int], direction: Direction) -> tuple[int, int] | int:
        grid_width, grid_height = len(self.area[0]), len(self.area)
        possible_block_position_list = []
        current_guard_pos = guard_initial_pos
        while True:

            # we tray_trace the path from here to the exit.
            if not is_block_simulation:
                # Can we loop from here?
                for d, block_offset in [(d, (d.value[0], d.value[1])) for d in Direction]:
                    # we don't block the forward direction

                    if d == direction:
                        continue
                    possible_block_position = (guard_initial_pos[0] + block_offset[0], guard_initial_pos[1] + block_offset[1])
                    loop = self.go_to_exit_or_loop(True, possible_block_position, guard_initial_pos, direction)
                    if type(loop) == tuple:
                        possible_block_position_list.append(possible_block_position)

            next_position = current_guard_pos[0] + direction.value[0], current_guard_pos[1] + direction.value[1]

            # exit?
            if not next_position[0] in range(grid_width) or not next_position[1] in range(grid_height):
                return len(possible_block_position_list)

            # a loop? give the block position
            if next_position == guard_initial_pos:
                print(f"block position: {block_position}")
                return block_position

            # wall?
            if self.area[next_position[1]][next_position[0]] == "#" or (is_block_simulation and next_position == block_position):
                direction = get_next_direction(direction)
            else:
                # ok, valid movement
                current_guard_pos = next_position


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
