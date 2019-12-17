from tkinter import *
from tkinter import Canvas, messagebox, Frame
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt


class View:
    def __init__(self, root, controller):
        self.root = root
        self.frame = Frame(root)
        self.frame.pack()
        #self.solve_frame = Frame(self.root)
        #self.solve_frame.pack(side=RIGHT)
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

    def load_solve_frame(self):
        solve_frame = Frame(self.root)
        solve_frame.pack(side=RIGHT)

    def load_view(self):  
        # L1 = Label(self.root, text="Minimum maze size")
        # L1.pack()
        # min_size_input = Entry(self.root, textvariable = self.min_size, font=("Calibri 12")) #Input field
        # min_size_input.pack(pady=5)
        # min_size_input.insert(0, "5")

        # L2 = Label(self.root, text="Maximum maze size")
        # L2.pack()
        # max_size_input = Entry(self.root, textvariable = self.max_size, font=("Calibri 12"))
        # max_size_input.pack(pady=5)
        # max_size_input.insert(0, "50")

        repetitions_label = Label(self.frame, text="Repetitions")
        repetitions_label.pack()
        repetitions_input = Entry(self.frame, textvariable = self.repetitions, font=("Calibri 12"))
        repetitions_input.pack(pady=5)
        repetitions_input.insert(0, "10")

        maze_size_label = Label(self.frame, text="Maze size")
        maze_size_label.pack()
        maze_size_input = Entry(self.frame, textvariable = self.single_maze_size, font=("Calibri 12")) #Input field
        maze_size_input.pack(pady=5)
        maze_size_input.insert(0, "10")

        select_maze_button = Button(self.frame, text = "Select maze file", command = self.select_file)
        select_maze_button.pack(pady=5)
        self.file_path_label = Label(self.frame)
        self.file_path_label.pack()

        save_file_checkbutton = Checkbutton(self.frame, text = "Save data to file", variable = self.save_data, onvalue = True, offvalue = False)
        save_file_checkbutton.pack(pady=5)

        sol_algorithm_label = Label(self.frame, text="Solution")
        sol_algorithm_label.pack()
        sol_algorithm = OptionMenu(self.frame, self.sol, *self.controller.get_sol_algorithms())
        sol_algorithm.pack(pady=5)

        solve_maze_button = Button(self.frame, text = "Solve single maze", command = lambda: self.controller.solve_single_maze(self.sol.get(), self.maze_file_name.get(), self.repetitions.get()))
        solve_maze_button.pack(pady=5)

        gen_algorithm_label = Label(self.frame, text="Generation")
        gen_algorithm_label.pack()
        gen_algorithm = OptionMenu(self.frame, self.gen, *self.controller.get_gen_algorithms())
        gen_algorithm.pack(pady=5)
        
        create_maze_button = Button(self.frame, text = "Create single maze", command = lambda: self.controller.generate_single_maze(self.gen.get(), self.single_maze_size.get(), self.repetitions.get()))
        create_maze_button.pack(pady=5)

        create_and_solve_button = Button(self.frame, text = "Create and solve", command = lambda: self.controller.generate_and_solve_multiple(self.repetitions.get(), self.save_data.get()))
        create_and_solve_button.pack(pady=5)

        load_maze_data_button = Button(self.frame, text = "Load Maze Data", command = lambda: self.controller.load_maze_data_from_file(self.maze_file_name.get()))
        load_maze_data_button.pack(pady=5)

    def show_graph(self):
        plt.show()

    def plot_graph(self, x, y):
        plt.plot(x, y)

    def setup_plot(self, fig_nr, title, title2, xlabel, ylabel):
        plt.figure(fig_nr)
        plt.title("{}\n{}".format(title, title2))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
