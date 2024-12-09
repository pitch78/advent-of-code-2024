from common.Puzzle import Puzzle


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[int | str | None, bool]:
        # create FS layout
        disk_map: list[int] = [int(item) for item in self.raw_items[0]]
        is_a_file: bool = True
        file_id: int = 0
        fs_map: list[int] = []
        available_space: list[int] = []
        available_file: list[int] = []
        current_fs_index: int = 0
        for value in disk_map:
            if is_a_file:
                for i in range(value):
                    fs_map.append(file_id)
                    available_file.append(current_fs_index + i)
                file_id += 1
            else:
                for i in range(value):
                    fs_map.append(-1)
                    available_space.append(current_fs_index + i)
            current_fs_index += value
            is_a_file = not is_a_file
        # print(disk_map)
        print(fs_map)
        print(available_space[:10])
        print(available_file[-10:])

        # compact layout
        done = False
        while len(available_space) > 0 and not done:
            file_index = available_file.pop()
            free_space_index = available_space.pop(0)
            if free_space_index > file_index:
                done = True
                continue
            fs_map[free_space_index] = fs_map[file_index]
            fs_map[file_index] = -1
            # print("".join(list_fs_map))
            # print(available_space)
            # print(available_file)
            # print("#"*50)

        #compute the checksum
        checksum = 0
        # print("".join(list_fs_map))
        for block_position, file_id in enumerate(fs_map):
            if file_id == -1:
                continue
            checksum += block_position * int(file_id)
        return checksum, True

    def solve_step2(self) -> tuple[int | str | None, bool]:
        return None, False


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(1928)

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
