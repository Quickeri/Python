import model as m
import controller as c
import argparse

#Takes a converted maze and pretty prints it
def pretty_print(maze):
    print("")
    for a in m.convert(maze):
        string = ""
        for b in a:
            string += str(b)
        print (string)
    print("")

def cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", "-l", type=range_type, required=False, default=1)
    args = parser.parse_args()
    loop = args.loop
    return loop

def range_type(arg):
    value = int(arg)
    if(value >= 1 and value <= 1000):
        return value
    else:
        raise argparse.ArgumentTypeError("Please enter a number from 1 to 100")

def show_invalid_input_error(err):
    print("{}".format(err))

def print_total_time(start, end):
    print("Total elapsed time: {:.3f}ms".format((end - start) * 1000))

def choose_size():
    print("Please enter a grid size")
    size = input("")
    return size

def choose_solution(solutions):
    print("Please choose one of the following solution algorithms:")
    #print("1. Recursive Algorithm")
    for algorithm in solutions:
        print("{}: {}".format(algorithm, solutions[algorithm]))
    algorithm = input("")
    return algorithm

def choose_generation():
    print("Please choose one of the following generation algorithms:")
    print("1. Depth First Algorithm")
    algorithm = input("")
    return algorithm

def print_times(times):
    print(times)
    
def print_result(maze_data, size):
    #print(times)
    print("\n")
    print("Maze: {}x{}".format(size, size))
    print("Average time: {}ms".format(maze_data[size]["avg_time"]))        
    print("Minimum time: {}ms".format(maze_data[size]["min_time"]))
    print("Maximum time: {}ms".format(maze_data[size]["max_time"]))
    print("Amount of moves: {}".format(maze_data[size]["moves"]))
