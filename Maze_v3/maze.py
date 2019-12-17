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
    
    # Copy all elements in list by value instead of reference
    def copy_maze(self):
        return [x[:] for x in self.grid]