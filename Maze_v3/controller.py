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

    #Generates a single maze with a given size and generation algorithm(String) - displays a messagebox in view
    def generate_single_maze(self, generation_alg, size, repetitions):
        try:
            self.model.generate_single_maze(generation_alg, size)
            self.view.show_messagebox("Success", "New {}x{} maze created".format(size, size))
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)
    
    #Solves a single maze from a given csv file - displays a messagebox in view
    def solve_single_maze(self, solution_alg, filename, repetitions):
        try:
            size, moves, times = self.model.solve_single_maze(solution_alg, filename)
            self.view.show_messagebox("Success", "Solved the {}x{} maze in {}ms, and {} moves".format(size, size, times, moves))
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)

    def generate_multiple_mazes(self, generation_alg):
        pass
    
    def solve_multiple_mazes(self, solution_algorithm, filename, repetitions):
        try:
            maze_data = self.model.solve_multiple_mazes(solution_algorithm, filename, repetitions)
            #Plot data in view
            pass
        except exc.InvalidInputException as e:
            self.view.show_messagebox("Error", e)

    def generate_with_all_algorithms(self):
        pass
    
    def solve_with_all_algorithms(self):
        pass

    def get_sol_algorithms(self):
        return self.model.get_sol_algorithms()

    def get_gen_algorithms(self):
        return self.model.get_gen_algorithms()