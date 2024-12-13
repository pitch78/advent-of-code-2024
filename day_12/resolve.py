from common.Puzzle import Puzzle

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


class Plant():
    def __init__(self, x: int, y: int, region_char: str, region_id: int = -1, external_sides: int = 4) -> None:
        self.x = x
        self.y = y
        self.region_char = region_char
        self.region_id = region_id
        self.external_sides = external_sides

    def __str__(self):
        return f"{self.x:02}x{self.y :02}|{self.external_sides}, {self.region_id} => '{self.region_char}'"

    def __repr__(self):
        return self.__str__()


class Region():
    def __init__(self, plant_list: list[Plant]) -> None:
        self.plant_list: list[Plant] = plant_list
        self.sides: int = 0


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()
        self.enriched_area: list[list[Plant]] = []
        self.regions: list[list[Plant] | Region] = []
        self.current_region_index = 0
        self.width, self.height = -1, -1

    def solve_step1(self) -> tuple[int | str | None, bool]:
        self.enriched_area = self.get_data_as_array(lambda x, y, item: Plant(x, y, item))
        self.regions = []
        self.width, self.height = len(self.enriched_area[0]), len(self.enriched_area)
        for row in range(self.width):
            for col in range(self.height):
                self.inspect_region_of(self.enriched_area[row][col])
                # self.print_regions()

        result = 0
        for r_index, region in enumerate(self.regions):
            # print(f"Region #{r_index}('{region[0].region_char}'): A:{len(region)}, P:{sum([p.external_sides for p in region])}")
            result += len(region) * sum([p.external_sides for p in region])

        return result, True

    def print_regions(self):
        print("#" * 50)
        print("Regions:")
        for region in self.regions:
            print(region)
        # for line in self.enriched_area:
        #     print("".join([str(plant.region_id) for plant in line]))

    def inspect_region_of(self, plant: Plant, in_same_region: bool = False, region_char: str = ""):
        # print(f"Checking {plant}:")
        # checking a "new" point
        if not in_same_region:
            # first Plant of a new region, lets create a region, add it to the region and scan current plant's neighbors
            if plant.region_id == -1:
                self.current_region_index = len(self.regions)
                self.regions.append([])
            else:
                # otherwise, nothing specific to do
                return

        # plan from another region, nothing to do
        if in_same_region and plant.region_char != region_char:
            return

        plant.region_id = self.current_region_index
        self.regions[self.current_region_index].append(plant)
        # now let's check neighbors
        for d in directions:
            # print(f"{plant.x + d[0]},{plant.y + d[1]}")
            if not (plant.x + d[0] in range(self.width) and plant.y + d[1] in range(self.height)):
                continue
            if self.enriched_area[plant.y + d[1]][plant.x + d[0]].region_char == plant.region_char:
                # one neighbor mean one side less exposed
                plant.external_sides -= 1
                if self.enriched_area[plant.y + d[1]][plant.x + d[0]].region_id == -1:
                    self.inspect_region_of(self.enriched_area[plant.y + d[1]][plant.x + d[0]], True, region_char=plant.region_char)

    def solve_step2(self) -> tuple[int | str | None, bool]:
        # 1) get regions as step_1
        self.enriched_area = self.get_data_as_array(lambda x, y, item: Plant(x, y, item))
        self.regions = []
        self.width, self.height = len(self.enriched_area[0]), len(self.enriched_area)
        for row in range(self.width):
            for col in range(self.height):
                self.inspect_region_of(self.enriched_area[row][col])
                # self.print_regions()

        self.regions = [Region(list_plant) for list_plant in self.regions]
        for r_index, region in enumerate(self.regions):
            self.check_sides_of(region)
            # print(f"Region #{r_index}('{region.plant_list[0].region_char}'): A:{len(region.plant_list)}, P:{sum([p.external_sides for p in region.plant_list])}, S: {region.sides}")

        # need a second loop as later region can be nested in earlier one
        result = 0
        for region in self.regions:
            result += len(region.plant_list) * region.sides
        # 3) détecter les zones imbriquées et ajouter les bords à la zone qui la contient
        return result, True

    def check_sides_of(self, region: Region) -> None:
        pl = region.plant_list
        # 2) go around (meaning 1 plant outside), until looping.
        # initially one block upper, going left, meaning the first block is on our right
        initial_pos_x, initial_pos_y = pl[0].x + directions[0][0], pl[0].y + directions[0][1]
        initial_dir_index = 1
        current_pos_x, current_pos_y, current_dir_index = initial_pos_x, initial_pos_y, 1
        nb_sides = 0
        current_region_id = pl[0].region_id
        list_region_visited: list[int] = []
        # loop closed?
        while not (nb_sides > 0 and current_pos_x == initial_pos_x and current_pos_y == initial_pos_y and current_dir_index == initial_dir_index):
            # print(f"Checking {current_pos_x},{current_pos_y} => {current_dir_index}...")

            block_in_the_front_x = current_pos_x + directions[current_dir_index][0]
            block_in_the_front_y = current_pos_y + directions[current_dir_index][1]
            front_out = not (block_in_the_front_x in range(self.width) and block_in_the_front_y in range(self.height))
            front_other_region = front_out or self.enriched_area[block_in_the_front_y][block_in_the_front_x].region_id != current_region_id
            front_in_region = not front_out and self.enriched_area[block_in_the_front_y][block_in_the_front_x].region_id == current_region_id

            block_on_the_right_x = current_pos_x + directions[(current_dir_index + 1) % 4][0]
            block_on_the_right_y = current_pos_y + directions[(current_dir_index + 1) % 4][1]
            right_out = not (block_on_the_right_x in range(self.width) and block_on_the_right_y in range(self.height))
            right_other_region = right_out or self.enriched_area[block_on_the_right_y][block_on_the_right_x].region_id != current_region_id
            right_in_region = not right_out and self.enriched_area[block_on_the_right_y][block_on_the_right_x].region_id == current_region_id

            # Move forward
            if front_other_region and right_in_region:
                current_pos_x += directions[current_dir_index][0]
                current_pos_y += directions[current_dir_index][1]
                if current_pos_x in range(self.width) and current_pos_y in range(self.height):
                    list_region_visited.append(self.enriched_area[current_pos_y][current_pos_x].region_id)
                else:
                    list_region_visited.append(-1)
                continue

            # Turn right + move forward
            # no matter Front status, as we need to turn
            # if front_other_region and right_other_region:
            if right_other_region:
                current_dir_index = (current_dir_index + 1) % 4
                nb_sides += 1
                current_pos_x += directions[current_dir_index][0]
                current_pos_y += directions[current_dir_index][1]
                # We remove last appended id, as diagonal are taken into account
                if len(list_region_visited) > 0:
                    list_region_visited.pop()

                # Then add current pos
                if current_pos_x in range(self.width) and current_pos_y in range(self.height):
                    list_region_visited.append(self.enriched_area[current_pos_y][current_pos_x].region_id)
                else:
                    list_region_visited.append(-1)
                continue

            # Turn left
            if front_in_region and right_in_region:
                current_dir_index = (current_dir_index - 1) % 4
                nb_sides += 1
                continue

            print("🤔")
        # print()
        # print(f"list: {list_region_visited}")
        distinct_visited_region = list(set(list_region_visited))
        if len(distinct_visited_region) == 1 and distinct_visited_region[0] != -1:
            # print(f"{nb_sides} more sides for region #{distinct_visited_region[0]}")
            self.regions[distinct_visited_region[0]].sides += nb_sides
        region.sides = nb_sides


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
    today_s_puzzle.resolve(1206)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
