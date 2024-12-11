import os.path
from time import time
from typing import Callable

from common.Loader import Loader
from common.Mode import Mode
from common.Step import Step


class Puzzle:
    def __init__(self, mode: Mode = Mode.TEST, step: Step = Step.STEP_1, split_by: str = "\n") -> None:
        self.mode = mode
        self.step: Step = step
        self.split_by: str = split_by
        self.raw_items: list[str] = []
        self.step_loader: Loader| None = None
        self.load_data()

    def load_data(self) -> None:
        step_2_extension = ""
        if self.step == Step.STEP_2 and os.path.exists(f"./input{'' if self.mode == Mode.PROD else '_test'}_2"):
            step_2_extension = "_2"

        with open(f"./input{'' if self.mode == Mode.PROD else '_test'}{step_2_extension}", "r") as input_file:
            self.raw_items = [item for item in input_file.read().split(self.split_by)]

            # remove trailing blank lines
            while len(self.raw_items[-1].strip()) == 0:
                del self.raw_items[-1]

    # Debug helper, not supposed to be used in regular usage
    def display_raw_data(self):
        for item in self.raw_items:
            print(item)

    def display_area(self):
        for item in self.area:
            print("".join(item))

    def get_data_as_array(self, transform: Callable[[str], str | int] = None) -> list[list[str | int]]:
        return [list(line) if transform is None else [transform(item) for item in line] for line in self.raw_items]

    # Wrapper around, current day solvers. Handle execution timing and response display
    def resolve(self, expected_result: int = None) -> None:
        self.step_loader = Loader(f"Part#{self.step.value} {self.mode.value}").start()
        start = time()
        if self.step == Step.STEP_1:
            solution, found = self.solve_step1()
        else:
            solution, found = self.solve_step2()
        end = time()
        must_exit, sum_up = self.__display_current_solution(expected_result, solution, found, end - start)
        self.step_loader.stop(sum_up, not must_exit)
        if must_exit:
            exit()

    def progress(self, value: int) -> None:
        if self.step_loader is not None:
            self.step_loader.progress(value)

    # No response, no solution found
    def solve_step1(self) -> tuple[str | None, bool]:
        return None, False

    # No response, no solution found
    def solve_step2(self) -> tuple[str | None, bool]:
        return None, False

    def step1(self):
        self.__set_step(Step.STEP_1)

    def step2(self):
        self.__set_step(Step.STEP_2)

    def prod_mode(self):
        self.__set_mode(Mode.PROD)

    def test_mode(self):
        self.__set_mode(Mode.TEST)

    def dummy(self):
        pass

    def __set_mode(self, mode: Mode):
        self.mode = mode
        self.load_data()

    def __set_step(self, step: Step, force_test_mode: bool = True):
        self.step = step
        if force_test_mode:
            self.test_mode()

    def __display_current_solution(self, expected_result: int | None, solution: int, found: bool, duration: float):
        if found and (expected_result is None or expected_result == solution):
            duration_str: str = "" if self.mode == Mode.TEST else f" (in {duration:.2f}s)"
            return False, f" {duration_str}: {solution}"
        elif expected_result is not None and expected_result != solution:
            return True, f" 😩: Got: {solution}, but {expected_result} expected"
        return True, f":\nYou can do it 💪🏻"
