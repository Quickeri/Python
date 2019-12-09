from model import Model, Maze
import unittest

class TestModelMethods(unittest.TestCase):
    def setUp(self):
        self.model = Model()

    def test_save_read_maze(self):
        generated_maze = self.model.depth_first_generation(5, 6)
        #maze = Maze(5, 6, generated_maze)
        self.model.save_maze("testmaze.csv", generated_maze)
        read_maze = self.model.read_maze("testmaze.csv")
        self.assertEqual(generated_maze, read_maze.grid)
        #self.assertEqual(29,read_maze.height)
        #self.assertEqual(39, read_maze.width)

    def test_save_read_multiple_mazes(self):
        #mazes = self.model.generate_multiple_mazes()
        maze1 = self.model.generate_single_maze("DFS", "5")
        maze2 = self.model.generate_single_maze("DFS", "6")
        maze3 = self.model.generate_single_maze("DFS", "7")
        mazes = [maze1, maze2, maze3]
        self.model.save_multiple_mazes("multiplemazes.csv", mazes)
        read_mazes = self.model.read_multiple_mazes("multiplemazes.csv")
        self.assertEqual(maze1, read_mazes[0].grid)
        self.assertEqual(9,read_mazes[0].height)
        self.assertEqual(9, read_mazes[0].width)

    def test_validate_input_range(self):
        input_valid = self.model.validate_input_range("asd", 5, 50)
        self.assertEqual(input_valid, False)

    def test_validate_input_range2(self):
        input_valid = self.model.validate_input_range("20", 5, 50)
        self.assertEqual(input_valid, True)

    def test_producer_consumer_queue(self):
        pass

    def test_solve_multiple_mazes(self):
        pass

    def test_generate_multiple_mazes(self):
        result = self.model.generate_and_solve_multiple("10", False)
        self.assertEqual(6, len(result))
    
if __name__ == '__main__':
    unittest.main()