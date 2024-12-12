from common.Puzzle import Puzzle


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[int | str | None, bool]:
        stones = [int(stone_number) for stone_number in self.raw_items[0].split()]
        nb_loops = 25
        for i in range(nb_loops):
            new_arrangement: list[int] = []
            for stone in stones:
                if stone == 0:
                    new_arrangement.append(1)
                    continue

                stone_as_str = str(stone)
                if (len(stone_as_str) % 2) == 0:
                    new_arrangement.append(int(stone_as_str[:len(stone_as_str) // 2]))
                    new_arrangement.append(int(stone_as_str[len(stone_as_str) // 2:]))
                else:
                    new_arrangement.append(2024 * stone)
            stones = new_arrangement.copy()
            self.progress(int(100 / nb_loops * (i + 1)))
        return len(stones), True

    def solve_step2(self) -> tuple[int | str | None, bool]:
        stones = [int(stone_number) for stone_number in self.raw_items[0].split()]
        result = 0
        remaining_loop = 75
        for stone in stones:
            result += solve_stone(stone, remaining_loop)
        return result, True


cache = {}
def solve_stone(stone: int, remaining_loop: int) -> int:
    if remaining_loop == 0:
        return 1

    if (stone, remaining_loop) in cache:
        # print(f"cache ({len(cache)}) hit for {stone} at {remaining_loop}")
        return cache[(stone, remaining_loop)]

    if stone == 0:
        value = solve_stone(1, remaining_loop - 1)
        cache[(stone, remaining_loop)] = value
        return value

    stone_as_str = str(stone)
    if (len(stone_as_str) % 2) == 0:
        value = solve_stone(int(stone_as_str[:len(stone_as_str) // 2]), remaining_loop - 1) + solve_stone(int(stone_as_str[len(stone_as_str) // 2:]), remaining_loop - 1)
        cache[(stone, remaining_loop)] = value
        return value
    value = solve_stone(2024 * stone, remaining_loop - 1)
    cache[(stone, remaining_loop)] = value
    return value


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(55312)

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
