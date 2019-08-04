import unittest
import sodoku_solver

# Size of sodoku puzzle. Default is 9x9
SIZE = 9
class TestSodokuSolverMethods(unittest.TestCase):

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

    exampleHardPuzzle = [
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

    exampleWrongPuzzle = [[str(i) for i in range(1, SIZE + 1)] for j in range(1, SIZE + 1)]

    def setUp(self):
        self.sodokuEasy = sodoku_solver.Sodoku(self.exampleEasyPuzzle)
        self.sodokuMedium = sodoku_solver.Sodoku(self.exampleMediumPuzzle)
        self.sodokuHard = sodoku_solver.Sodoku(self.exampleHardPuzzle)
        self.sodokuWrong = sodoku_solver.Sodoku(self.exampleWrongPuzzle)

    def test_get_group_index(self):
        self.assertEqual(self.sodokuEasy.get_group_index(0,0), 0)
        self.assertEqual(self.sodokuEasy.get_group_index(2,2), 0)
        self.assertEqual(self.sodokuEasy.get_group_index(2,3), 1)
        self.assertEqual(self.sodokuEasy.get_group_index(3,2), 3)
        self.assertEqual(self.sodokuEasy.get_group_index(8,8), 8)
        with self.assertRaises(ValueError):
            self.sodokuEasy.get_group_index(-1,0)
        with self.assertRaises(ValueError):
            self.sodokuEasy.get_group_index(0,-1)
        with self.assertRaises(ValueError):
            self.sodokuEasy.get_group_index(9,0)
        with self.assertRaises(ValueError):
            self.sodokuEasy.get_group_index(0,9)

    def test_is_solved(self):
        self.assertFalse(self.sodokuEasy.is_solved())
        self.assertFalse(self.sodokuMedium.is_solved())
        self.assertFalse(self.sodokuHard.is_solved())
        with self.assertRaises(ValueError):
            self.sodokuWrong.is_solved()

    def test_init_set_values(self):
        self.sodokuEasy.init_set_values()
        self.sodokuMedium.init_set_values()
        self.sodokuHard.init_set_values()

        # Test that rows, cols, groups have len(9)
        self.assertEqual(len(self.sodokuEasy.set_values['cols']), 9)
        self.assertEqual(len(self.sodokuMedium.set_values['groups']), 9)
        self.assertEqual(len(self.sodokuHard.set_values['rows']), 9)

        set_values = self.sodokuEasy.set_values
        self.assertEqual(set_values['rows'][0], {'1', '7', '6'})
        self.assertEqual(set_values['rows'][8], {'4', '9', '1', '8'})
        self.assertEqual(set_values['cols'][0], {'1', '3', '6', '9'})
        self.assertEqual(set_values['cols'][8], {'7', '9', '5', '8'})
        self.assertEqual(set_values['groups'][0], {'1', '7', '4', '5'})
        self.assertEqual(set_values['groups'][8], {'9', '2', '1', '8'})

        with self.assertRaises(ValueError):
            self.sodokuWrong.init_set_values()

    def test_init_possible_values(self):
        self.sodokuEasy.init_possible_values()
        self.sodokuMedium.init_possible_values()
        self.sodokuHard.init_possible_values()

        with self.assertRaises(ValueError):
            self.sodokuWrong.init_set_values()

    def test_place_value(self):
        self.sodokuHard.init_set_values()
        self.sodokuHard.init_possible_values()

        # Illegal argument exception
        with self.assertRaises(ValueError):
            self.sodokuHard.place_value(2, 1, 0)
        with self.assertRaises(ValueError):
            self.sodokuHard.place_value(2, 1, '.')
        with self.assertRaises(ValueError):
            self.sodokuHard.place_value(9, 0, '1')
        with self.assertRaises(ValueError):
            self.sodokuHard.place_value(0, 9, '1')
        with self.assertRaises(ValueError):
            self.sodokuHard.place_value(-1, 0, '1')
        with self.assertRaises(ValueError):
            self.sodokuHard.place_value(0, -1, '1')
        with self.assertRaises(ValueError):
            self.sodokuHard.place_value(0, 0, '1')

        # Cause board to have an illegal state
        with self.assertRaises(ValueError):
            self.sodokuHard.place_value(2, 1, '4')

        self.sodokuHard.place_value(2, 1, '5')
        self.assertEqual(self.sodokuHard.set_values['puzzle'][2][1], '5')

    def test_fill_trivial_spaces(self):
        self.sodokuEasy.init_possible_values()
        self.sodokuMedium.init_possible_values()
        self.sodokuHard.init_possible_values()

        self.assertTrue(self.sodokuEasy.fill_trivial_spaces())
        self.assertTrue(self.sodokuEasy.is_solved())
        self.assertFalse(self.sodokuMedium.fill_trivial_spaces())
        self.assertFalse(self.sodokuMedium.is_solved())
        self.assertFalse(self.sodokuHard.fill_trivial_spaces())
        self.assertFalse(self.sodokuHard.is_solved())

    def test_solved(self):
        return

if __name__ == '__main__':
    unittest.main()