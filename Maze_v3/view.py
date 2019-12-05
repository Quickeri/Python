from tkinter import *
from tkinter import Canvas, messagebox, Frame
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt


class View:
    def __init__(self, root, controller):
        self.root = root
        #self.frame = Frame(root)
        self.controller = controller
        self.min_size = StringVar()
        self.max_size = StringVar() 
        self.repetitions = StringVar()
        self.save_data = BooleanVar()
        self.single_maze_size = StringVar() 
        self.sol = StringVar()
        self.maze_file_name = StringVar()
        self.sol.set(controller.get_sol_algorithms()[0]) # default value
        self.gen = StringVar()
        self.gen.set(controller.get_gen_algorithms()[0]) # default value
        self.load_view()

    def get_values(self):
        messagebox.showinfo( "Information", "{}, {}, {}, {}".format(self.min_size.get(), self.max_size.get(), self.repetitions.get(), self.maze_file_name.get()))

    def show_messagebox(self, header, message):
        messagebox.showinfo( "{}".format(header), "{}".format(message))

    def select_file(self):
        filename = askopenfilename(filetypes=(("CSV files", "*.csv"),("All files", "*.*")))
        self.maze_file_name.set(filename)
        self.file_path_label.config(text = filename)

    def load_view(self):  
        L1 = Label(self.root, text="Minimum maze size")
        L1.pack()
        min_size_input = Entry(self.root, textvariable = self.min_size, font=("Calibri 12")) #Input field
        min_size_input.pack(pady=5)
        min_size_input.insert(0, "5")

        L2 = Label(self.root, text="Maximum maze size")
        L2.pack()
        max_size_input = Entry(self.root, textvariable = self.max_size, font=("Calibri 12"))
        max_size_input.pack(pady=5)
        max_size_input.insert(0, "50")

        L3 = Label(self.root, text="Repetitions")
        L3.pack()
        repetitions_input = Entry(self.root, textvariable = self.repetitions, font=("Calibri 12"))
        repetitions_input.pack(pady=5)
        repetitions_input.insert(0, "10")

        C1 = Checkbutton(self.root, text = "Save data to file", variable = self.save_data, onvalue = True, offvalue = False)
        C1.pack(pady=5)

        L4 = Label(self.root, text="Solution algorithm")
        L4.pack()
        sol_algorithm = OptionMenu(self.root, self.sol, *self.controller.get_sol_algorithms())
        sol_algorithm.pack(pady=5)

        L5 = Label(self.root, text="Generation algorithm")
        L5.pack()
        gen_algorithm = OptionMenu(self.root, self.gen, *self.controller.get_gen_algorithms())
        gen_algorithm.pack(pady=5)

        start_button = Button(self.root, text = "Start Program", command = self.get_values)
        start_button.pack(pady=5)

        L6 = Label(self.root, text="Maze size")
        L6.pack()
        min_size_input = Entry(self.root, textvariable = self.single_maze_size, font=("Calibri 12")) #Input field
        min_size_input.pack(pady=5)
        min_size_input.insert(0, "10")

        create_maze_button = Button(self.root, text = "Create single maze", command = lambda: self.controller.generate_single_maze(self.gen.get(), self.single_maze_size.get(), self.repetitions.get()))
        create_maze_button.pack(pady=5)

        solve_maze_button = Button(self.root, text = "Solve single maze", command = lambda: self.controller.solve_single_maze(self.sol.get(), self.maze_file_name.get(), self.repetitions.get()))
        solve_maze_button.pack(pady=5)

        select_maze_button = Button(self.root, text = "Select maze file", command = self.select_file)
        select_maze_button.pack(pady=5)
        self.file_path_label = Label(self.root)
        self.file_path_label.pack()

    def show_graphs(self, keys, avg_time, moves):
        plt.figure(1)
        title = "Relationship between the maze size and average solution time"
        self.setup_plot(title, "", "Maze Size", "Time (ms)")
        plt.plot(keys, avg_time)
        plt.legend()

        plt.figure(2)
        title = "Relationship between the maze size and amount of moves"
        self.setup_plot(title, "", "Maze Size", "Moves")
        plt.plot(keys, moves)
        plt.legend()
        plt.show()  
    
    def setup_plot(self, title, title2, xlabel, ylabel):
        plt.title("{}\n{}".format(title, title2))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    