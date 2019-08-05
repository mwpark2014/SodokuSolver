import copy
import heapq
import re
import sys
import time
from typing import List, Set, Tuple

# TODO: Create Exception class for unsolvable puzzle

# Size of sodoku puzzle. Default is 9x9
SIZE = 9

class Sodoku:
    def __init__(self, puzzle = None):
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
            # this is required to find patterns in possible values within each constraint
            'rows': None,
            'cols': None,
            'groups': None,
            # puzzle is a 2D matrix representing possible values (which is a set) for each board space
            'puzzle': None,
            # min heap of all unfilled spaces (ordered by length of the list of possible values)
            'unfilled_spaces': None,
            # visited is a 2D matrix representing all visited values so we trim the decision branches we've already
            # visited. This is a 2D matrix containing sets
            'visited': [[set() for i in range(SIZE)] for j in range(SIZE)],
        }
        self.threads = 0

    # Ask for input and parse into 2d array
    def get_input_and_parse(self):
        puzzle = []
        print('Input a sodoku puzzle! Insert X, ., or space for unfilled spaces')

        #Get rows in sodoku puzzle. SIZE rows in every sodoku puzzle
        for i in range(1, SIZE+1):
            while(True):
                rowString = input('Row {}: '.format(i))
                if rowString == 'exit':
                    sys.exit('Exited!')
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
            self.update_possible_values()
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
    def update_possible_values(self):
        puzzle = [[None for i in range(SIZE)] for j in range(SIZE)]
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
                    .difference(self.set_values['groups'][self.get_group_index(i, j)])
                    .difference(self.possible_values['visited'][i][j]))

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
    def place_values(self, coord_values:List[Tuple]):
        for coord_value in coord_values:
            i, j, value = coord_value
            if i < 0 or j < 0 or i >= SIZE or j >= SIZE:
                raise ValueError("'i' and 'j' arguments must be > 0 and < the size of the puzzle", i, j)
            if value is None or not isinstance(value, str) or re.match(r'\D', value):
                raise ValueError("'value' argument must be a string containing a digit", value)
            if self.set_values['puzzle'][i][j] != 'X':
                raise ValueError('Attempting to fill a space that is already filled', i, j, value)
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
        self.update_possible_values()

    # Fill in any spots that must have one solution
    # Return True if puzzle is solved
    # TODO: Break this method into using smaller methods for each of the two approaches
    def fill_trivial_spaces(self):
        was_changed = False
        if self.possible_values['unfilled_spaces'] is None:
            self.update_possible_values()

        # If any spot has only 1 possible value, then that space must have that possible value as the answer
        # unfilled_space is a tuple of (<length of possible_values>, <(i, j) coordinates of space>)
        unfilled_space = self.possible_values['unfilled_spaces'][0]
        # If we already have unfilled spaces with no possible values, then we're already in an unsolvable state
        if unfilled_space[0] < 1:
            raise ValueError('Puzzle is invalid and unsolvable')
        # We are only looking at the beginning of the min heap unfilled_spaces with 1 possible value
        if unfilled_space[0] == 1:
            i, j = unfilled_space[1]
            # Take the one and only element in possible_values['puzzle'] at i, j and place that in the unfilled space
            self.place_values([(i, j, self.possible_values['puzzle'][i][j].pop())])
            was_changed = True

        # If any constraint has only 1 spot a possible value can possibly be placed, then that value can only be placed
        # in that space
        # O(3 * SIZE * SIZE)
        for constraints in [self.possible_values['rows'], self.possible_values['cols'], self.possible_values['groups']]:
            coord_values = []
            for constraint in constraints:
                for value, coords in constraint.items():
                    if len(coords) == 1:
                        coord = coords[0]
                        coord_values.append((coord[0], coord[1], value))
                        was_changed = True
            self.place_values(coord_values)
            # Since we're mutating the values we're iterating over, we need to exit the loop if anything was changed
            if was_changed:
                break

        if self.is_solved():
            return True
        elif was_changed:
            return self.fill_trivial_spaces()
        return False

    # Main solve method!
    def solve(self):
        start_time = time.time()
        self.init_set_values()
        self.update_possible_values()
        if self.solve_helper():
            print('Solution found in {} seconds!'.format(time.time() - start_time))
            self.pretty_print()
        else:
            print('This sodoku puzzle is unsolvable.')

    # Try to solve by filling trivial spaces first.
    # If that doesn't work, make guesses and recurse through different decision tree paths
    # Return true if puzzle is solved
    def solve_helper(self):
        self.threads += 1
        if self.threads % 1000 == 0:
            print('{} decision paths have been explored!'.format(self.threads))
            sodoku.pretty_print()
        if self.is_solved():
            return True
        try:
            if self.fill_trivial_spaces():
                return True
        except ValueError:
            return False
        while len(self.possible_values['unfilled_spaces']) > 0:
            i, j = heapq.heappop(self.possible_values['unfilled_spaces'])[1]
            for possible_value in self.possible_values['puzzle'][i][j]:
                # Save a copy of current puzzle state before making guesses and recursing through decision paths
                set_values_copy = copy.deepcopy(self.set_values)
                possible_values_copy = copy.deepcopy(self.possible_values)
                self.place_values([(i, j, possible_value)])
                if self.solve_helper():
                    return True
                # Reset to previous state after determining that the guess did not leave to a solution
                self.set_values = set_values_copy
                self.possible_values = possible_values_copy
                self.possible_values['visited'][i][j].add(possible_value)
        return False

    # Randomly generate solvable puzzles, taking in difficulty ratio

    # Pretty print puzzle
    def pretty_print(self):
        for row in self.set_values['puzzle']:
            print(''.join(row))
        print()


if __name__ == '__main__':
    sodoku = Sodoku()
    sodoku.get_input_and_parse()
    sodoku.solve()
