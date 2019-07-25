from typing import List, Tuple

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

exampleWrongPuzzle = [[str(i) for i in range(SIZE)] for j in range(SIZE)]

class Sodoku:
    puzzle = examplePuzzle

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
            # TODO: Replace wildcards into a consistent format
            row = [char for char in rowString]
            self.puzzle.append(row)
        print('Solving the puzzle that looks like')
        self.pretty_print(self.puzzle)


    # Map groups to 1D array
    # Groups will be a 3x3 array where [1][2] will map to [3*1-3*2][3*2-3*3]
    def get_group_index(self, i: int, j: int):
        groupRow = int(i / 3)
        groupCol = int(j / 3)
        # Turn 2D array of groups into 1D array
        return groupRow * 3 + groupCol

    # Check if solved by looping through entire 2D puzzle
    def is_solved(self):
        puzzle = self.puzzle
        solved = True
        #TODO: Set syntax for python
        self.rowSets = [set() for i in range(SIZE)]
        self.colSets = [set() for i in range(SIZE)]
        self.groupSets = [set() for i in range(SIZE)]

        # Iterate through puzzle
        for i in range(SIZE):
            for j in range(SIZE):
                # If there are unfilled spaces, puzzle is unsolved
                if puzzle[i][j] == 'X':
                    solved = False
                    break
                # If there are duplicates in any set, puzzle will never be solved
                if(puzzle[i][j] in self.rowSets[i] or puzzle[i][j] in self.colSets[j]
                        or puzzle[i][j] in self.groupSets[self.get_group_index(i, j)]):
                    raise Exception('Puzzle is unsolvable!')
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
    def fill_trivial_spaces(self):
        was_changed = False
        for i in range(SIZE):
            for j in range(SIZE):
                if self.puzzle[i][j] == 'X':
                    possible_values = self.get_possible_values(i, j)
                    if len(possible_values) == 1:
                        self.puzzle[i][j] = possible_values[0]
                        was_changed = True
        if was_changed:
            if self.is_solved():
                return
            self.fill_trivial_spaces()

    # Recursion somewhere here

    # Randomly generate solvable puzzles, taking in difficulty ratio

    # Pretty print puzzle
    def pretty_print(self):
        for row in self.puzzle:
            print(''.join(row))


if __name__ == '__main__':
    sodoku = Sodoku()
    sodoku.pretty_print()
    # Use is_solved to populate row, col, group sets
    print(sodoku.is_solved())

    print(sodoku.get_possible_values(2, 1))
    sodoku.fill_trivial_spaces()
    #get_input_and_parse()
