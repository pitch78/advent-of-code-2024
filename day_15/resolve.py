import os
from time import sleep

from common.ColorUtils import ColorUtils
from common.Mode import Mode
from common.Puzzle import Puzzle

movements = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__(split_by="\n\n")
        self.room_plan: list[list[str]] = []
        self.robot_instructions: list[str] = []
        self.robot_position = (0, 0)

    def solve_step1(self) -> tuple[int | str | None, bool]:
        # room plan
        self.room_plan = [list(line) for line in self.raw_items[0].split("\n")]
        self.find_robot_initial_position()

        # robot instructions
        self.robot_instructions = []
        for line in self.raw_items[1].split("\n"):
            self.robot_instructions.extend(list(line))

        for index_mvt, mvt in enumerate(self.robot_instructions):
            self.move(mvt)
        return self.get_blocks_gps(), True

    def display_plan(self, mvt, index):
        os.system('clear')
        print(f"mvt: {ColorUtils.cyan}{mvt} ({index})")
        for line in self.room_plan:
            print("".join(line)
                  .replace("@", ColorUtils.bright + ColorUtils.blue + mvt + ColorUtils.reset)
                  .replace("O", ColorUtils.yellow + "O")
                  .replace("[]", ColorUtils.yellow + "[]")
                  .replace("#", ColorUtils.red + "#")
                  .replace(".", ColorUtils.reset + ".")
                  )
        print()
        print(f"{ColorUtils.reset}_" * 50)
        print()

    def save_step(self, c, index, file):
        lines = f"{c} {index}\n"
        for line in self.room_plan:
            lines += "".join(line) + "\n"
        lines += "\n\n"
        file.writelines(lines)

    def find_robot_initial_position(self) -> None:
        for y, line in enumerate(self.room_plan):
            for x, char in enumerate(line):
                if char == "@":
                    self.robot_position = x, y
                    return
        print("no initial position found")
        exit(1)

    def move(self, mvt: str) -> None:
        direction = movements[mvt]
        pos_ahead = self.robot_position[0] + direction[0], self.robot_position[1] + direction[1]
        item_at_pos_ahead = self.room_plan[pos_ahead[1]][pos_ahead[0]]

        # wall? nothing to do
        if item_at_pos_ahead == "#":
            return

        # free space? => one step forward
        if item_at_pos_ahead == ".":
            self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
            self.robot_position = pos_ahead
            self.room_plan[pos_ahead[1]][pos_ahead[0]] = "@"
            return

        initial_check_pos = pos_ahead
        while item_at_pos_ahead != "#" and item_at_pos_ahead != ".":
            pos_ahead = pos_ahead[0] + direction[0], pos_ahead[1] + direction[1]
            item_at_pos_ahead = self.room_plan[pos_ahead[1]][pos_ahead[0]]

        # wall? nothing to do
        if item_at_pos_ahead == "#":
            return

        # space? we move all the block one by one (meaning the first one to the final pos effectively)
        self.room_plan[pos_ahead[1]][pos_ahead[0]] = "O"

        # then the robot
        self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
        self.robot_position = initial_check_pos
        self.room_plan[initial_check_pos[1]][initial_check_pos[0]] = "@"

    def move_step2(self, mvt: str) -> None:
        direction = movements[mvt]
        pos_ahead = self.robot_position[0] + direction[0], self.robot_position[1] + direction[1]
        item_at_pos_ahead = self.room_plan[pos_ahead[1]][pos_ahead[0]]

        # wall? nothing to do
        if item_at_pos_ahead == "#":
            return

        # free space? => one step forward
        if item_at_pos_ahead == ".":
            self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
            self.robot_position = pos_ahead
            self.room_plan[pos_ahead[1]][pos_ahead[0]] = "@"
            return

        initial_check_pos = pos_ahead
        if mvt in ["<", ">"]:
            while item_at_pos_ahead != "#" and item_at_pos_ahead != ".":
                pos_ahead = pos_ahead[0] + direction[0], pos_ahead[1] + direction[1]
                item_at_pos_ahead = self.room_plan[pos_ahead[1]][pos_ahead[0]]

            # wall? nothing to do
            if item_at_pos_ahead == "#":
                return

            # space? we move all the block one by one
            # horizontal move ?
            if mvt == ">":
                for x in range(pos_ahead[0] - 1, initial_check_pos[0] - 1, -1):
                    self.room_plan[pos_ahead[1]][x + 1] = self.room_plan[pos_ahead[1]][x]
            else:
                for x in range(pos_ahead[0], initial_check_pos[0]):
                    self.room_plan[pos_ahead[1]][x] = self.room_plan[pos_ahead[1]][x + 1]

            # then the robot
            self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
            self.robot_position = initial_check_pos
            self.room_plan[initial_check_pos[1]][initial_check_pos[0]] = "@"
        elif mvt == "^":
            if self.move_up([pos_ahead]):
                # then move the robot
                self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
                self.robot_position = initial_check_pos
                self.room_plan[pos_ahead[1]][pos_ahead[0]] = "@"
                # self.display_plan("^")
        elif mvt == "v":
            if self.move_down([pos_ahead]):
                # then move the robot
                self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
                self.robot_position = initial_check_pos
                self.room_plan[pos_ahead[1]][pos_ahead[0]] = "@"
                # self.display_plan("v")
        else:
            print("unknown move 🤨")
            exit()

    def move_up(self, positions_to_test: list[tuple[int, int]]) -> bool:
        return self.move_vertically(-1, positions_to_test)

    def move_down(self, positions_to_test: list[tuple[int, int]]) -> bool:
        return self.move_vertically(1, positions_to_test)

    def move_vertically(self, offset: int, positions_to_test: list[tuple[int, int]]) -> bool:
        fixed_positions = []
        for index, pos in enumerate(positions_to_test):
            if self.room_plan[positions_to_test[index][1]][positions_to_test[index][0]] == "[":
                fixed_positions.append(pos)
                # missing ] ?
                if index == len(positions_to_test) - 1 or self.room_plan[positions_to_test[index + 1][1]][positions_to_test[index + 1][0]] != "]":
                    fixed_positions.append((pos[0] + 1, pos[1]))
            # missing [ ?
            elif self.room_plan[positions_to_test[index][1]][positions_to_test[index][0]] == "]":
                if index == 0 or self.room_plan[positions_to_test[index - 1][1]][positions_to_test[index - 1][0]] != "[":
                    fixed_positions.append((pos[0] - 1, pos[1]))
                fixed_positions.append(pos)

        # checking next row
        chars_next_line = [self.room_plan[pos[1] + offset][pos[0]] for pos in fixed_positions]
        if "#" in chars_next_line:
            return False

        # not all clear? => need to check, then if not ok => give up
        if not all(char == "." for char in chars_next_line) and not self.move_vertically(offset, [(p[0], p[1] + offset) for p in fixed_positions]):
            return False

        # then move the block
        for pos in fixed_positions:
            self.room_plan[pos[1] + offset][pos[0]] = self.room_plan[pos[1]][pos[0]]
            self.room_plan[pos[1]][pos[0]] = "."
        return True

    def get_blocks_gps(self) -> int:
        gps = 0
        for y, line in enumerate(self.room_plan):
            for x, char in enumerate(line):
                if char in "O[":
                    gps += x + y * 100
        return gps

    def solve_step2(self) -> tuple[int | str | None, bool]:
        # room plan
        self.room_plan = [list(line
                               .replace("#", "##")
                               .replace("O", "[]")
                               .replace(".", "..")
                               .replace("@", "@.")
                               ) for line in self.raw_items[0].split("\n")]
        self.find_robot_initial_position()

        # robot instructions
        self.robot_instructions = []
        for line in self.raw_items[1].split("\n"):
            self.robot_instructions.extend(list(line))

        for index_mvt, mvt in enumerate(self.robot_instructions):
            self.move_step2(mvt)
        self.display_plan(mvt, index_mvt)
        return self.get_blocks_gps(), True


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(10092)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(9021)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
