# This source file is made to be the interface Ui that
# the user will interact with. At the moment there are
# 3 pages, main page to import roadmap file
# and go to other pages, planner page where user can
# look/modify task, and last page that tell the user
# undated task.
# input: none
# output: none

# Created by Gold, 20 October 2024
# Modified by Gold, 8 November 2024

import tkinter as tk  # graphic library for GUI
import sqlite3
import pandas as pd
from tkinter import ttk  # extra function from the graphic library
from tkinter import filedialog, messagebox  # for importing file

from database import *
from Task import *


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
        check = init_database(filepath)
        if not check:
            print("Roadmap file already exist")
            self.fail_msg()
        else:
            self.success_msg()

    def success_msg(self):
        popup = tk.Toplevel(self)  # Use Toplevel to create a popup window
        popup.wm_title("Message")
        popup.after(1, lambda: popup.focus_force())
        
        label = tk.Label(popup, text="Open file successfully!", font=DEFAULTFONT)
        label.pack(pady=10)
        label2 = tk.Label(popup, text="Go to planner to look at your tasks!", font=DEFAULTFONT)
        label2.pack(pady=10)
        
        ok_button = ttk.Button(popup, text="Okay", command=popup.destroy)
        ok_button.pack(pady=10)

    def fail_msg(self):
        popup = tk.Toplevel(self)  # Use Toplevel to create a popup window
        popup.wm_title("Message")
        popup.after(1, lambda: popup.focus_force())

        
        label = tk.Label(popup, text="Roadmap file alredy initiated!", font=DEFAULTFONT)
        label.pack(pady=10)
        
        ok_button = ttk.Button(popup, text="Okay", command=popup.destroy)
        ok_button.pack(pady=10)
    
    

        
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


        table.bind("<Double-1>", lambda event: self.on_row_click(table))

        # scroll bar
        scroll = tk.Scrollbar(function_frame, orient='vertical', command=table.yview, bg='red')
        table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=0, sticky="nse")
 

        main = tk.Button(function_frame, text="Reset Table", width=20, height=2,
                             font=DEFAULTFONT,
                             command=lambda: self.init_planner(table))
        main.grid(row=3, column=0, sticky="w", padx=20, pady=40)

        lastpage = tk.Button(function_frame, text="next", width=20, height=2,
                                        font=DEFAULTFONT,
                              command=lambda: self.popupmsg())
        lastpage.grid(row=3, column=0, sticky="e", padx=20, pady=40)

    def init_planner(self, table):
        # Connect to the SQLite database and fetch data
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()
        print("hello")
        # Query the data from roadmap table
        cursor.execute("""SELECT competency_code, competency_name, skill_code, skill_name, duration 
                       FROM roadmap
                       WHERE duration is NOT NULL """)
        rows = cursor.fetchall()
        
        # Clear the current data in the table
        for item in table.get_children():
            table.delete(item)
        
        # Insert each row of data into the table
        for row in rows:
            table.insert('', 'end', values=row)
        
        con.close()

    def on_row_click(self, table):
        # Get the item that was clicked
        selected_item = table.selection()
        if selected_item:
        # Fetch the values of the selected row
            row_values = table.item(selected_item, "values")
            com_code, com_name, skill_code, skill_name, duration = row_values
            # com_code = row_values[0].strip()
            # com_name = row_values[1].strip()
            # skill_code = row_values[2].strip()
            # skill_name = row_values[3].strip()
            # duration = row_values[4].strip()
     
        print(com_code, com_name, skill_code, skill_name, duration)
        self.popupmsg(com_code, com_name, skill_code, skill_name)    

    def popupmsg(self, com_code, com_name, skill_code, skill_name):
        popup = tk.Tk()
        popup.wm_title("Edit Page")
        popup.after(1, lambda: popup.focus_force())
    
        # Label indicating the editing section
        label = tk.Label(popup, text=f"Editing:  {com_code} : {com_name}" , font=DEFAULTFONT)
        label.pack(pady=10, padx =80)

        # Entry fields for each value with initial text set to existing values
        # entry1 = tk.Entry(popup, width=40)
        # entry1.insert(0, com_code)  # Insert initial value for Competency Code
        # entry1.pack(pady=5)
        label1 = tk.Label(popup, text=f"{skill_code}")
        label1.pack(pady=10, padx =80)

        # entry2 = tk.Entry(popup, width=40)
        # entry2.insert(0, com_name)
        # entry2.pack(pady=5)

        entry3 = tk.Entry(popup, width=40)
        entry3.insert(0, skill_code) 
        entry3.pack(pady=5)

        entry4 = tk.Entry(popup, width=40)
        entry4.insert(0, skill_name)
        entry4.pack(pady=5)

        label3 = tk.Label(popup, text="Editing End Date(YYYY-MM-DD)")
        label3.pack(pady=10, padx =10)

        entry5 = tk.Entry(popup, width=40)
        entry5.insert(0, "YYYY-MM-DD")
        entry5.pack(pady=5)

    # Buttons
        save_button = tk.Button(popup, text="Save", width=30, command =lambda: modify_task(skill_code, entry4.get(), entry5.get()))
        save_button.pack(side="right", padx=10, pady=20)

        cancel_button = tk.Button(popup, text="Cancel", width=30, command=popup.destroy)
        cancel_button.pack(side="left", padx=10, pady=20)

        popup.mainloop()

       
