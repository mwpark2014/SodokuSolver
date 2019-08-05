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
        ['9', 'X', 'X', '4', 'X', 'X', 'X', '3', '5'],
        ['7', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '9'],
        ['X', '4', 'X', 'X', '5', '9', 'X', 'X', 'X'],
        ['X', 'X', 'X', '9', '2', 'X', 'X', 'X', '3'],
        ['6', '9', 'X', '8', 'X', '5', 'X', '2', '4'],
        ['3', 'X', 'X', 'X', '1', '7', 'X', 'X', 'X'],
        ['X', 'X', 'X', '7', '6', 'X', 'X', '4', 'X'],
        ['4', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '2'],
        ['5', '8', 'X', 'X', 'X', '3', 'X', 'X', '6'],
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

    exampleHardPuzzle2 = [
        ['X', 'X', '6', 'X', 'X', '7', 'X', '4', '8'],
        ['4', 'X', '8', 'X', 'X', 'X', 'X', '9', 'X'],
        ['X', '9', 'X', '4', '8', 'X', 'X', 'X', '1'],
        ['X', 'X', '5', 'X', '2', 'X', '3', 'X', 'X'],
        ['X', 'X', 'X', '3', '5', '4', 'X', 'X', 'X'],
        ['X', 'X', '3', 'X', '6', 'X', '7', 'X', 'X'],
        ['6', 'X', 'X', 'X', '7', '5', 'X', '8', 'X'],
        ['X', '8', 'X', 'X', 'X', 'X', '9', 'X', '5'],
        ['9', '5', 'X', '8', 'X', 'X', '4', 'X', 'X'],
    ]

    exampleWrongPuzzle = [[str(i) for i in range(1, SIZE + 1)] for j in range(1, SIZE + 1)]

    def setUp(self):
        self.sodokuEasy = sodoku_solver.Sodoku(self.exampleEasyPuzzle)
        self.sodokuMedium = sodoku_solver.Sodoku(self.exampleMediumPuzzle)
        self.sodokuHard = sodoku_solver.Sodoku(self.exampleHardPuzzle)
        self.sodokuHard2 = sodoku_solver.Sodoku(self.exampleHardPuzzle2)
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

    def test_update_possible_values(self):
        self.sodokuEasy.update_possible_values()
        self.sodokuMedium.update_possible_values()
        self.sodokuHard.update_possible_values()

        for sodoku in [self.sodokuEasy, self.sodokuMedium, self.sodokuHard]:
            # Test that rows, cols, groups have len(9)
            self.assertEqual(len(sodoku.possible_values['rows']), 9)
            self.assertEqual(len(sodoku.possible_values['cols']), 9)
            self.assertEqual(len(sodoku.possible_values['groups']), 9)
            # Test that puzzle, visited are 9x9
            self.assertEqual(len(sodoku.possible_values['puzzle']), 9)
            self.assertEqual(len(sodoku.possible_values['puzzle'][0]), 9)
            self.assertEqual(len(sodoku.possible_values['visited'][0]), 9)

        with self.assertRaises(ValueError):
            self.sodokuWrong.update_possible_values()

        possible_values = self.sodokuEasy.possible_values
        self.assertEqual(possible_values['rows'][0],
                         {'2': [(0, 1), (0, 8)], '3': [(0, 1), (0, 3), (0, 4), (0, 6), (0, 7), (0, 8)], '9': [(0, 1)],
                         '8': [(0, 3), (0, 4)], '5': [(0, 3), (0, 4), (0, 6), (0, 7)], '4': [(0, 4), (0, 7), (0, 8)]})
        self.assertEqual(possible_values['cols'][0],
                         {'2': [(1, 0), (5, 0), (8, 0)], '8': [(2, 0)], '4': [(4, 0), (5, 0)], '5': [(4, 0), (8, 0)],
                          '7': [(8, 0)]})
        self.assertEqual(possible_values['groups'][0],
                         {'2': [(0, 1), (1, 0), (1, 1)], '3': [(0, 1), (1, 1), (2, 2)], '9': [(0, 1)],
                          '6': [(1, 1), (2, 2)], '8': [(2, 0)]})
        self.assertEqual(possible_values['puzzle'][4][4], {'9', '3', '4'})
        self.assertEqual(possible_values['unfilled_spaces'][0], (1, (1, 0)))
        self.assertEqual(possible_values['unfilled_spaces'][20], (3, (0, 7)))

    def test_place_values(self):
        self.sodokuHard.init_set_values()
        self.sodokuHard.update_possible_values()

        # Illegal argument exception
        with self.assertRaises(ValueError):
            self.sodokuHard.place_values([(2, 1, 0)])
        with self.assertRaises(ValueError):
            self.sodokuHard.place_values([(2, 1, '.')])
        with self.assertRaises(ValueError):
            self.sodokuHard.place_values([(9, 0, '1')])
        with self.assertRaises(ValueError):
            self.sodokuHard.place_values([(0, 9, '1')])
        with self.assertRaises(ValueError):
            self.sodokuHard.place_values([(-1, 0, '1')])
        with self.assertRaises(ValueError):
            self.sodokuHard.place_values([(0, -1, '1')])
        with self.assertRaises(ValueError):
            self.sodokuHard.place_values([(0, 0, '1')])

        # Cause board to have an illegal state
        with self.assertRaises(ValueError):
            self.sodokuHard.place_values([(2, 1, '4')])

        # Before
        self.assertEqual(self.sodokuHard.possible_values['rows'][2]['5'], [(2, 1), (2, 2)])
        self.assertEqual(self.sodokuHard.possible_values['cols'][1]['5'], [(2, 1), (6, 1), (7, 1), (8, 1)])
        self.assertEqual(self.sodokuHard.possible_values['groups'][0]['5'], [(2, 1), (2, 2)])
        self.assertEqual(self.sodokuHard.possible_values['rows'][8]['5'], [(8, 1), (8, 2), (8, 5), (8, 6), (8, 8)])
        self.assertEqual(self.sodokuHard.possible_values['cols'][2]['5'], [(2, 2), (6, 2), (7, 2), (8, 2)])
        self.assertEqual(self.sodokuHard.possible_values['groups'][6]['5'], [(6, 1), (6, 2), (7, 1), (7, 2), (8, 1), (8, 2)])
        self.sodokuHard.place_values([(2, 1, '5')])
        self.assertEqual(self.sodokuHard.set_values['puzzle'][2][1], '5')
        # After
        self.assertEqual(self.sodokuHard.possible_values['rows'][2].get('5', None), None)
        self.assertEqual(self.sodokuHard.possible_values['cols'][1].get('5', None), None)
        self.assertEqual(self.sodokuHard.possible_values['groups'][0].get('5', None), None)
        self.assertEqual(self.sodokuHard.possible_values['rows'][8]['5'], [(8, 2), (8, 5), (8, 6), (8, 8)])
        self.assertEqual(self.sodokuHard.possible_values['cols'][2]['5'], [(6, 2), (7, 2), (8, 2)])
        self.assertEqual(self.sodokuHard.possible_values['groups'][6]['5'], [(6, 2), (7, 2), (8, 2)])

    def test_fill_trivial_spaces(self):
        self.sodokuEasy.update_possible_values()
        self.sodokuMedium.update_possible_values()
        self.sodokuHard.update_possible_values()

        self.assertTrue(self.sodokuEasy.fill_trivial_spaces())
        self.assertTrue(self.sodokuEasy.is_solved())
        self.assertTrue(self.sodokuMedium.fill_trivial_spaces())
        self.assertTrue(self.sodokuMedium.is_solved())
        self.assertFalse(self.sodokuHard.fill_trivial_spaces())
        self.assertFalse(self.sodokuHard.is_solved())

    def test_solved(self):
        self.sodokuEasy.solve()
        self.assertTrue(self.sodokuEasy.is_solved())
        self.sodokuMedium.solve()
        self.assertTrue(self.sodokuMedium.is_solved())
        self.sodokuHard.solve()
        self.assertTrue(self.sodokuHard.is_solved())
        self.sodokuHard2.solve()
        self.assertTrue(self.sodokuHard2.is_solved())

if __name__ == '__main__':
    unittest.main()