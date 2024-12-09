from babel.dates import format_interval

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
        # print(fs_map)
        # print(available_space[:10])
        # print(available_file[-10:])

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

        # compute the checksum
        checksum = 0
        # print("".join(list_fs_map))
        for block_position, file_id in enumerate(fs_map):
            if file_id == -1:
                continue
            checksum += block_position * int(file_id)
        return checksum, True

    def solve_step2(self) -> tuple[int | str | None, bool]:
        # create FS layout
        disk_map: list[int] = [int(item) for item in self.raw_items[0]]
        is_a_file: bool = True
        file_id: int = 0
        fs_map: list[int] = []
        available_space: list[tuple[int, int]] = []
        available_file: list[tuple[int, int]] = []
        current_fs_index: int = 0
        for value in disk_map:
            if is_a_file:
                for i in range(value):
                    fs_map.append(file_id)
                available_file.append((current_fs_index, value))
                file_id += 1
            else:
                for i in range(value):
                    fs_map.append(-1)
                available_space.append((current_fs_index, value))
            current_fs_index += value
            is_a_file = not is_a_file
        # print(disk_map)

        # compact layout
        done = False
        while len(available_file) > 0:
            file_to_move_infos = available_file.pop()

            #find free space index
            index = -1
            for free_space_index, free_space in enumerate(available_space):
                # no free space big enough before the file
                if free_space[0] >= file_to_move_infos[0]:
                    break
                if free_space[1] >= file_to_move_infos[1]:
                    index = free_space_index
                    break
            #no free space for that file
            if index == -1:
                continue

            free_space_infos = available_space[index]

            # checking space
            if free_space_infos[1] < file_to_move_infos[1]:
                continue
            # we can now consider that space filled. (even if some space left)
            elif free_space_infos[1] == file_to_move_infos[1]:
                available_space.pop(index)
            else:
                available_space[index] = (free_space_infos[0] + file_to_move_infos[1], free_space_infos[1] - file_to_move_infos[1])

            # and do the copy
            for index in range(file_to_move_infos[1]):
                fs_map[free_space_infos[0] + index] = fs_map[file_to_move_infos[0] + index]
                fs_map[file_to_move_infos[0] + index] = -1
            # print(f"file: {file_to_move_infos}")
            # print(f"spc: {free_space_infos}")
            # print("".join(["." if val == -1 else str(val) for val in fs_map]))
            # print(available_space)
            # print(available_file)
            # print("#"*50)

        # compute the checksum
        checksum = 0
        # print("".join(list_fs_map))
        for block_position, file_id in enumerate(fs_map):
            if file_id == -1:
                continue
            checksum += block_position * int(file_id)
        return checksum, True


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
    today_s_puzzle.resolve(2858)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
