from random import randint, shuffle, choice
from queue import Queue
from maze import Maze
import time
import exceptions as exc
from threading import Thread
import csv
import os.path
import sys

sys.setrecursionlimit(10000)

class Model:
    def __init__(self):
        self.queue = Queue(10)
        self.MIN_SIZE = 5
        self.MAX_SIZE = 50
        self.MIN_REPETITIONS = 1
        self.MAX_REPETITIONS = 100

    # Checks if the input string is a number within the given range - returns a boolean
    def validate_input_range(self, user_input, min_value, max_value):
        input_valid = False
        if(user_input.isdigit()):
            user_input = int(user_input)
            if(user_input >= min_value and user_input <= max_value):
                input_valid = True
        return input_valid

    # Checks if the file exists, and the format is correct
    def validate_csv_file(self, path_to_file):
        input_valid = False
        if(os.path.exists(path_to_file)):
            drive, path = os.path.splitdrive(path_to_file)
            filename, filetype = os.path.splitext(path)
            if(filetype == ".csv"):
                input_valid = True
        return input_valid

    # Generates a single maze from a given generation algorithm(String) and a file path
    def generate_single_maze(self, generation_algorithm, size):
        if(self.validate_input_range(size, self.MIN_SIZE, self.MAX_SIZE)):
            size = int(size)
            gen_alg = self.select_gen_algorithm(generation_algorithm)
            Thread(target=self.gen_maze, args=(gen_alg, self.queue, size)).start()
            maze = self.queue.get()
            self.save_maze("maze.csv", maze)
            return maze
        else:
            raise exc.InvalidInputException("Invalid input - maze size must be a number between {} and {}".format(self.MIN_SIZE, self.MAX_SIZE))
    
    def generate_multiple_mazes(self, genneration_algorithm):
        pass

    # Solves a single maze from a given solution algorithm(String) and file path
    def solve_single_maze(self, solution_algorithm, path_to_file, repetitions):
        if(self.validate_csv_file(path_to_file) and self.validate_input_range(repetitions, self.MIN_REPETITIONS, self.MAX_REPETITIONS)):
            maze = self.read_maze(path_to_file)
            sol_alg = self.select_sol_algorithm(solution_algorithm)
            Thread(target=self.sol_maze, args=(sol_alg, self.queue, maze, repetitions)).start()
            #moves = self.queue.get()
            return maze
        else:
            raise exc.InvalidInputException("Unable to read the file - wrong extention type or maze format")
    
    def solve_multiple_mazes(self, solution_algorithm, path_to_file, repetitions):
        if(self.validate_csv_file(path_to_file)):
            mazes = self.read_multiple_mazes(path_to_file)
            sol_alg = self.select_sol_algorithm(solution_algorithm)
            Thread(target=self.sol_maze, args=(sol_alg, self.queue, mazes, repetitions)).start()
            solved_mazes = self.queue.get() 
            return solved_mazes
        else:
            raise exc.InvalidInputException("Unable to read the file - wrong extention type or maze format")

    # Generates a single maze using the given algorithm and puts it into the given queue
    def gen_maze(self, gen_alg, queue, size):
        start = time.perf_counter()
        generated_maze = gen_alg(size, size) 
        end = time.perf_counter()
        elapsed = (end - start) * 1000.0 # Elasped time in ms
        queue.put(generated_maze)

    # Generates a single maze using the given algorithm and puts it into the given queue
    def sol_maze(self, sol_alg, queue, maze, repetitions):
        for i in range(int(repetitions)):
            start = time.perf_counter()
            sol_alg(maze.grid) 
            end = time.perf_counter()
            elapsed = (end - start) * 1000.0
            maze.solution_times.append(elapsed)
        #queue.put(maze)
    
    def sol_multiple_mazes(self, sol_alg, queue, mazes, repetitions):
        for maze in mazes:
            for i in range(repetitions):
                start = time.perf_counter()
                sol_alg(maze.maze) 
                end = time.perf_counter()
                elapsed = (end - start) * 1000.0
                maze.solution_times() 
            queue.put(maze)

    # Returns a reference to a generation algorithm if the key exists in the dictionary
    def select_gen_algorithm(self, name):
        generation_algorithms = {"DFS": self.depth_first_generation}
        if(name in generation_algorithms):
            return generation_algorithms[name]
        else:
            raise exc.InvalidInputException("Generation algorithm not found")

    # Returns a reference to a solution algorithm if the key exists in the dictionary
    def select_sol_algorithm(self, name):
        solution_algorithms = {"Recursive": self.search} # Make option for all algorithms?
        if(name in solution_algorithms):
            return solution_algorithms[name]
        else:
            raise exc.InvalidInputException("Solution algorithm not found")

    # List of the available generation algorithms
    def get_gen_algorithms(self):
        generation_algorithms = ["DFS", "A*", "Recurisve", "All"] 
        return generation_algorithms

    # List of the available solution algorithms
    def get_sol_algorithms(self):
        solutions_algorithms = ["Recursive", "BFS", "DFS", "All"] 
        return solutions_algorithms

    def calc_average(self, values):
        return sum(values) / len(values)

    def save_maze(self, filename, maze):
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(maze)

    def read_maze(self, filename): 
        with open(filename, 'r') as f:
            maze = [list(map(int, el)) for el in csv.reader(f, delimiter=',')]
            m = Maze(len(maze), len(maze[0]), maze)
        return m

    def save_multiple_mazes(self, filename, mazes):
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            for maze in mazes:
                writer.writerows(maze)
                writer.writerow("")

    def read_multiple_mazes(self, filename):
        mazes = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=",")
            temp_grid = []
            for row in reader: 
                if(row):
                    temp_grid.append(row)
                else:
                    temp_grid = [list(map(int, el)) for el in temp_grid]
                    grid = [row[:] for row in temp_grid]
                    m = Maze(len(grid), len(grid[0]), grid)
                    mazes.append(m)
                    temp_grid.clear()
        return mazes

    # Generates and returns a maze with the given height and width, using the depth first algorithm
    def depth_first_generation(self, height, width):
        converted_maze = self.convert(self.DFS(self.make_empty_maze(height, width)))
        return converted_maze

    # Returns an empty maze of a given size
    def make_empty_maze(self, height, width):
        maze = [[[] for b in range(width)] for a in range(height)]
        return maze

    def convert(self, maze):
        pretty_maze = [[1]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
        for y,row in enumerate(maze):
            for x,col in enumerate(row):
                pretty_maze[2*y+1][2*x+1] = 0
                for direction in col:
                    pretty_maze[2*y+1+direction[0]][2*x+1+direction[1]] = 0
        # Removing the walls around the maze
        pretty_maze.pop(0)
        pretty_maze.pop(len(pretty_maze)-1)
        for row in pretty_maze:
            row.pop(0)
            row.pop(len(row)-1)
        length = len(pretty_maze)-1
        # Placing the destination
        pretty_maze[length][length] = 2
        return pretty_maze

    def DFS(self, maze, coords=(0,0)):
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        shuffle(directions)
        for direction in directions:
            new_coords = (coords[0] + direction[0], coords[1] + direction[1])
            if (0 <= new_coords[0] < len(maze)) and (0 <= new_coords[1] < len(maze[0])) and not maze[new_coords[0]][new_coords[1]]:
                maze[coords[0]][coords[1]].append(direction)
                maze[new_coords[0]][new_coords[1]].append((-direction[0], -direction[1]))
                self.DFS(maze, new_coords)
        return maze

    ###   Algorithms   ###
    # Recursive Backtracker #
    # Solves the given maze using a recursive algorithm
    def search(self, grid, count=0, x=0, y=0):
        if grid[x][y] == 2:
            return True
        elif grid[x][y] == 1:
            return False
        elif grid[x][y] == 3:
            return False
        count += 1
        grid[x][y] = 3
        if ((x < (len(grid)-1) and self.search(grid, count, x+1, y))
            or (y > 0 and self.search(grid, count, x, y-1))
            or (x > 0 and self.search(grid, count, x-1, y))
            or (y < len(grid)-1 and self.search(grid, count, x, y+1))):
            return True
        return False 

    # # A* Algorithm #
    # # g = actual length from start cell to current cell
    # # h = estimated length from current cell to end (without walls)
    # # f = sum of g and h
    # class cell(object):
    #     def __init__(self, x, y, reachable):
    #         self.reachable
    #         self.x = x
    #         self.y = y
    #         self.parent = None
    #         self.g = 0
    #         self.h = 0
    #         self.f = 0

    # # Heapyfies the list with the lowest "f" at the top
    # # gets the size of the grid
    # class AStar(object):
    #     def __init__(self, x, y, reachable, height, width):
    #         self.opened = []
    #         heapq.heapify(self.opened)
    #         self.closed = set()
    #         self.cells = []
    #         self.grid_height = height
    #         self.grid_width = width

    # # Calculates distance from current to end
    # def get_h_value(self, cell):
    #     return 10 * (abs(cell.x - cell.end.x) + abs(cell.y - cell.end.y))

    # # Initializes the grid - gets start and end coordinate
    # # Checks where there's walls
    # def init_grid(grid, x, y):
    #     for x in range(self.grid_width):
    #         for y in range(self.grid_height):
    #             if grid[x][y] == 2:
    #                 reachable = False
    #             else:
    #                 reachable = True
    #             self.cells.append(Cell (x, y, reachable))
    #     self.start = self.get_cell(0,0)
    #     # For Testing:
    #     # self.end = self.get_cell(9,9)
    #     self.end = self.get_cell(self.grid_height, self.grid_width)

    # # Returns particular cell with given coordinates
    # def get_cell(self, x, y):
    #     return self.cells[x * self.grid_height + y]

    # # Retrieve Adjacent cells to specific cell
    # def get_adjacent_cells(self, cell):
    #     cells = []
    #     if cell.x < self.grid_width-1:
    #         cells.append(self.get_cell(cell.x+1, cell.y))
    #     if cell.y > 0:
    #         cells.append(self.get_cell(cell.x, cell.y-1))
    #     if cell.x > 0:
    #         cells.append(self.get_cell.x-1, cell.y)                                                                                                     
    #     if cell.y < self.grid_height-1:
    #         cells.append(self.get_cell(cell.x, cell.y+1))
    #     return cells                    

    # # Calculates G and H values and sets the parent cell
    # def update_cell(self, adj, cell):
    #     adj.g = cell.g + 10
    #     adj.h = self.get_h_value(adj)
    #     adj.parent = cell
    #     adj.f = adj.h + adj.g

    #     #
    #     def process(self):
    #         # Adds starting cell to open heap queue
    #         heapq.heappush(self.opened, (self.start.f, self.start))
    #         while len(self.opened):
    #             #
    #             f, cell = heapq.heappop(self.opened)
    #             #
    #             self.closed.add(cell)
    #             # If its ending cell "TO_DO" 
    #             if cell is self.end:
    #                 # TO_DO
    #                 break
    #             adj_cells = self.get_adjacent_cells(cell)
    #             for adj_cell in adj_cells:
    #                 if ((adj_cell.f, adj_cell) in self.opened):
    #                     if adj_cell.g > cell.g + 10:
    #                         self.update_cell(adj_cell, cell)
    #                 else:
    #                     self.update_cell(adj_cell, cell)
    #                     heapq.heappush(self.opened, (adj_cell.f, adj_cell))
                

    ### Algorithms end ###
    def generate_and_solve_multiple(self, repetitions, save):
        if(self.validate_input_range(repetitions, self.MIN_REPETITIONS, self.MAX_REPETITIONS)):
            sol_list = [self.search]
            gen_list = [self.depth_first_generation]
            p = ProducerThread(self.queue, repetitions, gen_list)
            c = ConsumerThread(self.queue, repetitions, sol_list)
            p.start()
            c.start()
            p.join()
            c.join()
            if(save == True):
                grids = []
                for maze in p.maze_list:
                    grids.append(maze.grid)
                self.save_multiple_mazes("producerconsumer.csv", grids)
            return p.maze_list
        else:
            raise exc.InvalidInputException("Repetitions must be a number between {} and {}".format(self.MIN_REPETITIONS, self.MAX_REPETITIONS))

class ProducerThread(Thread):
    def __init__(self, queue, repetitions, generation_alg, save=True):
        self.queue = queue
        self.repetitions = int(repetitions)
        self.maze_list = []
        self.generation_alg = generation_alg 
        self.save = save
        super(ProducerThread, self).__init__()

    def run(self):
        for size in range(5, 35, 5):
            for alg in self.generation_alg:
                maze = Maze(size, size)
                for i in range(self.repetitions):
                    start = time.perf_counter()
                    grid = alg(size, size)
                    end = time.perf_counter()
                    elapsed = (end - start) * 1000.0
                    maze.grid = grid
                    maze.generation_times.append(elapsed)
                    print("Generation time: {}ms".format(elapsed))
                self.maze_list.append(maze)
                self.queue.put(maze)
        self.queue.put([]) # Stops the consumer from running   
    
class ConsumerThread(Thread):
    def __init__(self, queue, repetitions, solution_alg, save=True):
        self.queue = queue
        self.repetitions = int(repetitions)
        self.solution_alg = solution_alg
        self.save = save
        self.running = True
        super(ConsumerThread, self).__init__()

    def run(self):
        while self.running:
            maze = self.queue.get()
            if maze:
                for alg in self.solution_alg:
                    for i in range(self.repetitions):
                        start = time.perf_counter()
                        grid = [row[:] for row in maze.grid] # Copy all elements in list by value instead of reference
                        alg(grid) 
                        end = time.perf_counter()
                        elapsed = (end - start) * 1000.0
                        maze.solution_times.append(elapsed)
                        print("Solution time: {}ms".format(elapsed))
                    print("\n")
                    self.queue.task_done()
            else:
                self.running = False