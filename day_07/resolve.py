from common.Puzzle import Puzzle


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[str | None, bool]:
        total_calibration_result = 0
        for line in self.raw_items:
            response = self.__solve_equation(line)
            total_calibration_result += response
        return total_calibration_result, True

    def solve_step2(self) -> tuple[str | None, bool]:
        return None, False

    def __solve_equation(self, line) -> int:
        print(f"solving: {line}")
        expected_response, numbers = line.split(":")
        expected_response, number_list = int(expected_response), [int(n) for n in numbers.strip().split(" ")]
        possible_responses : list[int] = [number_list[0]]
        for number in number_list[1:]:
            possible_response_next : list[int] = []
            for response in possible_responses:
                if response + number == expected_response:
                    return expected_response
                possible_response_next.append(response + number)
                if response * number == expected_response:
                    return expected_response
                possible_response_next.append(response * number)
            possible_responses = possible_response_next.copy()
        return 0
        # try:
        #     if possible_responses.index(expected_response):
        #         return expected_response
        # except ValueError:
        #     return 0


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(3749)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(11387)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
