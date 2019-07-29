import heapq
import re
from typing import List

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
    puzzle = exampleMediumPuzzle
    rowSets = None
    colSets = None
    groupSets = None

    # Ask for input and parse into 2d array
    def get_input_and_parse(self):
        self.puzzle = []
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
            self.puzzle.append(row)
        print('Solving the puzzle that looks like')
        self.pretty_print()


    # Map groups to 1D array
    # Groups will be a 3x3 array where [1][2] will map to [3*1-3*2][3*2-3*3]
    def get_group_index(self, i: int, j: int):
        groupRow = int(i / 3)
        groupCol = int(j / 3)
        # Turn 2D array of groups into 1D array
        return groupRow * 3 + groupCol

    # Check if solved by looping through entire 2D puzzle
    # Side effect of updating self.rowSets, self.colSets, and self.groupSets is depended upon
    def is_solved(self):
        puzzle = self.puzzle
        solved = True
        self.rowSets = [set() for i in range(SIZE)]
        self.colSets = [set() for i in range(SIZE)]
        self.groupSets = [set() for i in range(SIZE)]

        # Iterate through puzzle
        for i in range(SIZE):
            for j in range(SIZE):
                # If there are unfilled spaces, puzzle is unsolved
                if puzzle[i][j] == 'X':
                    solved = False
                    continue
                # If there are duplicates in any set, puzzle will never be solved
                if(puzzle[i][j] in self.rowSets[i] or puzzle[i][j] in self.colSets[j]
                        or puzzle[i][j] in self.groupSets[self.get_group_index(i, j)]):
                    # self.pretty_print()
                    # print(i, j)
                    # print(puzzle[i][j])
                    # print(self.rowSets[i])
                    # print(self.colSets[j])
                    # print(self.groupSets[self.get_group_index(i, j)])
                    raise Exception('Puzzle is invalid and unsolvable!')
                self.rowSets[i].add(puzzle[i][j])
                self.colSets[j].add(puzzle[i][j])
                self.groupSets[self.get_group_index(i, j)].add(puzzle[i][j])
        return solved

    # Get all the possible values that can go in a particular space
    def get_possible_values(self, i: int, j: int) -> List[str]:
        possible_values = []
        # If this space isn't blank, then we return the space value itself
        if self.puzzle[i][j] != 'X':
            return [self.puzzle[i][j]]
        solutionSet = {str(i) for i in range(1, SIZE+1)}
        return list(solutionSet
                    .difference(self.rowSets[i])
                    .difference(self.colSets[j])
                    .difference(self.groupSets[self.get_group_index(i, j)]))

    # Fill in any spots that must have one solution
    # Return True if puzzle is solved
    def fill_trivial_spaces(self):
        was_changed = False
        for i in range(SIZE):
            for j in range(SIZE):
                if self.puzzle[i][j] == 'X':
                    possible_values = self.get_possible_values(i, j)
                    if len(possible_values) == 1:
                        self.puzzle[i][j] = possible_values[0]
                        was_changed = True
        is_solved = self.is_solved()
        if was_changed and not is_solved:
            return self.fill_trivial_spaces()
        elif is_solved:
            return True
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
        self.pretty_print()
        for i in range(SIZE):
            for j in range(SIZE):
                if self.puzzle[i][j] == 'X':
                    possible_values = self.get_possible_values(i, j)
                    heapq.heappush(possible_values_min_heap, (len(possible_values), (i, j)))
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
        for row in self.puzzle:
            print(''.join(row))
        print()


if __name__ == '__main__':
    sodoku = Sodoku()
    sodoku.pretty_print()
    sodoku.solve()
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
