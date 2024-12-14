import re
from functools import reduce
from operator import mul

import numpy as np
from requests.packages import target

from common.Mode import Mode
from common.Puzzle import Puzzle


class Robot:
    def __init__(self, px: int, py: int, vx: int, vy: int, area_width:int, area_height:int):
        super().__init__()
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.area_width = area_width
        self.area_height = area_height

    def goto_next_position(self):
        self.px = (self.px + self.vx) % self.area_width
        self.py = (self.py + self.vy) % self.area_height


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[int | str | None, bool]:
        nb_iteration = 100
        from common.Mode import Mode
        if self.mode == Mode.TEST:
            area_width, area_height = 11, 7
        else:
            area_width, area_height = 101, 103

        robot_infos_re = r"p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)"
        robots_final_positions: list[tuple[int, int]] = []
        for robot_data in self.raw_items:
            px, py, vx, vy = [int(value) for value in re.findall(robot_infos_re, robot_data)[0]]
            for _ in range(nb_iteration):
                area_counters = np.zeros((area_height, area_width), dtype=np.int64)
                area_counters[py][px] = 1
                # print()
                # for line in area_counters:
                #     print("".join(['.' if cpt == 0 else str(cpt) for cpt in line]))
                # print()
                px = (px + vx) % area_width
                py = (py + vy) % area_height

            robots_final_positions.append((px, py))
        print(robots_final_positions)

        quadrant_counter = [0, 0, 0, 0]
        quadrant_w, quadrant_height = area_width // 2, area_height // 2
        area_counters = np.zeros((area_height, area_width), dtype=np.int64)
        for robot_pos in robots_final_positions:
            area_counters[robot_pos[1]][robot_pos[0]] += 1
            if robot_pos[0] < quadrant_w and robot_pos[1] < quadrant_height:
                quadrant_counter[0] += 1
            elif robot_pos[0] > quadrant_w and robot_pos[1] < quadrant_height:
                quadrant_counter[1] += 1
            elif robot_pos[0] < quadrant_w and robot_pos[1] > quadrant_height:
                quadrant_counter[2] += 1
            elif robot_pos[0] > quadrant_w and robot_pos[1] > quadrant_height:
                quadrant_counter[3] += 1
        # print(quadrant_counter)
        # for line in area_counters:
        #     print("".join(['.' if cpt == 0 else str(cpt) for cpt in line]))
        return reduce(mul, quadrant_counter), True

    def solve_step2(self) -> tuple[int | str | None, bool]:
        if self.mode == Mode.TEST:
            area_width, area_height = 11, 7
        else:
            area_width, area_height = 101, 103

        robot_infos_re = r"p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)"
        robots_final_positions: list[tuple[int, int]] = []
        robots: list[Robot] = []
        for robot_data in self.raw_items:
            px, py, vx, vy = [int(value) for value in re.findall(robot_infos_re, robot_data)[0]]
            robots.append(Robot(px, py, vx, vy, area_width, area_height))

        easter_egg_found = False
        nb_iteration = 0
        m = 0
        while not easter_egg_found:
            nb_iteration += 1
            area_counters = np.zeros((area_height, area_width), dtype=np.int64)
            for robot in robots:
                robot.goto_next_position()
                area_counters[robot.py][robot.px] += 1

            target_ok = False
            for line in area_counters:
                max_robots_in_a_row = 0
                nb_robots_in_a_row = 0
                for cpt in line:
                    if cpt == 0:
                        if nb_robots_in_a_row > max_robots_in_a_row:
                            max_robots_in_a_row = nb_robots_in_a_row
                        nb_robots_in_a_row = 0
                    else:
                        nb_robots_in_a_row +=1
                target_ok = max_robots_in_a_row > 20
                if m > 20:
                    for line in area_counters:
                        print("".join(['.' if cpt == 0 else "#" for cpt in line]))
                if target_ok:
                    break
            if max_robots_in_a_row > m:
                m = max_robots_in_a_row
            easter_egg_found = target_ok
            if target_ok:
                for line in area_counters:
                    print("".join(['.' if cpt == 0 else "#" for cpt in line]))
            self.progress(f"{nb_iteration} => {m}")
        return nb_iteration, True


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve()

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    # today_s_puzzle.resolve(1000)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
