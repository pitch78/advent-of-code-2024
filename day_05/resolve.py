from common.Puzzle import Puzzle


class TodaysPuzzle(Puzzle):
    def __init__(self) -> None:
        super().__init__()

    def solve_step1(self) -> tuple[str | None, bool]:
        # Loading rules and updates
        rules: list[list[str]] = []
        updates: list[list[str]] = []
        is_rule: bool = True
        for line in self.raw_items:
            if is_rule and line.strip() == "":
                is_rule = False
                continue

            if is_rule:
                rules.append(line.strip().split("|"))
            else:
                updates.append(line.strip().split(","))

        # Solving the puzzle
        result = 0
        for update in updates:
            update_valid = True
            for rule in rules:
                try:
                    index_a = update.index(rule[0])
                    index_b = update.index(rule[1])
                except ValueError:
                    continue
                if index_a > index_b:
                    update_valid = False
                    break
            if update_valid:
                result += int(update[len(update) // 2])
        return result, True

    def solve_step2(self) -> tuple[str | None, bool]:
        # Loading rules and updates
        rules: list[list[str]] = []
        updates: list[list[str]] = []
        is_rule: bool = True
        for line in self.raw_items:
            if is_rule and line.strip() == "":
                is_rule = False
                continue

            if is_rule:
                rules.append(line.strip().split("|"))
            else:
                updates.append(line.strip().split(","))
        # last empty line
        if len(updates[-1]) == 1:
            del updates[-1]

        # Solving the puzzle
        result = 0
        for update in updates:
            need_to_retry = True
            update_invalid_at_some_point = False
            while need_to_retry:
                need_to_retry = False
                for rule in rules:
                    try:
                        index_a = update.index(rule[0])
                        index_b = update.index(rule[1])
                    except ValueError:
                        #one or the other not there, no compare to do
                        continue

                    if index_a > index_b:
                        update[index_a], update[index_b] = update[index_b], update[index_a]
                        need_to_retry = True
                        break
                if need_to_retry:
                    update_invalid_at_some_point = True
            if update_invalid_at_some_point:
                result += int(update[len(update) // 2])
        return result, True


if __name__ == "__main__":
    # starting step_1, test_mode
    today_s_puzzle = TodaysPuzzle()
    today_s_puzzle.resolve(143)

    # then step_1, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()

    # Part 2
    print()
    # then step_2, test_mode
    today_s_puzzle.step2()
    today_s_puzzle.resolve(123)

    # then step_2, prod_mode
    today_s_puzzle.prod_mode()
    today_s_puzzle.resolve()
