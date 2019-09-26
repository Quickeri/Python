from model import Maze

#Returns an empty maze of given size
def make_empty_maze(height, width):
    maze = [[[] for b in range(width)] for a in range(height)]
    return maze

def convert(maze):
    pretty_maze = [["1"]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
    for y,row in enumerate(maze):
        for x,col in enumerate(row):
            pretty_maze[2*y+1][2*x+1] = "0"
            for direction in col:
                pretty_maze[2*y+1+direction[0]][2*x+1+direction[1]] = "0"
    return pretty_maze

#Takes a converted maze and pretty prints it
def pretty_print(maze):
    for a in convert(maze):
        string = ""
        for b in a:
            string += b
        print (string)
    print("")

def showAllView(list):
    print ('In db we have %i coordinates. Shown here: ' % len(list))
    for item in list:
        print (item.grid())
def showEmptyMazes():
    size = 5
    pretty_print(make_empty_maze(size, size))

def startView():
    print ('MVC - Simple example')
    print ('Do you want to see the GRID?')
def endView():
    print ('Goodbye!')


# from model import Person
# def showAllView(list):
#    print ('In our db we have %i users. Here they are:' % len(list))
#    for item in list:
#       print (item.name())
# def startView():
#    print ('MVC - the simplest example')
#    print ('Do you want to see everyone in my db?[y/n]')
# def endView():
#    print ('Goodbye!')