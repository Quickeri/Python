import model as m

#Takes a converted maze and pretty prints it
def pretty_print(maze):
    print("")
    for a in m.convert(maze):
        string = ""
        for b in a:
            string += str(b)
        print (string)
    print("")

def print_time(time):
    print("Elapsed time: {:.3f}ms".format(time))

def start_view():
    print("Please enter a grid size")

def choose_solution():
    print("Please choose one of the following algorithms:")
    print("1. Recursive Algorithm")

def incorrect_input():
    print("Please enter a grid size between 3 and 50")

def incorrect_input2():
    print("Invalid input, please try again")

def print_solution():
    print("Solved in: {} moves".format(len(m.visited)))
