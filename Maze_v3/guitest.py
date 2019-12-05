from tkinter import *
from tkinter import Canvas, messagebox
import controller as c

def get_values():
    msg = messagebox.showinfo( "Information", "{}, {}, {}, {}, {}, {}".format(min_size.get(), max_size.get(), repetitions.get(), save_data.get(), sol.get(), gen.get()))

root = Tk()
root.minsize(height = 400, width = 800)
C = Canvas(root, height = 400, width = 800)

min_size = StringVar() 
max_size = StringVar() 
repetitions = StringVar()
save_data = BooleanVar()
single_maze_size = StringVar() 
#def validate_input(value):
#    valid = value.isdigit() and len(value) <= 30
#    return valid

#validate = root.register(validate_input)

#labelframe = LabelFrame(root, text="This is a LabelFrame")
#labelframe.pack(fill="both", expand="yes")
#left = Label(labelframe, text="Inside theLabelFrame")
#left.pack()

#L1 = Label(root, text="Minimum maze size")
#L1.pack()
min_size_input = Entry(root, textvariable = min_size, font=("Calibri 12")) #Input field
min_size_input.pack(pady=5)
min_size_input.insert(0, "Minimum maze size")

#text = Text(root, height=5, width=20) #Text field
#text.pack()

#L2 = Label(root, text="Maximum maze size")
#L2.pack()
max_size_input = Entry(root, textvariable = max_size, font=("Calibri 12"))
max_size_input.pack(pady=5)
max_size_input.insert(0, "Maximum maze size")

#L3 = Label(root, text="Repetitions")
#L3.pack()
max_size_input = Entry(root, textvariable = repetitions, font=("Calibri 12"))
max_size_input.pack(pady=5)
max_size_input.insert(0, "Maximum maze size")

C1 = Checkbutton(root, text = "Save data to file", variable = save_data, onvalue = True, offvalue = False)
C1.pack(pady=5)

solutions_algorithms = ["Recurisve", "A*", "DFS"] 
sol = StringVar(root)
sol.set(solutions_algorithms[0]) # default value
sol_algorithm = OptionMenu(root, sol, *solutions_algorithms)
sol_algorithm.pack(pady=5)

generation_algorithms = ["DFS", "BFS"] 
gen = StringVar(root)
gen.set(generation_algorithms[0]) # default value
sol_algorithm = OptionMenu(root, gen, *generation_algorithms)
sol_algorithm.pack(pady=5)

#start_button = Button(root, text = "Start Program", command = c.add)
#start_button.pack(pady=5)

min_size_input = Entry(root, textvariable = single_maze_size, font=("Calibri 12")) #Input field
min_size_input.pack(pady=5)
min_size_input.insert(0, "Single maze size")

create_maze_button = Button(root, text = "Create single maze", command = get_values)
create_maze_button.pack(pady=5)

root.mainloop() 