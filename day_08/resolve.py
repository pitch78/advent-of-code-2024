from common.Puzzle import Puzzle


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[int | str | None, bool]:
        # create dict of each frequency
        antenna_positions = dict()
        area = self.get_data_as_array()
        area_width, area_height = len(area[0]), len(area)
        for x in range(area_width):
            for y in range(area_height):
                symbol = area[y][x]
                if symbol == '.':
                    continue
                if not symbol in antenna_positions:
                    antenna_positions[symbol] = []
                antenna_positions[symbol].append((x, y))

        # check antinodes, per frequency
        antinode_set = set()
        for frequency in antenna_positions:
            positions = antenna_positions[frequency]
            nb_positions = len(positions)
            for checking_index in range(nb_positions):
                current_antenna_position = positions[checking_index]
                other_positions = positions[:checking_index] + positions[checking_index + 1:]
                for other_antenna_position in other_positions:
                    antinode_x, antinode_y = 2 * other_antenna_position[0] - current_antenna_position[0], 2 * other_antenna_position[1] - current_antenna_position[1]
                    if antinode_x in range(area_width) and antinode_y in range(area_height):
                        antinode_set.add((antinode_x, antinode_y))

        return len(antinode_set), True

    def solve_step2(self) -> tuple[int | str | None, bool]:
        # create dict of each frequency
        antenna_positions = dict()
        area = self.get_data_as_array()
        area_width, area_height = len(area[0]), len(area)
        antinode_set = set()
        for x in range(area_width):
            for y in range(area_height):
                symbol = area[y][x]
                if symbol == '.':
                    continue
                if not symbol in antenna_positions:
                    antenna_positions[symbol] = []
                antenna_positions[symbol].append((x, y))
                antinode_set.add((x, y))

        # check antinodes, per frequency
        for frequency in antenna_positions:
            positions = antenna_positions[frequency]
            nb_positions = len(positions)
            for checking_index in range(nb_positions):
                current_antenna_position = positions[checking_index]
                other_positions = positions[:checking_index] + positions[checking_index + 1:]
                for other_antenna_position in other_positions:
                    index = 1
                    antinode_x = other_antenna_position[0] + index * (other_antenna_position[0] - current_antenna_position[0])
                    antinode_y = other_antenna_position[1] + index * (other_antenna_position[1] - current_antenna_position[1])
                    while antinode_x in range(area_width) and antinode_y in range(area_height):
                        antinode_set.add((antinode_x, antinode_y))
                        index += 1
                        antinode_x = other_antenna_position[0] + index * (other_antenna_position[0] - current_antenna_position[0])
                        antinode_y = other_antenna_position[1] + index * (other_antenna_position[1] - current_antenna_position[1])

        # display antenna + antinodes
        display_area = area.copy()
        for antinode in antinode_set:
            display_area[antinode[1]][antinode[0]] = "#"
        for line in display_area:
            print("".join(line))
        return len(antinode_set), True


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(14)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(34)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
