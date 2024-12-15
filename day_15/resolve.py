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
            print("".join(line).replace("@", ColorUtils.BGwhite + ColorUtils.black + ColorUtils.blink +"@"+ColorUtils.reset).replace("O", ColorUtils.yellow+"O").replace("#", ColorUtils.red+"#").replace(".", ColorUtils.reset+"."))
        print()
        print(f"{ColorUtils.reset}_" * 50)
        print()

    def solve_step2(self) -> tuple[int | str | None, bool]:
        return None, False

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
        pos_forward = self.robot_position[0] + direction[0], self.robot_position[1] + direction[1]
        item_at_pos_forward = self.room_plan[pos_forward[1]][pos_forward[0]]

        # wall? nothing to do
        if item_at_pos_forward == "#":
            return

        # free space? => one step forward
        if item_at_pos_forward == ".":
            self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
            self.robot_position = pos_forward
            self.room_plan[pos_forward[1]][pos_forward[0]] = "@"
            return

        initial_check_pos = pos_forward
        while item_at_pos_forward != "#" and item_at_pos_forward != ".":
            pos_forward = pos_forward[0] + direction[0], pos_forward[1] + direction[1]
            item_at_pos_forward = self.room_plan[pos_forward[1]][pos_forward[0]]

        # wall? nothing to do
        if item_at_pos_forward == "#":
            return

        # space? we move all the block by one (meaning the first one to the final pos effectively)
        self.room_plan[pos_forward[1]][pos_forward[0]] = "O"

        # then the robot
        self.room_plan[self.robot_position[1]][self.robot_position[0]] = "."
        self.robot_position = initial_check_pos
        self.room_plan[initial_check_pos[1]][initial_check_pos[0]] = "@"

    def get_blocks_gps(self) -> int:
        gps = 0
        for y, line in enumerate(self.room_plan):
            for x, char in enumerate(line):
               if char == "O":
                    gps += x + y * 100
        return gps


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
