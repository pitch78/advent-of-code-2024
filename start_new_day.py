import os
import pathlib
import re
import shutil

import numpy as np


def create_new_puzzle():
    new_puzzle_day_number: int = __get_new_puzzle_day_number()
    __create_new_puzzle_folder(new_puzzle_day_number)


def __get_new_puzzle_day_number() -> int:
    puzzle_folder_name_regex: str = r"day_\d{2}$"

    current_path = pathlib.Path(__file__).parent.resolve()
    available_days_num = [int(f.name[4:]) for f in os.scandir(current_path) if f.is_dir() and re.fullmatch(puzzle_folder_name_regex, f.name)]
    result: int = 1 if not available_days_num else np.max(available_days_num) + 1
    return result


def __create_new_puzzle_folder(new_puzzle_day_number) -> None:
    if new_puzzle_day_number > 24:
        print("See you next year 🥳")
        exit()
    print(f"{shutil.copytree('day_skeleton', f"day_{new_puzzle_day_number:02}")} created & ready.")


if __name__ == "__main__":
    create_new_puzzle()
