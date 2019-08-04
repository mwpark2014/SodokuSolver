import heapq
import re
from typing import Set

# If every class variable will be snapshot, make every dependence real-time instead of cached
# Cut out branches that have already been explored (at least the failures)

# Size of sodoku puzzle. Default is 9x9
SIZE = 9

# TODO: Remove this
examplePuzzle = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['7', '8', '9', '1', '2', '3', '4', '5', '6'],
    ['4', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['2', '3', '4', '5', '6', '7', '8', '9', '1'],
    ['5', '6', '7', '8', '9', '1', '2', '3', '4'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
]

exampleEasyPuzzle = [
    ['1', 'X', '7', 'X', 'X', '6', 'X', 'X', 'X'],
    ['X', 'X', '4', 'X', 'X', '9', '8', 'X', '7'],
    ['X', '5', 'X', '2', 'X', 'X', 'X', 'X', '9'],
    ['3', '7', '9', 'X', 'X', '5', '4', 'X', 'X'],
    ['X', '8', 'X', '1', 'X', '7', 'X', '2', 'X'],
    ['X', 'X', '1', '6', 'X', 'X', '7', '8', '5'],
    ['6', 'X', 'X', 'X', 'X', '8', 'X', '9', 'X'],
    ['9', 'X', '8', '4', 'X', 'X', '2', 'X', 'X'],
    ['X', '4', 'X', '9', 'X', 'X', '1', 'X', '8'],
]

exampleMediumPuzzle = [
    ['X', '2', 'X', '6', 'X', '8', 'X', 'X', 'X'],
    ['5', '8', 'X', 'X', 'X', '9', '7', 'X', 'X'],
    ['X', 'X', 'X', 'X', '4', 'X', 'X', 'X', 'X'],
    ['3', '7', 'X', 'X', 'X', 'X', '5', 'X', '4'],
    ['6', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', '8', 'X', 'X', 'X', 'X', '1', '3'],
    ['X', 'X', 'X', 'X', '2', 'X', 'X', 'X', 'X'],
    ['X', 'X', '9', '8', 'X', 'X', 'X', '3', '6'],
    ['X', 'X', 'X', '3', 'X', '6', 'X', '9', 'X'],
]

exampleWrongPuzzle = [[str(i) for i in range(1, SIZE+1)] for j in range(1, SIZE+1)]


class Sodoku:
    def __init__(self, puzzle):
        # Data structures dealing with values already set
        self.set_values = {
            # rows, cols, and groups are sets representing set values for each constraint
            'rows': None,
            'cols': None,
            'groups': None,
            # puzzle is a 2D matrix representing set values
            'puzzle': puzzle,
        }
        # Data structures dealing with possible values still to be placed
        self.possible_values = {
            # rows, cols, and groups are dicts representing possible values mapped to all possible positions
            'rows': None,
            'cols': None,
            'groups': None,
            # puzzle is a 2D matrix representing possible values (which is a set)
            'puzzle': None,
            # min heap of all unfilled spaces (ordered by length of the list of possible values)
            'unfilled_spaces': None,
        }

    # Ask for input and parse into 2d array
    def get_input_and_parse(self):
        puzzle = []
        print('Input a sodoku puzzle! Insert X, ., or space for unfilled spaces')

        #Get rows in sodoku puzzle. SIZE rows in every sodoku puzzle
        for i in range(1, SIZE+1):
            while(True):
                rowString = input('Row {}: '.format(i))
                if rowString == 'exit':
                    return
                elif len(rowString) != SIZE:
                    print('A valid row must have exactly {} characters in it! "exit" to quit'.format(SIZE))
                else:
                    break
            rowString = re.sub(r'\D', 'X', rowString)
            row = [char for char in rowString]
            puzzle.append(row)
        self.set_values['puzzle'] = puzzle
        print('Solving the puzzle that looks like')
        self.pretty_print()

    # Map groups to 1D array
    # Groups will be a 3x3 array where [1][2] will map to [3*1-3*2][3*2-3*3]
    @staticmethod
    def get_group_index(i: int, j: int):
        if i < 0 or j < 0 or i >= SIZE or j >= SIZE:
            raise ValueError('Index can not be negative or greater than the size of the puzzle')
        groupRow = int(i / 3)
        groupCol = int(j / 3)
        # Turn 2D array of groups into 1D array
        return groupRow * 3 + groupCol

    # Check if solved by checking whether there are any spaces left to fill. The puzzle should never be in a state
    # where all spaces are filled but it is not valid. This will throw an exception.
    def is_solved(self):
        if self.possible_values['unfilled_spaces'] is None:
            self.init_possible_values()
        if len(self.possible_values['unfilled_spaces']) <= 0:
            return True
        return False

    # Initialize set_values rows, cols, and groups (sets representing set values for each constraint)
    def init_set_values(self):
        puzzle = self.set_values['puzzle']
        rows = [set() for i in range(SIZE)]
        cols = [set() for i in range(SIZE)]
        groups = [set() for i in range(SIZE)]
        if puzzle is None:
            self.get_input_and_parse()
        # Iterate through puzzle
        for i in range(SIZE):
            for j in range(SIZE):
                # If there are unfilled spaces, ignore
                if puzzle[i][j] == 'X':
                    continue
                # If there are duplicates in any set, puzzle will never be solved
                if (puzzle[i][j] in rows[i] or puzzle[i][j] in cols[j]
                        or puzzle[i][j] in groups[self.get_group_index(i, j)]):
                    raise ValueError('Puzzle is invalid and unsolvable!')
                rows[i].add(puzzle[i][j])
                cols[j].add(puzzle[i][j])
                groups[self.get_group_index(i, j)].add(puzzle[i][j])
        self.set_values.update({
            'rows': rows,
            'cols': cols,
            'groups': groups,
        })

    # Initialize possible_values puzzle 2D matrix and
    def init_possible_values(self):
        puzzle = [[[] for i in range(SIZE)] for j in range(SIZE)]
        rows = [{} for i in range(SIZE)]
        cols = [{} for i in range(SIZE)]
        groups = [{} for i in range(SIZE)]
        unfilled_spaces = []
        if self.set_values['rows'] is None or self.set_values['cols'] is None or self.set_values['groups'] is None:
            self.init_set_values()

        # Get all the possible values that can go in a particular space
        def get_possible_values(i: int, j: int) -> Set[str]:
            # If this space isn't blank, then we return the space value itself
            if self.set_values['puzzle'][i][j] != 'X':
                return {self.set_values['puzzle'][i][j]}
            solution_set = {str(i) for i in range(1, SIZE + 1)}
            return (solution_set
                    .difference(self.set_values['rows'][i])
                    .difference(self.set_values['cols'][j])
                    .difference(self.set_values['groups'][self.get_group_index(i, j)]))

        # Iterate through puzzle
        for i in range(SIZE):
            for j in range(SIZE):
                possible_values = get_possible_values(i, j)
                if self.set_values['puzzle'][i][j] == 'X':
                    unfilled_spaces.append((len(possible_values), (i, j)))
                    for value in possible_values:
                        rows[i].setdefault(value, []).append((i, j))
                        cols[j].setdefault(value, []).append((i, j))
                        groups[self.get_group_index(i, j)].setdefault(value, []).append((i, j))
                puzzle[i][j] = possible_values

        heapq.heapify(unfilled_spaces)
        self.possible_values.update({
            'puzzle': puzzle,
            'unfilled_spaces': unfilled_spaces,
            'rows': rows,
            'cols': cols,
            'groups': groups,
        })

    # Update sodoku state when placing a value into an unfilled space. Transition unfilled space with possible_values
    # to a set space with one definitive value
    # Raise exception if len(possible_values) for any spot is ever < 1
    def place_value(self, i, j, value):
        if i < 0 or j < 0 or i >= SIZE or j >= SIZE:
            raise ValueError("'i' and 'j' arguments must be > 0 and < the size of the puzzle")
        if value is None or not isinstance(value, str) or re.match(r'\D', value):
            raise ValueError("'value' argument must be a string containing a digit")
        if self.set_values['puzzle'][i][j] != 'X':
            raise ValueError('Attempting to fill a space that is already filled')
        self.set_values['puzzle'][i][j] = value

        # Update set_values
        rows = self.set_values['rows']
        cols = self.set_values['cols']
        groups = self.set_values['groups']
        # If there are duplicates in any set, puzzle will never be solved
        if value in rows[i] or value in cols[j] or value in groups[self.get_group_index(i, j)]:
            # Undo placement in case we decide to recover from this exception
            self.set_values['puzzle'][i][j] = 'X'
            raise ValueError('Puzzle is invalid and unsolvable!')
        rows[i].add(value)
        cols[j].add(value)
        groups[self.get_group_index(i, j)].add(value)

        # Update possible_values

        return

    # Fill in any spots that must have one solution
    # Return True if puzzle is solved
    def fill_trivial_spaces(self):
        was_changed = False
        if self.possible_values['unfilled_spaces'] is None:
            self.init_possible_values()
        unfilled_spaces = self.possible_values['unfilled_spaces']

        # unfilled_space is a tuple of (<length of possible_values>, <(i, j) coordinates of space>)
        for unfilled_space in unfilled_spaces:
            # We are only looking at the beginning of the min heap unfilled_spaces, so exit after we start seeing
            # possible_values lengths > 1
            if unfilled_space[0] > 1:
                break
            i, j = unfilled_space[1]
            # Take the one and only element in possible_values['puzzle'] at i, j and place that in the unfilled space
            self.place_value(i, j, self.possible_values['puzzle'][i][j][0])
            was_changed = True

        if self.is_solved():
            return True
        elif was_changed:
            return self.fill_trivial_spaces()
        return False

    # Main solve method!
    def solve(self):
        if self.solve_helper():
            print('Solution: ')
            self.pretty_print()
        else:
            print('This sodoku puzzle is unsolvable.')

    # Try to solve by filling trivial spaces first.
    # If that doesn't work, make guesses and recurse through different decision tree paths
    # Return true if puzzle is solved
    def solve_helper(self):
        possible_values_min_heap = []
        if self.is_solved():
            return True
        try:
            if self.fill_trivial_spaces():
                return True
        except Exception:
            return False
        if len(possible_values_min_heap) != 0:
            # Save a copy of current puzzle state before making guesses and recursing through decision paths
            while len(possible_values_min_heap) > 0:
                i, j = heapq.heappop(possible_values_min_heap)[1]
                for possible_value in self.get_possible_values(i, j):
                    puzzle_copy = [row[:] for row in self.puzzle]
                    self.puzzle[i][j] = possible_value
                    if self.solve_helper():
                        return True
                    self.puzzle = puzzle_copy
                    self.is_solved()
        return False

    # Randomly generate solvable puzzles, taking in difficulty ratio

    # Pretty print puzzle
    def pretty_print(self):
        for row in self.set_values['puzzle']:
            print(''.join(row))
        print()


if __name__ == '__main__':
    sodoku = Sodoku()
    sodoku.pretty_print()
    sodoku.init_possible_values()
    #sodoku.fill_trivial_spaces()
    #sodoku.get_input_and_parse()
    #sodoku.solve()
    # Use is_solved to populate row, col, group sets
    # print(sodoku.is_solved())
    # print(sodoku.get_possible_values(0, 0))
    # print(sodoku.get_possible_values(2, 0))
    # print(sodoku.get_possible_values(2, 1))
    # print(sodoku.get_possible_values(2, 2))
    # print(sodoku.get_possible_values(0, 2))
    # print(sodoku.get_possible_values(1, 2))
    # sodoku.fill_trivial_spaces()
    # sodoku.pretty_print()
    # print(sodoku.is_solved())
    #get_input_and_parse()
