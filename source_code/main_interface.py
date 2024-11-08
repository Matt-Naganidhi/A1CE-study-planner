# This source file is made to be the interface Ui that
# the user will interact with. At the moment there are
# 3 pages, main page to import roadmap file
# and go to other pages, planner page where user can
# look/modify task, and last page that tell the user
# undated task.
# input: none
# output: none

# Created by Gold, 20 October 2024
# Modified by Gold, 4 November 2024

import tkinter as tk  # graphic library for GUI
import sqlite3
import pandas as pd
from tkinter import ttk  # extra function from the graphic library
from tkinter import filedialog, messagebox  # for importing file

from database import init_database, read_roadmap_data
import Task

DEFAULTFONT = ("Helvetica", 12, "bold")  # define default font
BIGFONT = ("Helvetica", 24, "bold")  # define big font


# Main application class that handles page switching
class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window geometry to 1000x800
        self.geometry("1400x800")
        self.title("A1CE Study Planner")

        # Container to hold all pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Dictionary to store pages
        self.pages = {}

        # Initialize pages
        for Page in (MainPage, Planner, Undated):
            page = Page(container, self)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        # set style of treeview
        ttk.Style().configure("Treeview", background="black",
                foreground="white")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        

        # Show the first page
        self.show_frame(MainPage)

        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def show_frame(self, page_class):
        page = self.pages[page_class]
        page.tkraise()  # Bring the page to the front
    
    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you want to quit"):
            print("Saving files")
            self.destroy()


