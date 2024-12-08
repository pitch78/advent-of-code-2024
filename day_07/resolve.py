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
        total_calibration_result = 0
        for line in self.raw_items:
            response = self.__solve_equation_2(line)
            total_calibration_result += response
        return total_calibration_result, True

    def __solve_equation(self, line) -> int:
        expected_response, numbers = line.split(":")
        expected_response, number_list = int(expected_response), [int(n) for n in numbers.strip().split(" ")]
        possible_responses: list[int] = [number_list[0]]
        for number in number_list[1:]:
            possible_response_next: list[int] = []
            for response in possible_responses:
                if response + number == expected_response:
                    print(f"{line} => Ok")
                    return expected_response
                possible_response_next.append(response + number)
                if response * number == expected_response:
                    print(f"{line} => Ok")
                    return expected_response
                possible_response_next.append(response * number)
            possible_responses = possible_response_next.copy()
        return 0
        # try:
        #     if possible_responses.index(expected_response):
        #         return expected_response
        # except ValueError:
        #     return 0

    def __solve_equation_2(self, line) -> int:
        expected_response, numbers = line.split(":")
        expected_response, number_list = int(expected_response), [int(n) for n in numbers.strip().split(" ")]
        possible_responses: list[int] = [0]
        last_mergeable_index = len(number_list) - 1
        for num_index, number in enumerate(number_list):
            possible_response_next: list[int] = []
            for response in possible_responses:
                if response + number == expected_response or (num_index < last_mergeable_index and (response + self.__merge(number, number_list[num_index + 1]) == expected_response)):
                    print(f"{line} => Ok")
                    return expected_response
                possible_response_next.append(response + number)
                if (1 if response == 0 else response) * number == expected_response or (num_index < last_mergeable_index and ((1 if response == 0 else response) * self.__merge(number, number_list[num_index + 1]) == expected_response)):
                    print(f"{line} => Ok")
                    return expected_response
                possible_response_next.append(response * number)
            possible_responses = possible_response_next.copy()
        return 0

    @staticmethod
    def __merge(number, next_number) -> int:
        return int(f"{number}{next_number}")


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
