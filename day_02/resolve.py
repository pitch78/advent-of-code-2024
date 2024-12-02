import numpy

from common.Puzzle import Puzzle


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[int | None, bool]:
        reports_ok = 0
        for report in self.raw_items:
            levels = [int(value) for value in report.split()]
            report_direction = numpy.sign(levels[1] - levels[0])
            safe = True
            for level_index in range(len(levels) - 1):
                diff = levels[level_index + 1] - levels[level_index]
                delta = abs(diff)
                if delta < 1 or delta > 3:
                    safe = False
                    break
                current_direction = numpy.sign(diff)
                if current_direction != report_direction:
                    safe = False
                    break
            if safe:
                reports_ok += 1
        return reports_ok, True

    def solve_step2(self) -> tuple[int | None, bool]:
        reports_ok = 0
        for report in self.raw_items:
            untouched_levels = [int(value) for value in report.split()]
            done = False
            need_to_retry = False
            bad_level_index = 0
            while not done or need_to_retry:
                levels = untouched_levels.copy()
                if need_to_retry:
                    levels.pop(bad_level_index)
                    bad_level_index += 1
                report_direction = numpy.sign(levels[1] - levels[0])
                safe = True
                for level_index in range(len(levels) - 1):
                    diff = levels[level_index + 1] - levels[level_index]
                    delta = abs(diff)
                    current_direction = numpy.sign(diff)
                    if delta < 1 or delta > 3 or current_direction != report_direction:
                        if bad_level_index < len(untouched_levels):
                            need_to_retry = True
                        else:
                            need_to_retry = False
                        safe = False
                        break
                if safe:
                    done = True
                    need_to_retry = False
                    reports_ok += 1
                else:
                    done = not need_to_retry
            # if not safe:
            #     print(f"{untouched_levels}: Unsafe")
        return reports_ok, True


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(2)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(4)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
