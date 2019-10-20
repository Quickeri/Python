from random import randint, shuffle, choice
import sys

sys.setrecursionlimit(10000)

#Returns an empty maze of given size
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
def search(grid, x, y):
    if grid[x][y] == 2:
        # Found
        return True
    elif grid[x][y] == 1:
        # Wall
        return False
    elif grid[x][y] == 3:
        # Visiting?
        return False
    visited.append(str((x, y)))
    grid[x][y] = 3
    if ((x < (len(grid)-1) and search(grid, x+1, y))
        or (y > 0 and search(grid, x, y-1))
        or (x > 0 and search(grid, x-1, y))
        or (y < len(grid)-1 and search(grid, x, y+1))):
        return True
    return False