# Main page 
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Configure page grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Menu frame that contain button to go to all pages
        menu_frame = tk.LabelFrame(self, bg="#001046", fg='black', bd=1)
        menu_frame.place(x=0, y=0, relwidth=0.15, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2), weight=1)

        to_main = tk.Button(menu_frame, text="Main", width=20, height=5, 
                                fg="white", bg="black",
                                font=DEFAULTFONT, command=lambda: controller.show_frame(MainPage))
        to_main.grid(row=0, column=0, padx=10, pady=10)

        to_planner = tk.Button(menu_frame, text="Planner", width=20, height=5, 
                                fg="white", bg="black",
                                font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        to_planner.grid(row=1, column=0, padx=10, pady=10)

        to_undated = tk.Button(menu_frame, text="Undated", width=20, height=5, 
                                fg="white", bg="black",
                                font=DEFAULTFONT, command=lambda: controller.show_frame(Undated))
        to_undated.grid(row=2, column=0, padx=10, pady=10)

        # Function frame that contain all the function of the page
        function_frame = tk.LabelFrame(self, bg="#2d3960", fg='white', bd=1)
        function_frame.place(relx=0.15, y=0, relwidth=0.85, relheight=1)
        function_frame.columnconfigure((0, 1, 2), weight=1)
        function_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Label frame at the top
        label = tk.Label(function_frame, text=".csv file", font=DEFAULTFONT, bg ="#2d3960", fg="white")
        label.grid(row=0, column=1, pady=10, padx=10, sticky="s")


        # Import Roadmap Button
        import_button = tk.Button(function_frame, text="Import Roadmap", width=20, height=2, fg="white", bg="black",
                                       font=DEFAULTFONT, command=self.open_file)
        import_button.grid(row=1, column=1, padx=20, pady=40, sticky="nsew")

        # Clear Roadmap Button
        clear_button = tk.Button(function_frame, text="Clear Roadmap", width=20, height=2, fg="white", bg="black",
                                      font=DEFAULTFONT)
        clear_button.grid(row=2, column=1, padx=20, pady=40, sticky="nsew")

        # View Planner Button
        planner_button = tk.Button(function_frame, text="View Planner", width=20, height=2, fg="white", bg="black",
                                        font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        planner_button.grid(row=3, column=1, padx=20, pady=40, sticky="nsew")

    # Ask for filepath and print it
    # input: None
    # output: filepath
    def open_file(self):
        filepath = filedialog.askopenfilename()
        print(filepath)
        init_database(filepath)
        read_roadmap_data()

        




# Planner page
class Planner(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Configure page grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Menu frame that contain button to go to all pages
        menu_frame = tk.LabelFrame(self, bg="#001046", fg='black', bd=1)
        menu_frame.place(x=0, y=0, relwidth=0.15, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2), weight=1)

        to_main = tk.Button(menu_frame, text="Main", width=20, height=5, fg="white", bg="black", 
                                   font=DEFAULTFONT, command=lambda: controller.show_frame(MainPage))
        to_main.grid(row=0, column=0, padx=10, pady=10)

        to_planner = tk.Button(menu_frame, text="Planner", width=20, height=5, fg="white", bg="black",
                         font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        to_planner.grid(row=1, column=0, padx=10, pady=10)

        to_undated = tk.Button(menu_frame, text="Undated", width=20, height=5, 
                                fg="white", bg="black",
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Undated))
        to_undated.grid(row=2, column=0, padx=10, pady=10)

        # Function frame that contain all the function of the page
        function_frame = tk.LabelFrame(self, bg="#2d3960", fg='white', bd=1)
        function_frame.place(relx=0.15, y=0, relwidth=0.85, relheight=1)
        function_frame.columnconfigure(0, weight=1)
        function_frame.rowconfigure((0, 1, 2, 3), weight=1)
        
        # Label of the page
        label = tk.Label(function_frame, text="Planner", font=BIGFONT, bg ="#2d3960", fg="white")
        label.grid(row=0, column=0, pady=10, padx=10)

        table = ttk.Treeview(function_frame, columns=("comp_id", "comp_name", "skill_code", "skill_name", "duration"), show="headings")
        table.column("comp_id", width=10)
        table.column("comp_name", width=100)
        table.column("skill_code", width=10)
        table.column("skill_name", width=50)
        table.column("duration", width=10)

        table.heading('comp_id', text="Competency Code")
        table.heading('comp_name', text="Competency Name")
        table.heading('skill_code', text="Skill Code")
        table.heading('skill_name', text="Skill Name")
        table.heading('duration', text="Duration")
        table.grid(row=1, column=0, sticky="nsew", padx=20)

        con = sqlite3.connect('roadmap.db')
        # Read the data from the roadmap table into a DataFrame
        df = pd.read_sql_query("SELECT * FROM roadmap", con)
        
        
        con.close()
      
        table.insert(parent='', index=0, values=("AIC-401", " Information Retrieval, Extraction, Search and Indexing "
                                                 , " AIC-401:00030", " Understand ranking algorithms"))
        
        # scroll bar
        scroll = tk.Scrollbar(function_frame, orient='vertical', command=table.yview, bg='red')
        table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=0, sticky="nse")

        main = tk.Button(function_frame, text="back", width=20, height=2,
                             font=DEFAULTFONT,
                             command=lambda: controller.show_frame(MainPage))
        main.grid(row=3, column=0, sticky="w", padx=20, pady=40)

        lastpage = tk.Button(function_frame, text="next", width=20, height=2,
                                        font=DEFAULTFONT,
                              command=lambda: controller.show_frame(Undated))
        lastpage.grid(row=3, column=0, sticky="e", padx=20, pady=40)

    def init_planner():
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()

       
# Page to show undated
class Undated(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Configure page grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Menu frame that contain button to go to all pages
        menu_frame = tk.LabelFrame(self, bg="#001046", fg='black', bd=1)
        menu_frame.place(x=0, y=0, relwidth=0.15, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2), weight=1)

        to_main = tk.Button(menu_frame, text="Main", width=20, height=5, fg="white", bg="black", 
                                   font=DEFAULTFONT, command=lambda: controller.show_frame(MainPage))
        to_main.grid(row=0, column=0, padx=10, pady=10)

        to_planner = tk.Button(menu_frame, text="Planner", width=20, height=5, fg="white", bg="black",
                         font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        to_planner.grid(row=1, column=0, padx=10, pady=10)

        to_undated = tk.Button(menu_frame, text="Undated", width=20, height=5, 
                                fg="white", bg="black",
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Undated))
        to_undated.grid(row=2, column=0, padx=10, pady=10)

        # Function frame that contain all the function of the page
        function_frame = tk.LabelFrame(self, bg="#333e61", fg='white', bd=1)
        function_frame.place(relx=0.15, y=0, relwidth=0.85, relheight=1)
        function_frame.columnconfigure(0, weight=1)
        function_frame.rowconfigure((0, 1, 2, 3), weight=1)

        # Label at the top of the page
        label = tk.Label(function_frame, text="Undated", font=BIGFONT, bg ="#333e61", fg="white")
        label.grid(row=0, column=0, pady=10, padx=10)

        # Table for data display
        table = ttk.Treeview(function_frame, columns=("comp_id", "comp_name", "skill_code", "skill_name", "duration"), show="headings")
        table.column("comp_id", width=10)
        table.column("comp_name", width=100)
        table.column("skill_code", width=10)
        table.column("skill_name", width=50)
        table.column("duration", width=10)

        table.heading('comp_id', text="Competency Code")
        table.heading('comp_name', text="Competency Name")
        table.heading('skill_code', text="Skill Code")
        table.heading('skill_name', text="Skill Name")
        table.heading('duration', text="Duration")
        table.grid(row=1, column=0, sticky="nsew", padx=20)
        table.insert(parent='', index=0, values=("AIC-401", " Information Retrieval, Extraction, Search and Indexing "
                                                 , " AIC-401:00030", " Understand ranking algorithms", "2 days"))

        # scroll bar
        scroll = tk.Scrollbar(function_frame, orient='vertical', command=table.yview, bg='red')
        table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=0, sticky="nse")


        toplanner = tk.Button(function_frame, text="back to planner", width=20, height=2,
                             font=DEFAULTFONT,
                             command=lambda: controller.show_frame(Planner))
        toplanner.grid(row=3, column=0, sticky="w", padx=20, pady=40)

        tomain = tk.Button(function_frame, text="back to main", width=20, height=2,
                                        font=DEFAULTFONT,
                              command=lambda: controller.show_frame(MainPage))
        tomain.grid(row=3, column=0, sticky="e", padx=20, pady=40)



# Run the application
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    