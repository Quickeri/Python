import model as m
import matplotlib.pyplot as plt
import plot as p
import exceptions as exc
import view
import sys
import time

def solve_multiple_mazes(solution_alg, loop):
    maze_data = {}
    for size in range(5, 35, 5):
        maze_data[size] = {}
        empty_maze = m.make_empty_maze(size, size)
        maze = m.DFS(empty_maze)
        converted_maze = m.convert(maze)
        #m.save_maze("maze.csv", converted_maze)
        #loaded_maze = m.read_maze("maze.csv")
        times, moves = solve_with_algorithm(solution_alg, converted_maze, loop)
        maze_data[size]["moves"] = moves[0]
        maze_data[size]["avg_time"] = m.calc_average(times)
        maze_data[size]["min_time"] = min(times)
        maze_data[size]["max_time"] = max(times)
        view.print_result(maze_data, size)
        #view.print_times(times)
    return maze_data

def solve_with_algorithm(choice, maze, loop):
    if(choice == "1"):
        times = []
        moves = []
        times.clear()
        moves.clear()
        for i in range(loop):
            start = time.perf_counter()
            m.search(maze, 0, 0)
            end = time.perf_counter()
            elapsed = (end - start) * 1000.0
            times.append(elapsed)
            moves.append(len(m.visited))
            m.reset_search(maze)
    return times, moves

def prepare_data(maze_data):
    keys = []
    avg_time = []
    moves = []
    for key in maze_data.keys():
        keys.append(key)
        avg_time.append(maze_data[key]["avg_time"])
        moves.append(maze_data[key]["moves"])
    return keys, avg_time, moves

def choose_sol_alg(alg):
    try:
        algorithm = m.available_algorithms(alg)
        return algorithm
    except exc.InvalidInputException as e:
        view.show_invalid_input_error(e)
        sys.exit(1)

def start():
    loop = view.cli_args()
    #generation_alg = view.choose_generation()
    solution_alg = view.choose_solution(m.get_solutions())
    sol_algorithm = choose_sol_alg(solution_alg)
    maze_data = solve_multiple_mazes(solution_alg, loop)

    m.save_maze_data2("mazedata.csv", maze_data)
    #data = m.load_maze_data2("mazedata.csv")
    keys, avg_time, moves = prepare_data(maze_data)

    plt.figure(1)
    title = "Relationship between the maze size and average solution time"
    title2 = "Loops: {}".format(loop)
    p.setup_plot(title, title2, "Maze Size", "Time (ms)")
    plt.plot(keys, avg_time, label=sol_algorithm)
    plt.legend()

    plt.figure(2)
    title = "Relationship between the maze size and amount of moves"
    title2 = "Loops: {}".format(loop)
    p.setup_plot(title, title2, "Maze Size", "Moves")
    plt.plot(keys, moves, label=sol_algorithm)
    plt.legend()
    plt.show()  

if __name__ == "__main__":
    start()