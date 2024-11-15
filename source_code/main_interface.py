# This source file is made to be the interface Ui that
# the user will interact with. At the moment there are
# 3 pages, main page to import roadmap file
# and go to other pages, planner page where user can
# look/modify task, and last page that tell the user
# undated task.
# input: none
# output: none

# Created by Gold, 20 October 2024
# Modified by Gold, 13 November 2024

import tkinter as tk  # graphic library for GUI
import sqlite3
import pandas as pd
from tkinter import ttk  # extra function from the graphic library
from tkinter import filedialog, messagebox  # for importing file
from datetime import datetime

from database import*
from Task import*


DEFAULTFONT = ("Helvetica", 12, "bold")  # define default font
BIGFONT = ("Helvetica", 24, "bold")  # define big font


# Main application class that handles page switching
class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window geometry to 1000x800
        self.geometry("1400x800")
        self.minsize(1400, 800)
        self.title("A1CE Study Planner")

        # Container to hold all pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Dictionary to store pages
        self.pages = {}

        # Initialize pages
        for Page in (MainPage, Planner, Undated, Finished):
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
            # print("Saving files")
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
        menu_frame.rowconfigure((0, 1, 2, 3), weight=1)

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

        to_finish = tk.Button(menu_frame, text="Completed", width=20, height=5, 
                                fg="white", bg="black",
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Finished))
        to_finish.grid(row=3, column=0, padx=10, pady=10)

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
        clear_button = tk.Button(function_frame, text="Clear Roadmap", command = self.delete_roadmap,
                                 width=20, height=2, fg="white", bg="black",
                                      font=DEFAULTFONT)
        clear_button.grid(row=2, column=1, padx=20, pady=40, sticky="nsew")

        # View Planner Button
        # add initiate table function to this button
        planner_button = tk.Button(function_frame, text="View Planner", width=20, height=2, fg="white", bg="black",
                                        font=DEFAULTFONT, command=lambda: controller.show_frame(Planner))
        planner_button.grid(row=3, column=1, padx=20, pady=40, sticky="nsew")

    def delete_roadmap(self):
        message = messagebox.askokcancel("Confirm", "Do you really want to clear your roadmap?")
        if message == True:
            clear_roadmap()
            messagebox.showinfo("Success", "Deleted Roadmap")
    
    # Ask for filepath and print it
    # input: None
    # output: filepath
    def open_file(self):
        filepath = filedialog.askopenfilename()
        # print(filepath)
        check = init_database(filepath)
        # print(check)
        if not check:
            # print("Roadmap file already exist")
            messagebox.showinfo("Failed", "Roadmap file already exist")
        else:
            messagebox.showinfo("Success", "Go to planner to look/edit roadmap")

    
    

        
