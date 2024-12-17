from common.ColorUtils import ColorUtils
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

        for mvt in self.robot_instructions:
            self.move(mvt)
            # self.display_plan(mvt)
        return self.get_blocks_gps(), True

    def display_plan(self, mvt):
        print()
        print(f"mvt: {ColorUtils.cyan}{mvt}")
        for line in self.room_plan:
            print("".join(line)
                  .replace("@", ColorUtils.BGwhite + ColorUtils.black + ColorUtils.blink + "@" + ColorUtils.reset)
                  .replace("O", ColorUtils.yellow + "O")
                  .replace("[]", ColorUtils.yellow + "[]")
                  .replace("#", ColorUtils.red + "#")
                  .replace(".", ColorUtils.reset + ".")
                  )
        print()
        print(f"{ColorUtils.reset}_" * 50)
        print()

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
        elif mvt == "^":
            if self.move_down([pos_ahead]):
                # then move the robot
                self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
                self.robot_position = initial_check_pos
                self.room_plan[pos_ahead[1]][pos_ahead[0]] = "@"
        else:
            print("unknown move 🤨")
            exit()

    def move_up(self, positions_to_test: list[tuple[int, int]]) -> bool:
        # do we need to extend the range?
        if self.room_plan[positions_to_test[0][1]][positions_to_test[0][0]] == "]":
            # adding "[" pos as first item of the list
            positions_to_test.insert(0, (positions_to_test[0][0] - 1, positions_to_test[0][1]))
        if self.room_plan[positions_to_test[-1][1]][positions_to_test[-1][0]] == "[":
            # adding "]" pos as last item of the list
            positions_to_test.append((positions_to_test[-1][0] + 1, positions_to_test[-1][1]))

        # checking row above
        row_above_ok = True
        for pos in positions_to_test:
            if self.room_plan[pos[1] - 1][pos[0]] == "#":
                row_above_ok = False
                break
            if self.room_plan[pos[1] - 1][pos[0]] in ["[", "]"] and not self.move_up([(p[0], p[1] - 1) for p in positions_to_test]):
                row_above_ok = False
                break
        if not row_above_ok:
            return False

        # then move the block
        for pos in positions_to_test:
            self.room_plan[pos[1] - 1][pos[0]] = self.room_plan[pos[1]][pos[0]]
            self.display_plan("^")
            self.room_plan[pos[1]][pos[0]] = "."
            self.display_plan("^")
        return True

    def move_down(self, positions_to_test: list[tuple[int, int]]) -> bool:
        # do we need to extend the range?
        if self.room_plan[positions_to_test[0][1]][positions_to_test[0][0]] == "]":
            # adding "[" pos as first item of the list
            positions_to_test.insert(0, (positions_to_test[0][0] - 1, positions_to_test[0][1]))
        if self.room_plan[positions_to_test[-1][1]][positions_to_test[-1][0]] == "[":
            # adding "]" pos as last item of the list
            positions_to_test.append((positions_to_test[-1][0] + 1, positions_to_test[-1][1]))

        # checking row above
        row_below_ok = True
        for pos in positions_to_test:
            if self.room_plan[pos[1] + 1][pos[0]] == "#":
                row_below_ok = False
                break
            if self.room_plan[pos[1] + 1][pos[0]] in ["[", "]"] and not self.move_down([(p[0], p[1] + 1) for p in positions_to_test]):
                row_below_ok = False
                break
        if not row_below_ok:
            return False

        # then move the block
        for pos in positions_to_test:
            self.room_plan[pos[1] + 1][pos[0]] = self.room_plan[pos[1]][pos[0]]
            self.display_plan("v")
            self.room_plan[pos[1]][pos[0]] = "."
            self.display_plan("v")
        return True

    def get_blocks_gps(self) -> int:
        gps = 0
        for y, line in enumerate(self.room_plan):
            for x, char in enumerate(line):
                if char in ["O", "["]:
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

        for mvt in self.robot_instructions:
            self.move_step2(mvt)
            self.display_plan(mvt)
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
