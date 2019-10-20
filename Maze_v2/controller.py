import model as m
import view
import time

def choose_maze_size(size):
    maze = None
    if(size.isdigit()):
        grid_size = int(size)
        if(grid_size <= 1 or grid_size >= 50):
            view.incorrect_input()
        else:
            maze = m.make_empty_maze(grid_size, grid_size)
    else:
        view.incorrect_input()
    return maze

def solve_with_algorithm(choice, maze):
    solved = False
    #Recursive 
    if(choice == "1"):
        m.search(maze, 0, 0)
        solved = True
    else:
        view.incorrect_input2()
    return solved
 
def start():
    view.start_view()
    size = input("")
    view.choose_solution()
    algorithm = input("")
    start = time.time()
    empty_maze = choose_maze_size(size)
    #print(empty_maze)
    if(empty_maze != None):
        maze = m.DFS(empty_maze)
        converted_maze = m.convert(maze)
        print(converted_maze)
        solved = solve_with_algorithm(algorithm, converted_maze)
        if(solved):
            view.pretty_print(maze)
            view.print_solution()
            end = time.time()
            elapsed = (end - start) * 1000.0
            #print("Start: {:.3f}".format(start))
            #print("End: {:.3f}".format(end))
            view.print_time(elapsed)
            # Persist maze data
          
if __name__ == "__main__":
    start()