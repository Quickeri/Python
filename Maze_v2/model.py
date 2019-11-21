from random import randint, shuffle, choice
import exceptions as exc
import csv
import sys

sys.setrecursionlimit(10000)

#Returns an empty maze of a given size
def make_empty_maze(height, width):
    maze = [[[] for b in range(width)] for a in range(height)]
    return maze

def convert(maze):
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

def DFS(maze, coords=(0,0)):
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    shuffle(directions)
    for direction in directions:
        new_coords = (coords[0] + direction[0], coords[1] + direction[1])
        if (0 <= new_coords[0] < len(maze)) and (0 <= new_coords[1] < len(maze[0])) and not maze[new_coords[0]][new_coords[1]]:
            maze[coords[0]][coords[1]].append(direction)
            maze[new_coords[0]][new_coords[1]].append((-direction[0], -direction[1]))
            DFS(maze, new_coords)
    return maze

#List of coordinates visited when solving the maze
visited = []
times = []
moves = []
def search(grid, x, y):
    if grid[x][y] == 2:
        #print("Found exit at ({}, {})".format(x, y))
        return True
    elif grid[x][y] == 1:
        return False
    elif grid[x][y] == 3:
        return False
    visited.append(str((y, x)))
    grid[x][y] = 3
    if ((x < (len(grid)-1) and search(grid, x+1, y))
        or (y > 0 and search(grid, x, y-1))
        or (x > 0 and search(grid, x-1, y))
        or (y < len(grid)-1 and search(grid, x, y+1))):
        return True
    return False

def save_maze(filename, maze):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(maze)

def read_maze(filename):
    maze = []
    with open(filename, 'r') as f:
        maze = [list(map(int, el)) for el in csv.reader(f, delimiter=',')]
    return maze      

def save_maze_data(filename, maze_data):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        for row in maze_data:
            for value in maze_data[row]:
                writer.writerow([row, value, maze_data[row][value]])

# Saves to csv with no headers or field names
def save_maze_data2(filename, maze_data):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        for size in maze_data:
            writer.writerow([size, maze_data[size]['moves'], maze_data[size]['avg_time'], maze_data[size]['min_time'], maze_data[size]['max_time']])

def load_maze_data(filename):
    maze_data = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f, delimiter=(','))
        for row in reader:
            print(row)
    return maze_data

# Loads the maze data from csv 
def load_maze_data2(filename):
    maze_data = {}
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=(','))
        for row in reader:
            maze_data[row[0]] = {'moves': row[1], 'avg_time': row[2], 'min_time': row[3], 'max_time': row[4]}
    return maze_data

def available_algorithms(choice):
    solutions = {"1": "Recursive"}
    #solutions = {"1": {"name": "Recursive", "algorithm": search}}
    if choice not in solutions.keys():
        raise exc.InvalidInputException("Invalid input - Please try again")
    else:
        return solutions[choice]

def get_solutions():
    solutions = {"1": "Recursive"}
    return solutions
    
def calc_average(values):
    return sum(values) / len(values)