# Planner page
class Planner(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.edit_window = None
        self.add_task_popup = None

        # Configure page grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        menu_frame = tk.LabelFrame(self, bg="#001046", fg='black', bd=1)
        menu_frame.place(x=0, y=0, relwidth=0.15, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2, 3), weight=1)

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

        to_finish = tk.Button(menu_frame, text="Completed", width=20, height=5, 
                                fg="white", bg="black",
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Finished))
        to_finish.grid(row=3, column=0, padx=10, pady=10)

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
 

        reset_table = tk.Button(function_frame, text="Reload Table", width=20, height=2,
                             font=DEFAULTFONT,
                             command=lambda: self.init_planner(table))
        reset_table.grid(row=3, column=0, sticky="w", padx=20, pady=40)


        add_task = tk.Button(function_frame, text="Add Task", width=20, height=2,
                                        font=DEFAULTFONT,
                              command= self.add_taskpopup)
        add_task.grid(row=3, column=0, sticky="e", padx=20, pady=40)

    # Link with reset table to initiate/reset the table
    def init_planner(self, table):
        # Connect to the SQLite database and fetch data
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()

        # Get the current date
        current_date = datetime.now().date()
    
    # Update duration based on the difference between end_date and the current date
        cursor.execute("SELECT skill_code, end_date FROM roadmap")
        rows = cursor.fetchall()
    
        for skill_code, end_date in rows:
            if end_date:
            # Parse the end_date and calculate the difference
                end_date_obj = datetime.strptime(end_date.split()[0], "%Y-%m-%d").date()
                duration = (end_date_obj - current_date).days
                cursor.execute("UPDATE roadmap SET duration = ? WHERE skill_code = ?", (duration, skill_code))
    
    # Commit the updates to the database
        con.commit()
        
        # Query the data from roadmap table
        cursor.execute("""
        SELECT competency_code, competency_name, skill_code, skill_name, duration
        FROM roadmap
        ORDER BY duration IS NULL, CAST(duration AS INTEGER) ASC
        """)
        rows = cursor.fetchall()
        
        # Clear the current data in the table
        for item in table.get_children():
            table.delete(item)
        
        # Insert each row of data into the table
        # for row in rows:
        #     table.insert('', 'end', values=row)

        for row in rows:
        # Append "days" to the duration if it is not None
            formatted_row = row[:-1] + (f"{row[-1]} days" if row[-1] is not None else "",)
            table.insert('', 'end', values=formatted_row)
        
        con.close()

    
    # Pop up for adding new task
    def add_taskpopup(self):
        if self.add_task_popup is not None and self.add_task_popup.winfo_exists():
            self.add_task_popup.lift()  # Bring the existing window to the front
            return
        
        self.add_task_popup = tk.Toplevel(self)
        self.add_task_popup.wm_title("Add New Task")
        
        # Allow for selecting or entering a competency code
        tk.Label(self.add_task_popup, text="Select Existing or Enter New Competency Code", font=DEFAULTFONT).pack(pady=10)

        # Fetch competencies from the database
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()
        cursor.execute("SELECT DISTINCT competency_code, competency_name FROM roadmap")
        competencies = cursor.fetchall()
        con.close()
        
        # Dropdown for existing competencies
        selected_competency = tk.StringVar()
        competency_menu = tk.OptionMenu(self.add_task_popup, selected_competency, *[f"{comp[0]}: {comp[1]}" for comp in competencies])
        competency_menu.pack(pady=5)

        # New competency code and name entries
        tk.Label(self.add_task_popup, text="Or Enter New Competency Code", font=DEFAULTFONT).pack(pady=5)
        new_competency_code_entry = tk.Entry(self.add_task_popup, width=30)
        new_competency_code_entry.pack()

        tk.Label(self.add_task_popup, text="Enter New Competency Name", font=DEFAULTFONT).pack(pady=5)
        new_competency_name_entry = tk.Entry(self.add_task_popup, width=30)
        new_competency_name_entry.pack()

        # Skill name entry
        tk.Label(self.add_task_popup, text="Skill Code", font=DEFAULTFONT).pack(pady=5)
        skill_code_entry = tk.Entry(self.add_task_popup, width=30)
        skill_code_entry.pack()

        # Skill name entry
        tk.Label(self.add_task_popup, text="Skill Name", font=DEFAULTFONT).pack(pady=5)
        skill_name_entry = tk.Entry(self.add_task_popup, width=30)
        skill_name_entry.pack()

        # End date entry
        tk.Label(self.add_task_popup, text="End Date (YYYY-MM-DD)", font=DEFAULTFONT).pack(pady=5)
        end_date_entry = tk.Entry(self.add_task_popup, width=30)
        end_date_entry.pack()

        # Save button
        save_button = tk.Button(self.add_task_popup, text="Save", width=20,
                                command=lambda: self.save_new_task(selected_competency.get(), 
                                                                   new_competency_code_entry.get(),
                                                                   new_competency_name_entry.get(),
                                                                   skill_code_entry.get(),
                                                                   skill_name_entry.get(), 
                                                                   end_date_entry.get(), 
                                                                   self.add_task_popup))
        save_button.pack(pady=20)


    # Save info enter and save as new task
    def save_new_task(self, selected_competency, new_competency_code, new_competency_name, skill_name, skill_code, end_date, popup):
        # Determine which competency code and name to use
        if new_competency_code and new_competency_name:
            competency_code = new_competency_code
            competency_name = new_competency_name
        elif selected_competency:
            competency_code, competency_name = selected_competency.split(": ")
        else:
            self.msg("Please select or enter a competency code and name.")
            return

        # Call add_task function from task_manager.py
        message = add_task(competency_code, competency_name, skill_name, skill_code, end_date)
        
        # Close popup and refresh the table
        popup.destroy()
        # self.init_planner(self.table)  # Refresh the table with updated data
        messagebox.showinfo("Message", message)
        # self.msg(message)  # Display message to user

    
    # Edit page on double click
    def on_row_click(self, table):
        # Get the item that was clicked
        selected_item = table.selection()
        if selected_item:
        # Fetch the values of the selected row
            row_values = table.item(selected_item, "values")
            com_code, com_name, skill_code, skill_name, duration = row_values
     
        # print(com_code, com_name, skill_code, skill_name, duration)
        self.open_edit_page(com_code, com_name, skill_code, skill_name)  

    # To-do
    # Pop up for Edit page
    # Pop up for Edit page
    def open_edit_page(self, com_code, com_name, skill_code, skill_name):
        if self.edit_window is not None and self.edit_window.winfo_exists():
            self.edit_window.lift()  # Bring the existing window to the front
            return
        
        self.edit_window = tk.Toplevel(self)
        self.edit_window.title("Edit Page")

        # Bind the close event to set self.edit_window to None when closed
        self.edit_window.protocol("WM_DELETE_WINDOW", self.on_edit_close)

        self.edit_window.after(1, lambda: self.edit_window.focus_force())
    
        # Label indicating the editing section
        label = tk.Label(self.edit_window, text=f"Editing:  {com_code} : {com_name}", font=DEFAULTFONT)
        label.pack(pady=10, padx=80)
        


        # Skill code entry
        label2 = tk.Label(self.edit_window, text="Editing Skill Code", font=DEFAULTFONT).pack(padx=10)
        entry3 = tk.Entry(self.edit_window, width=40)
        entry3.insert(0, skill_code) 
        entry3.pack(pady=5)

        # Skill name entry
        label3 = tk.Label(self.edit_window, text="Editing Skill Name", font=DEFAULTFONT).pack(padx=10)
        entry4 = tk.Entry(self.edit_window, width=40)
        entry4.insert(0, skill_name)
        entry4.pack(pady=5)

        # End date entry
        label4 = tk.Label(self.edit_window, text="Editing End Date (YYYY-MM-DD)", font=DEFAULTFONT).pack(padx=10)

        label5 = tk.Label(self.edit_window, text="Leave it alone if you are not editing the date").pack(padx=10)

        entry5 = tk.Entry(self.edit_window, width=40)
        entry5.insert(0, "YYYY-MM-DD")
        entry5.pack(pady=5)

        # Buttons
        def show_save_message(message):
            # messagebox.showinfo("Message", message)
            self.edit_save(message)
            self.edit_window.destroy()

        def show_delete_message(skill_id):
            check = messagebox.askokcancel("Confirm Delete", f"Are you sure you want to delete task: {skill_id}")
            if check == True:
                message = delete_task(skill_id)
                messagebox.showinfo("Message",message)

            # self.delete_msg(skill_id)
            self.edit_window.destroy()

        def show_mark_message(skill_id):
            check = messagebox.askokcancel("Confirm", f"Are you sure you want to mark: {skill_id} as finsihed")
            if check == True:
                mark_finish(skill_id)
            self.edit_window.destroy()

            # self.mark_finish(skill_id)
            # self.edit_window.destroy()

        save_button = tk.Button(self.edit_window, text="Save", width=30, font=DEFAULTFONT,
                                command=lambda: modify_task(skill_code, entry3.get(), entry4.get(), entry5.get(), show_save_message))
        save_button.pack(side="right", padx=10, pady=20)

        finish_button = tk.Button(self.edit_window, text="Mark as Finished", width=30, bg="light yellow", font=DEFAULTFONT, command = lambda: show_mark_message(skill_code)
                                )
        finish_button.pack(side="right", padx=10, pady=20)

        

        cancel_button = tk.Button(self.edit_window, text="Cancel", width=30, font=DEFAULTFONT, command=self.edit_window.destroy)
        cancel_button.pack(side="left", padx=10, pady=20)

        delete_button = tk.Button(self.edit_window, text="Delete Task", width=20, bg="red", fg="white", font=DEFAULTFONT, 
                                  command=lambda: show_delete_message(skill_code))
        delete_button.pack(side="left", pady=20)

    def on_edit_close(self):
        """Callback to reset edit_window attribute when window is closed."""
        self.edit_window.destroy()
        self.edit_window = None

    def edit_save(self, message):
        popup = tk.Toplevel(self)
        popup.wm_title("Message")
        popup.after(1, lambda: popup.focus_force())

        label = tk.Label(popup, text=message, font=DEFAULTFONT)
        label.pack(pady=10)

        ok_button = ttk.Button(popup, text="Okay", command=popup.destroy)
        ok_button.pack(pady=10)

    # def delete_msg(self, skill_code):
    #     popup = tk.Toplevel(self)
    #     popup.wm_title("Message")
    #     popup.after(1, lambda: popup.focus_force())

    #     label = tk.Label(popup, text="Are you sure you want to delete this task?", font=DEFAULTFONT)
    #     label.pack(pady=10)

    #     no_button = ttk.Button(popup, text="Cancel", command=popup.destroy)
    #     no_button.pack(pady=10, padx=10, side="left")

    #     yes_button = ttk.Button(popup, text="Confirm", command=lambda: [delete_task(skill_code), popup.destroy()])
    #     yes_button.pack(pady=10,padx=10, side="right")


    
