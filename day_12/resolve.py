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


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()
        self.enriched_area: list[list[Plant]] = []
        self.regions: list[list[Plant]] = []
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
            print(f"Region #{r_index}('{region[0].region_char}'): A:{len(region)}, P:{sum([p.external_sides for p in region])}")
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
        return None, False


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
    today_s_puzzle.resolve(80)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
