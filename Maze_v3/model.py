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
        self.min_size = 4
        self.max_size = 50

    #Checks if the input string is a number within the given range - returns a boolean
    def validate_input_range(self, user_input, min_value, max_value):
        input_valid = False
        if(user_input.isdigit()):
            user_input = int(user_input)
            if(user_input > min_value and user_input < max_value):
                input_valid = True
        return input_valid

    #Checks if the file exists, and the format is correct
    def validate_csv_file(self, path_to_file):
        input_valid = False
        if(os.path.exists(path_to_file)):
            drive, path = os.path.splitdrive(path_to_file)
            filename, filetype = os.path.splitext(path)
            if(filetype == ".csv"):
                input_valid = True
        return input_valid

    #Generates a single maze from a given generation algorithm(String) and a file path
    def generate_single_maze(self, generation_algorithm, size):
        if(self.validate_input_range(size, self.min_size, self.max_size)):
            size = int(size)
            gen_alg = self.select_gen_algorithm(generation_algorithm)
            Thread(target=self.gen_maze, args=(gen_alg, self.queue, size)).start()
            maze = self.queue.get()
            self.save_maze("maze.csv", maze)
            return maze
        else:
            raise exc.InvalidInputException("Invalid input - maze size must be a number between 4 and 50")
    
    def generate_multiple_mazes(self):
        pass

    #Solves a single maze from a given solution algorithm(String) and file path
    def solve_single_maze(self, solution_algorithm, path_to_file):
        if(self.validate_csv_file(path_to_file)):
            maze = self.read_maze(path_to_file)
            sol_alg = self.select_sol_algorithm(solution_algorithm)
            Thread(target=self.sol_maze, args=(sol_alg, self.queue, maze)).start()
            moves = self.queue.get()
            size = 5
            time = 1.023123
            return size, moves, time
        else:
            raise exc.InvalidInputException("Unable to read the file - wrong extention type or maze format")
    
    def solve_multiple_mazes(self, solution_algorithm, path_to_file, repetitions):
        if(self.validate_csv_file(path_to_file)):
            mazes = self.read_multiple_mazes(path_to_file)
            sol_alg = self.select_sol_algorithm(solution_algorithm)
            Thread(target=self.sol_maze, args=(sol_alg, self.queue, mazes)).start()
            solved_mazes = self.queue.get() 
            return solved_mazes
        else:
            raise exc.InvalidInputException("Unable to read the file - wrong extention type or maze format")

    #Generates a single maze using the given algorithm and puts it into the given queue
    def gen_maze(self, gen_alg, queue, size):
        generated_maze = gen_alg(size, size) 
        queue.put(generated_maze)

    #Generates a single maze using the given algorithm and puts it into the given queue
    def sol_maze(self, sol_alg, queue, maze):
        #pass the maze count to alg
        solved = sol_alg(maze) 
        queue.put(solved)
    
    def sol_multiple_mazes(self, sol_alg, queue, mazes, repetitions):
        for maze in mazes:
            for i in range(repetitions):
                start = time.perf_counter()
                sol_alg(maze.maze) 
                end = time.perf_counter()
                elapsed = (end - start) * 1000.0
                maze.solution_times() 
            queue.put(maze)

    #Returns a reference to a generation algorithm if the key exists in the dictionary
    def select_gen_algorithm(self, name):
        generation_algorithms = {"DFS": self.depth_first_generation}
        if(name in generation_algorithms):
            return generation_algorithms[name]
        else:
            raise exc.InvalidInputException("Generation algorithm not found")

    #Returns a reference to a solution algorithm if the key exists in the dictionary
    def select_sol_algorithm(self, name):
        solution_algorithms = {"Recursive": self.search}
        if(name in solution_algorithms):
            return solution_algorithms[name]
        else:
            raise exc.InvalidInputException("Solution algorithm not found")

    #List of the available generation algorithms
    def get_gen_algorithms(self):
        generation_algorithms = ["DFS", "A*", "Recurisve"] 
        return generation_algorithms

    #List of the available solution algorithms
    def get_sol_algorithms(self):
        solutions_algorithms = ["Recursive", "BFS", "DFS"] 
        return solutions_algorithms

    def calc_average(self, values):
        return sum(values) / len(values)

    def save_maze(self, filename, maze):
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(maze)

    def read_maze(self, filename): #Change maze to object, with height and width
        maze = []
        with open(filename, 'r') as f:
            maze = [list(map(int, el)) for el in csv.reader(f, delimiter=',')]
        return maze 

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
            temp_maze = []
            for row in reader: 
                if(row):
                    temp_maze.append(row)
                else:
                    temp_maze = [list(map(int, el)) for el in temp_maze]
                    maze = temp_maze.copy()
                    mazes.append(maze)
                    temp_maze.clear()
        return mazes 

    #Generates and returns a maze with the given height and width, using the depth first algorithm
    def depth_first_generation(self, height, width):
        converted_maze = self.convert(self.DFS(self.make_empty_maze(height, width)))
        return converted_maze

    #Returns an empty maze of a given size
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
        #Removing the walls around the maze
        pretty_maze.pop(0)
        pretty_maze.pop(len(pretty_maze)-1)
        for row in pretty_maze:
            row.pop(0)
            row.pop(len(row)-1)
        length = len(pretty_maze)-1
        #Placing the destination
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

    #Solves the given maze using a recursive algorithm
    def search(self, grid, count=0, x=0, y=0):
        if grid[x][y] == 2:
            return True
        elif grid[x][y] == 1:
            return False
        elif grid[x][y] == 3:
            return False
        #moves.append("{},{}".format(x, y))
        count += 1
        print(count)
        grid[x][y] = 3
        if ((x < (len(grid)-1) and self.search(grid, count, x+1, y))
            or (y > 0 and self.search(grid, count, x, y-1))
            or (x > 0 and self.search(grid, count, x-1, y))
            or (y < len(grid)-1 and self.search(grid, count, x, y+1))):
            return True
        return False 

