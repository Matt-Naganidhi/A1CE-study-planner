# This source file is made to be the interface Ui that
# the user will interact with. At the moment there are
# 3 pages, main page to import roadmap file
# and go to other pages, planner page where user can
# look/modify task, and last page that tell the user
# undated task.
# input: none
# output: none

# Crated by Gold, 20 October 2024

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
        self.geometry("800x800")
        self.grid_columnconfigure(0, weight=1)
        container.grid(row=0, column=0, sticky="nsew")

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

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
        self.grid_columnconfigure(0, weight=1)

        # Main page label
        label = tk.Label(self, text="MainPage", font=DEFAULTFONT)
        label.grid(row=0, column=0, padx=10, pady=10)

        # Button to go to next page
        button1 = tk.Button(self, text="go next", width=50, font=DEFAULTFONT,
                             command=lambda: controller.show_frame(Planner))
        button1.grid(row=8, column=0, sticky="")

        # Import Roadmap Button
        import_button = tk.Button(self, text="Import Roadmap", width=20, height=2,
                                       font=DEFAULTFONT, command=self.open_file)
        import_button.grid(row=2, column=0, padx=20, pady=10)

        # Clear Roadmap Button
        clear_button = tk.Button(self, text="Clear Roadmap", width=20, height=2,
                                      font=DEFAULTFONT)
        clear_button.grid(row=4, column=0, padx=20, pady=40)

        # View Planner Button
        planner_button = tk.Button(self, text="View Planner", width=20, height=2,
                                        font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        planner_button.grid(row=5, column=0, padx=20, pady=40)

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
        label = tk.Label(self, text="Planner", font=DEFAULTFONT)
        label.grid(row=0, column=0, pady=10, padx=10)

        table = ttk.Treeview(self, columns=("comp_id", "comp_name", "skill_code", "skill_name"), show="headings")
        table.heading('comp_id', text="Competency Code")
        table.heading('comp_name', text="Competency Name")
        table.heading('skill_code', text="Skill Code")
        table.heading('skill_name', text="Skill Name")
        table.grid(row=1, column=0, sticky="nsew")
        table.insert(parent='', index=0, values=("AIC-401", " Information Retrieval, Extraction, Search and Indexing "
                                                 , " AIC-401:00030", " Understand ranking algorithms"))

        main = tk.Button(self, text="back", width=20, height=2,
                             font=DEFAULTFONT,
                             command=lambda: controller.show_frame(Undated))
        main.grid(row=7, column=0, sticky="s", padx=20, pady=40)

        lastpage = tk.Button(self, text="next", width=20, height=2,
                                        font=DEFAULTFONT,
                              command=lambda: controller.show_frame(Undated))
        lastpage.grid(row=6, column=0, sticky="s", padx=20, pady=40)


# Display Undated Task
class Undated(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self)
        self.grid_columnconfigure(0, weight=1)
        label = tk.Label(self, text="Undated", font=DEFAULTFONT)
        label.grid(row=0, column=0, pady=10, padx=10)

        table = ttk.Treeview(self, columns=("comp_id", "comp_name", "skill_code", "skill_name"), show="headings")
        table.heading('comp_id', text="Competency Code")
        table.heading('comp_name', text="Competency Name")
        table.heading('skill_code', text="Skill Code")
        table.heading('skill_name', text="Skill Name")
        table.grid(row=1, column=0, sticky="nsew")
        table.insert(parent='', index=0, values=("AIC-401", "Undated Task", "Undated Task", "Undated Task"))
        table.insert(parent='', index=1, values=("AIC-401", "Undated Task", "Undated Task", "Undated Task"))

        back1 = tk.Button(self, text="Back to main", width=20, height=2, font=DEFAULTFONT,
                          command=lambda: controller.show_frame(MainPage))
        back1.grid(row=6, column=0, sticky="nsew", padx=20, pady=40)

        back2 = tk.Button(self, text="To Planner", width=20, height=2, font=DEFAULTFONT,
                          command=lambda: controller.show_frame(MainPage))
        back2.grid(row=5, column=0, sticky="nsew", padx=20, pady=40)


# call to initiate app
app = App()
app.mainloop()
