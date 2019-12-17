from model import Model
from maze import Maze
from tkinter import Tk
import exceptions as exc
from view import View

class Controller:
    def __init__(self):
        self.root = Tk()
        self.model = Model()
        self.view = View(self.root, self)
    
    def run(self):
        self.root.title("Python Maze Solver")
        self.root.minsize(height = 600, width = 1000)
        self.root.mainloop()

    # Generates a single maze with a given size and generation algorithm(String) - displays a messagebox in view
    def generate_single_maze(self, generation_alg, size, repetitions):
        try:
            self.model.generate_single_maze(generation_alg, size)
            self.view.show_messagebox("Success", "New {}x{} maze created".format(size, size))
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)
    
    # Solves a single maze from a given csv file - displays a messagebox in view
    def solve_single_maze(self, solution_alg, filename, repetitions):
        try:
            maze = self.model.solve_single_maze(solution_alg, filename, repetitions)
            self.view.show_messagebox("Success", "Solved the {}x{} maze with {} repetition(s): \n{}ms minimum \n{}ms maximum \n{}ms average".format(maze.height, maze.width, repetitions, min(maze.solution_times), max(maze.solution_times), self.model.calc_average(maze.solution_times)))
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)

    def generate_multiple_mazes(self, generation_alg):
        try:
            pass
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)
    
    def solve_multiple_mazes(self, solution_algorithm, filename, repetitions):
        try:
            maze_data = self.model.solve_multiple_mazes(solution_algorithm, filename, repetitions)
            #Plot data in view
            pass
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)

    def generate_and_solve_multiple(self, repetitions, save):
        try:
            mazes = self.model.generate_and_solve_multiple(repetitions, save)
            maze_sizes = []
            avg_solution_times = []
            avg_generation_times = []
            for maze in mazes:
                maze_sizes.append(maze.height)
                avg_solution_times.append(self.model.calc_average(maze.solution_times))
                avg_generation_times.append(self.model.calc_average(maze.generation_times))

            title = "Relationship between the maze size and average solution time"
            self.view.setup_plot(1, title, "", "Maze Size", "Time (ms)")
            self.view.plot_graph(maze_sizes, avg_solution_times)
            
            title2 = "Relationship between the maze size and average generation time"
            self.view.setup_plot(2, title2, "", "Maze Size", "Time (ms)")
            self.view.plot_graph(maze_sizes, avg_generation_times)
            self.view.show_graph()
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)
    
    def solve_with_all_algorithms(self):
        pass

    def get_sol_algorithms(self):
        return self.model.get_sol_algorithms()

    def get_gen_algorithms(self):
        return self.model.get_gen_algorithms()

    def load_maze_data_from_file(self, filename):
        try:
            mazes = self.model.load_maze_data(filename)
            maze_sizes = []
            avg_solution_times = []
            avg_generation_times = []
            for maze in mazes:
                maze_sizes.append(maze.height)
                avg_solution_times.append(self.model.calc_average(maze.solution_times))
                avg_generation_times.append(self.model.calc_average(maze.generation_times))
            title = "Relationship between the maze size and average solution time"
            self.view.setup_plot(1, title, "", "Maze Size", "Time (ms)")
            self.view.plot_graph(maze_sizes, avg_solution_times)
            
            title2 = "Relationship between the maze size and average generation time"
            self.view.setup_plot(2, title2, "", "Maze Size", "Time (ms)")
            self.view.plot_graph(maze_sizes, avg_generation_times)
            self.view.show_graph()
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)