class ProducerThread(Thread):
    def __init__(self, queue, repetitions, generation_alg, size):
        self.queue = queue
        self.repetitions = repetitions
        self.generation_alg = generation_alg
        self.size = size

    def run(self):
        #for size in range(5, 35, 5):
            for i in range(self.repetitions):
                if not self.queue.full():
                    start = time.perf_counter()
                    generated_maze = self.generation_alg(self.size, self.size)
                    end = time.perf_counter()
                    elapsed = (end - start) * 1000.0
                    #self.maze.generation_times.append(elapsed)
                    self.queue.put(generated_maze)
                    print("Generation time: {}ms".format(elapsed))    
    
class ConsumerThread(Thread):
    def __init__(self, queue, save=True, solve=True):
        self.queue = queue
        self.save = save
        self.solve = solve

    def run(self):
        while True:
            if not self.queue.empty():
                maze = self.queue.get()
                start = time.perf_counter()
                self.search(maze)
                end = time.perf_counter()
                elapsed = (end - start) * 1000.0
                self.queue.task_done()
                print("Solution time: {}ms".format(elapsed))

    def search(self, grid, x=0, y=0):
        if grid[x][y] == 2:
            return True
        elif grid[x][y] == 1:
            return False
        elif grid[x][y] == 3:
            return False
        #maze.moves += 1
        #visited.append(str((y, x)))
        grid[x][y] = 3
        if ((x < (len(grid)-1) and self.search(grid, x+1, y))
            or (y > 0 and self.search(grid, x, y-1))
            or (x > 0 and self.search(grid, x-1, y))
            or (y < len(grid)-1 and self.search(grid, x, y+1))):
            return True
        return False 

# class ProducerThread(Thread):
#     def run(self):
#         while True:
#             if not queue.full():
#                 start = time.perf_counter()
#                 converted_maze = convert(DFS(make_empty_maze(50, 50)))
#                 end = time.perf_counter()
#                 elapsed = (end - start) * 1000.0
#                 queue.put(converted_maze)
#                 print("Generation time: {}ms".format(elapsed))