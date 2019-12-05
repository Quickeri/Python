from model import Model, Maze
import unittest

class TestModelMethods(unittest.TestCase):
    def setUp(self):
        self.model = Model()

    def test_save_read_maze(self):
        generated_maze = self.model.depth_first_generation(20, 20)
        self.model.save_maze("testmaze.py", generated_maze)
        read_maze = self.model.read_maze("testmaze.py")
        self.assertEqual(generated_maze, read_maze)

    def test_save_read_multiple_mazes(self):
        #mazes = self.model.generate_multiple_mazes()
        maze1 = self.model.generate_single_maze("DFS", "5")
        maze2 = self.model.generate_single_maze("DFS", "6")
        maze3 = self.model.generate_single_maze("DFS", "7")
        mazes = [maze1, maze2, maze3]
        self.model.save_multiple_mazes("multiplemazes.csv", mazes)
        read_mazes = self.model.read_multiple_mazes("multiplemazes.csv")
        self.assertEqual(mazes, read_mazes)

    def test_validate_input_range(self):
        input_valid = self.model.validate_input_range("asd", 5, 50)
        self.assertEqual(input_valid, False)

    def test_validate_input_range2(self):
        input_valid = self.model.validate_input_range("20", 5, 50)
        self.assertEqual(input_valid, True)
    
    def test_validate_input_range3(self):
        input_valid = self.model.validate_input_range("100", 5, 50)
        self.assertEqual(input_valid, False)

if __name__ == '__main__':
    unittest.main()