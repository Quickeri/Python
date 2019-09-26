from model import Maze
import view

# def start():
#     print("Hello from start")


def showEmptyMaze():
    return view.showEmptyMazes()

def showAll():
    coordinats_in_db = Maze.getAll()
    return view.showAllView(coordinats_in_db)

def start():
    view.startView()
    textInput = input("")
    if textInput == "y":
        # return showAll()
        return showEmptyMaze()
    else:
        return view.endView()

if __name__ == "__main__":
    start()