# Page to show undated
class Undated(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Configure page grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Menu frame containing buttons to navigate
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
                               fg="white", bg="black", font=DEFAULTFONT, command=lambda: controller.show_frame(Undated))
        to_undated.grid(row=2, column=0, padx=10, pady=10)
        
        # Function frame that contains all the functionalities
        function_frame = tk.LabelFrame(self, bg="#333e61", fg='white', bd=1)
        function_frame.place(relx=0.15, y=0, relwidth=0.85, relheight=1)
        function_frame.columnconfigure(0, weight=1)
        function_frame.rowconfigure((0, 1, 2, 3), weight=1)

        # Label at the top of the page
        label = tk.Label(function_frame, text="Undated", font=BIGFONT, bg="#333e61", fg="white")
        label.grid(row=0, column=0, pady=10, padx=10)

        # Table for data display
        self.table = ttk.Treeview(function_frame, columns=("comp_id", "comp_name", "skill_code", "skill_name", "duration"), show="headings")
        self.table.column("comp_id", width=10)
        self.table.column("comp_name", width=100)
        self.table.column("skill_code", width=10)
        self.table.column("skill_name", width=50)
        self.table.column("duration", width=10)

        self.table.heading('comp_id', text="Competency Code")
        self.table.heading('comp_name', text="Competency Name")
        self.table.heading('skill_code', text="Skill Code")
        self.table.heading('skill_name', text="Skill Name")
        self.table.heading('duration', text="Duration")
        self.table.grid(row=1, column=0, sticky="nsew", padx=20)

        # Scroll bar
        scroll = tk.Scrollbar(function_frame, orient='vertical', command=self.table.yview, bg='red')
        self.table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=0, sticky="nse")

        toplanner = tk.Button(function_frame, text="Back to planner", width=20, height=2,
                              font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        toplanner.grid(row=3, column=0, sticky="w", padx=20, pady=40)

        tomain = tk.Button(function_frame, text="Back to main", width=20, height=2,
                           font=DEFAULTFONT, command=lambda: self.init_planner(self.table))
        tomain.grid(row=3, column=0, sticky="e", padx=20, pady=40)

    def init_planner(self, table):
        # Connect to the SQLite database and fetch data
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()
        
        # Query the data from roadmap table where duration is NULL or empty
        cursor.execute("""
            SELECT competency_code, competency_name, skill_code, skill_name, duration 
            FROM roadmap
            WHERE duration IS NULL
        """)
        rows = cursor.fetchall()
        
        # Clear the current data in the table
        for item in table.get_children():
            table.delete(item)
        
        # Insert each row of data into the table
        for row in rows:
            table.insert('', 'end', values=row)
        
        con.close()
    


# Run the application
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    