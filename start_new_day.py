import os
import pathlib
import re
import shutil

import numpy as np
import requests

my_aoc_cookie: str = "..."
current_aoc_year = 2024


def create_new_puzzle():
    need_to_create_new_puzzle, new_puzzle_day_number = __get_new_puzzle_infos()
    if need_to_create_new_puzzle:
        __create_new_puzzle_folder(new_puzzle_day_number)
    __check_prod_input(new_puzzle_day_number)


def __get_new_puzzle_infos() -> (bool, int):
    puzzle_folder_name_regex: str = r"day_\d{2}$"

    # Search for existing day folders
    current_path = pathlib.Path(__file__).parent.resolve()
    available_days_num = [int(f.name[4:]) for f in os.scandir(current_path) if f.is_dir() and re.fullmatch(puzzle_folder_name_regex, f.name)]
    if not available_days_num:
        return True, 1

    last_day = np.max(available_days_num)
    # If all input files are there and not empty, we can assume that the day is ok and we need to jump to the next one
    if __last_day_inputs_ok(last_day):
        return True, last_day + 1
    # Current day not yet completed
    return False, last_day


def __create_new_puzzle_folder(new_puzzle_day_number) -> None:
    if new_puzzle_day_number > 24:
        print("See you next year 🥳")
        exit()
    print(f"Creating new folder for day {new_puzzle_day_number}...", end="")
    shutil.copytree('day_skeleton', f"day_{new_puzzle_day_number:02}")
    print("created.")


def __check_prod_input(new_puzzle_day_number):
    if not __prod_input_ok(new_puzzle_day_number):
        __dl_last_day_input(new_puzzle_day_number)


def __dl_last_day_input(last_day):
    print(f"Downloading input for day {last_day}...")
    # aoc_input_url = f"https://adventofcode.com/{current_aoc_year}/day/{last_day}/input"
    aoc_input_url = f"https://adventofcode.com/{current_aoc_year}/day/4/input"
    aoc_input_response = requests.get(aoc_input_url, cookies={"session": my_aoc_cookie})
    if aoc_input_response.status_code != 200:
        print(f"Day {last_day:02} input not available")
        return
    with open(f"day_{last_day:02}/input", 'w') as input_file:
        input_file.write(aoc_input_response.text)


def __last_day_inputs_ok(last_day):
    return __test_input_ok(last_day) and __prod_input_ok(last_day)


def __test_input_ok(day_number):
    input_file_path = f"day_{day_number:02}/input_test"
    return __input_file_ok(input_file_path)


def __prod_input_ok(day_number):
    input_file_path = f"day_{day_number:02}/input"
    return __input_file_ok(input_file_path)


def __input_file_ok(input_file_path):
    return os.path.isfile(input_file_path) and os.path.getsize(input_file_path) > 0


if __name__ == "__main__":
    create_new_puzzle()
