# This source file is made to be the interface Ui that
# the user will interact with. At the moment there are
# 3 pages, main page to import roadmap file
# and go to other pages, planner page where user can
# look/modify task, and last page that tell the user
# undated task.
# input: none
# output: none

# Created by Gold, 20 October 2024
# Modified by Gold, 29 October 2024

import tkinter as tk  # graphic library for GUI
from tkinter import ttk
from tkinter import filedialog  # for importing file

DEFAULTFONT = ("Arial", 12)  # define default font


class App(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("A1CE Study Planner")
        container = tk.Frame(self)

        # set initial size of the window

        self.geometry("1000x800")
        self.grid_columnconfigure(0, weight=1)
        container.grid(row=0, column=0, sticky="nsew")

        # container.grid_columnconfigure(0, weight=1)
        # container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        # for frames in the 3 pages, create frame to store them
        for F in (MainPage, Planner, Undated):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

    # show the chosen frame
    # input: Name of frame
    # output: None
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # bring to frame in


# Main page
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self)
        # self.grid_columnconfigure(0, weight=1)

        # Main page label
        # Initialize style
        # Create style used by default for all Frames

        menu_frame = tk.LabelFrame(self, text="function", bg="#2a2f54", fg='black')
        menu_frame.place(x=0, y=0, relwidth=0.2, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        to_main = tk.Button(menu_frame, text="Main", width=20, height=2,
                                   font=DEFAULTFONT, command=lambda: controller.show_frame(MainPage))
        to_main.grid(row=0, column=0, padx=10, pady=10)

        to_planner = tk.Button(menu_frame, text="Planner", width=20, height=2,
                         font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        to_planner.grid(row=2, column=0, padx=10, pady=10)

        to_undated = tk.Button(menu_frame, text="Undated", width=20, height=2,
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Undated))
        to_undated.grid(row=4, column=0, padx=10, pady=10)


        function_frame = tk.LabelFrame(self, text="option", bg="#ff9851", fg='black')
        function_frame.place(relx=0.2, y=0, relwidth=0.8, relheight=1)
        function_frame.columnconfigure((0, 1, 2), weight=1)
        function_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)


        # Import Roadmap Button
        import_button = tk.Button(function_frame, text="Import Roadmap", width=20, height=2,
                                       font=DEFAULTFONT, command=self.open_file)
        import_button.grid(row=1, column=1, padx=20, pady=10)

        # Clear Roadmap Button
        clear_button = tk.Button(function_frame, text="Clear Roadmap", width=20, height=2,
                                      font=DEFAULTFONT)
        clear_button.grid(row=2, column=1, padx=20, pady=40)

        # View Planner Button
        planner_button = tk.Button(function_frame, text="View Planner", width=20, height=2,
                                        font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        planner_button.grid(row=3, column=1, padx=20, pady=40)

    # Ask for filepath and print it
    # input: None
    # output: filepath
    def open_file(self):
        filepath = filedialog.askopenfilename()
        print(filepath)


# Display Task
class Planner(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self)
        self.grid_columnconfigure(0, weight=1)

        menu_frame = tk.LabelFrame(self, text="function", bg="#2a2f54", fg='black')
        menu_frame.place(x=0, y=0, relwidth=0.2, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        to_main = tk.Button(menu_frame, text="Main", width=20, height=2,
                            font=DEFAULTFONT, command=lambda: controller.show_frame(MainPage))
        to_main.grid(row=0, column=0, padx=10, pady=10)

        to_planner = tk.Button(menu_frame, text="Planner", width=20, height=2,
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        to_planner.grid(row=2, column=0, padx=10, pady=10)

        to_undated = tk.Button(menu_frame, text="Undated", width=20, height=2,
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Undated))
        to_undated.grid(row=4, column=0, padx=10, pady=10)

        function_frame = tk.LabelFrame(self, text="option", bg="#ff9851", fg='black')
        function_frame.place(relx=0.2, y=0, relwidth=0.8, relheight=1)
        function_frame.columnconfigure(0, weight=1)
        function_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)


        label = tk.Label(function_frame, text="Planner", font=DEFAULTFONT)
        label.grid(row=0, column=0, pady=10, padx=10)

        table = ttk.Treeview(function_frame, columns=("comp_id", "comp_name", "skill_code", "skill_name"), show="headings")
        table.heading('comp_id', text="Competency Code")
        table.heading('comp_name', text="Competency Name")
        table.heading('skill_code', text="Skill Code")
        table.heading('skill_name', text="Skill Name")
        table.grid(row=2, column=0, sticky="nsew")
        table.insert(parent='', index=0, values=("AIC-401", " Information Retrieval, Extraction, Search and Indexing "
                                                 , " AIC-401:00030", " Understand ranking algorithms"))

        main = tk.Button(function_frame, text="back", width=20, height=2,
                             font=DEFAULTFONT,
                             command=lambda: controller.show_frame(MainPage))
        main.grid(row=3, column=0, sticky="s", padx=20, pady=40)

        lastpage = tk.Button(function_frame, text="next", width=20, height=2,
                                        font=DEFAULTFONT,
                              command=lambda: controller.show_frame(Undated))
        lastpage.grid(row=4, column=0, sticky="s", padx=20, pady=40)


# Display Undated Task
class Undated(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self)
        self.grid_columnconfigure(0, weight=1)

        menu_frame = tk.LabelFrame(self, text="function", bg="#2a2f54", fg='black')
        menu_frame.place(x=0, y=0, relwidth=0.2, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        to_main = tk.Button(menu_frame, text="Main", width=20, height=2,
                            font=DEFAULTFONT, command=lambda: controller.show_frame(MainPage))
        to_main.grid(row=0, column=0, padx=10, pady=10)

        to_planner = tk.Button(menu_frame, text="Planner", width=20, height=2,
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        to_planner.grid(row=2, column=0, padx=10, pady=10)

        to_undated = tk.Button(menu_frame, text="Undated", width=20, height=2,
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Undated))
        to_undated.grid(row=4, column=0, padx=10, pady=10)

        function_frame = tk.LabelFrame(self, text="option", bg="#ff9851", fg='black')
        function_frame.place(relx=0.2, y=0, relwidth=0.8, relheight=1)
        function_frame.columnconfigure(0, weight=1)
        function_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)

        label = tk.Label(function_frame, text="Undated", font=DEFAULTFONT)
        label.grid(row=0, column=0, pady=10, padx=10)

        table2 = ttk.Treeview(function_frame, columns=("comp_id", "comp_name",
                                                       "skill_code", "skill_name"), show="headings")
        table2.heading('comp_id', text="Competency Code")
        table2.heading('comp_name', text="Competency Name")
        table2.heading('skill_code', text="Skill Code")
        table2.heading('skill_name', text="Skill Name")
        table2.grid(row=1, column=0, sticky="nsew")
        table2.insert(parent='', index=0, values=("AIC-401", "Undated Task", "Undated Task", "Undated Task"))
        table2.insert(parent='', index=1, values=("AIC-401", "Undated Task", "Undated Task", "Undated Task"))

        # for some reason editing this button mess with the whole screen
        backplanner = tk.Button(self, text="", width=1, height=40, font=DEFAULTFONT,
                          command=lambda: controller.show_frame(Planner))
        backplanner.grid(row=4, column=6, sticky="e", padx=20, pady=40)


# call to initiate app
app = App()
app.mainloop()