# Page to show undated
class Undated(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.bulk_entry_window = None

        # Configure page grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Menu frame that contain button to go to all pages
        menu_frame = tk.LabelFrame(self, bg="#001046", fg='black', bd=1)
        menu_frame.place(x=0, y=0, relwidth=0.15, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2, 3), weight=1)

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

        to_finish = tk.Button(menu_frame, text="Completed", width=20, height=5, 
                                fg="white", bg="black",
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Finished))
        to_finish.grid(row=3, column=0, padx=10, pady=10)

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

        # scroll bar
        scroll = tk.Scrollbar(function_frame, orient='vertical', command=table.yview, bg='red')
        table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=0, sticky="nse")


        toplanner = tk.Button(function_frame, text="Reload Table", width=20, height=2,
                             font=DEFAULTFONT,
                             command=lambda: self.init_planner(table))
        toplanner.grid(row=3, column=0, sticky="w", padx=20, pady=40)

        tomain = tk.Button(function_frame, text="Add A lot of Date", width=20, height=2,
                                        font=DEFAULTFONT,
                              command= self.open_bulk_date_entry)
        tomain.grid(row=3, column=0, sticky="e", padx=20, pady=40)


    # Link with reset table to initiate/reset the table
    def init_planner(self, table):
    # Connect to the SQLite database and fetch data
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()
    
    # Query to get rows where duration is either NULL or an empty string
        cursor.execute("""
        SELECT competency_code, competency_name, skill_code, skill_name, duration
        FROM roadmap
        WHERE duration IS NULL OR duration = ''
    """)
        rows = cursor.fetchall()
    
    # Clear the current data in the table
        for item in table.get_children():
            table.delete(item)
    
    # Insert each row of data with empty duration into the table
        for row in rows:
            table.insert('', 'end', values=row)
    
        con.close()


    def open_bulk_date_entry(self):

        if self.bulk_entry_window is not None and tk.Toplevel.winfo_exists(self.bulk_entry_window):
            self.bulk_entry_window.lift()  # Bring the existing window to the front
            return
        
        # Create a new Toplevel window and store it in self.bulk_entry_window
        self.bulk_entry_window = tk.Toplevel(self)
        self.bulk_entry_window.title("Bulk Date Entry")
        self.bulk_entry_window.geometry('1500x400')


        # Bind the close event to set self.bulk_entry_window to None when closed
        self.bulk_entry_window.protocol("WM_DELETE_WINDOW", self.on_bulk_entry_close)


    # Create a canvas and scrollbar for scrollable content
        canvas = tk.Canvas(self.bulk_entry_window, width=500, height=400)
        scrollbar = tk.Scrollbar(self.bulk_entry_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

    # Configure the canvas and scrollbar
        scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # Fetch undated tasks from the database
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()
        cursor.execute("""
        SELECT competency_code, competency_name, skill_code, skill_name
        FROM roadmap
        WHERE duration IS NULL OR duration = ''
    """)
        tasks = cursor.fetchall()
        con.close()

    # Store entries for saving
        self.task_entries = []

        

    # Populate the scrollable frame with task labels and entry fields
        for idx, (competency_code, competency_name, skill_code, skill_name) in enumerate(tasks):
        # Task description label
            
            tk.Label(scrollable_frame, text=f"{competency_code} - {competency_name} - {skill_code} - {skill_name}").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        
        # Duration entry field
            duration_entry = tk.Entry(scrollable_frame)
            duration_entry.grid(row=idx, column=1, padx=10, pady=5)
            duration_entry.insert(0, "YYYY-MM-DD")
            self.task_entries.append((skill_code, duration_entry))

    # Save button at the end of the scrollable frame
        save_button = tk.Button(scrollable_frame, text="Save Dates", font=DEFAULTFONT, bg="red", fg="white", command= lambda: self.save_bulk_dates(self.bulk_entry_window))
        save_button.grid(row=len(tasks), column=0, columnspan=2, pady=10)  # Span both columns
        
    def on_bulk_entry_close(self):
        """Callback to reset bulk_entry_window attribute when window is closed."""
        self.bulk_entry_window.destroy()
        self.bulk_entry_window = None

    def save_bulk_dates(self, bulk_entry_window):
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()

    # Update each task with the entered duration
        for skill_code, duration_entry in self.task_entries:
            new_end_date = duration_entry.get()
            if duration_entry.get() != "YYYY-MM-DD":  # Only update if a duration is entered
                end_date_obj = datetime.strptime(new_end_date, "%Y-%m-%d")
                start_date = datetime.now().strftime("%Y-%m-%d")
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                new_duration = (end_date_obj - start_date_obj).days

            
                cursor.execute("UPDATE roadmap SET duration = ?, end_date = ? WHERE skill_code = ?", (new_duration, end_date_obj, skill_code))
    
        con.commit()
        con.close()

    # Confirmation message
        response = messagebox.showinfo("Success", "Dates saved successfully!")
        if response:
            bulk_entry_window.destroy()

class Finished(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Configure page grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Menu frame that contain button to go to all pages
        menu_frame = tk.LabelFrame(self, bg="#001046", fg='black', bd=1)
        menu_frame.place(x=0, y=0, relwidth=0.15, relheight=1)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure((0, 1, 2, 3), weight=1)

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

        to_finish = tk.Button(menu_frame, text="Completed", width=20, height=5, 
                                fg="white", bg="black",
                               font=DEFAULTFONT, command=lambda: controller.show_frame(Finished))
        to_finish.grid(row=3, column=0, padx=10, pady=10)

        # Function frame that contain all the function of the page
        function_frame = tk.LabelFrame(self, bg="#6fa7b0", fg='white', bd=1)
        function_frame.place(relx=0.15, y=0, relwidth=0.85, relheight=1)
        function_frame.columnconfigure(0, weight=1)
        function_frame.rowconfigure((0, 1, 2, 3), weight=1)
        
        # Label of the page
        label = tk.Label(function_frame, text="Finished", font=BIGFONT, bg ="#6fa7b0", fg="white")
        label.grid(row=0, column=0, pady=10, padx=10)

        table = ttk.Treeview(function_frame, columns=("comp_id", "comp_name", "skill_code", "skill_name"), show="headings")
        table.column("comp_id", width=10)
        table.column("comp_name", width=100)
        table.column("skill_code", width=10)
        table.column("skill_name", width=50)

        table.heading('comp_id', text="Competency Code")
        table.heading('comp_name', text="Competency Name")
        table.heading('skill_code', text="Skill Code")
        table.heading('skill_name', text="Skill Name")
        table.grid(row=1, column=0, sticky="nsew", padx=20)


        # scroll bar
        scroll = tk.Scrollbar(function_frame, orient='vertical', command=table.yview, bg='red')
        table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=0, sticky="nse")
 

        reset_table = tk.Button(function_frame, text="Reload Table", width=20, height=2,
                             font=DEFAULTFONT,
                             command=lambda: self.init_planner(table))
        reset_table.grid(row=3, column=0, sticky="w", padx=20, pady=40)



    # Link with reset table to initiate/reset the table
    def init_planner(self, table):
        # Connect to the SQLite database and fetch data
        con = sqlite3.connect('task.db')
        cursor = con.cursor()

        
        # Query the data from roadmap table
        cursor.execute("""
        SELECT competency_code, competency_name, skill_code, skill_name
        FROM task""")
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
    