import csv

class Maze:
    def __init__(self, height, width, grid=[]):
        self.height = height
        self.width = width
        self.grid = grid #use list.copy() to create new list instead of a reference? Search() will modify the list
        self.generation_times = [] #use dictionary instead (algorithm as key, list of times as value)
        self.solution_times = []
        self.moves = []
        self.count = 0

    def pretty_print(self):
        for a in self.grid:
            string = ""
            for b in a:
                string += str(b)
            print (string)
        print("")   

    # Saves to csv with no headers or field names
    def save_maze_data(self, filename, maze_data):
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            for size in maze_data:
                writer.writerow([size, maze_data[size]['moves'], maze_data[size]['avg_time'], maze_data[size]['min_time'], maze_data[size]['max_time']])
    
    # Loads the maze data from csv 
    def load_maze_data(self, filename):
        maze_data = {}
        with open(filename, "r") as f:
            reader = csv.reader(f, delimiter=(','))
            for row in reader:
                maze_data[row[0]] = {'moves': row[1], 'avg_time': row[2], 'min_time': row[3], 'max_time': row[4]}
        return maze_data
    
    # Copy all elements in list by value instead of reference
    def copy_maze(self):
        return [x[:] for x in self.grid]