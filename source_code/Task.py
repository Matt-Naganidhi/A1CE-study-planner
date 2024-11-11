# This source file is made to add, modfiy, and delete tasks
# inputs device date data, roadmap data
# Author Im and Matt
# Modified by Gold, 10 November 2024
import os
import csv
import pandas as pd
import sqlite3
from datetime import datetime

def add_task():
    roadmap_con = sqlite3.connect('roadmap.db')
    roadmap_cursor = roadmap_con.cursor()

    roadmap_cursor.execute("PRAGMA table_info(roadmap)")
    columns = [info[1] for info in roadmap_cursor.fetchall()]
    if 'duration' not in columns:
        roadmap_cursor.execute("ALTER TABLE roadmap ADD COLUMN duration INTEGER")

    roadmap_cursor.execute("SELECT DISTINCT competency_code, competency_name FROM roadmap")
    competencies = roadmap_cursor.fetchall()
    print("Available competencies:")
    for comp_code, comp_name in competencies:
        print(f"{comp_code}: {comp_name}")

    selected_competency  = input("Enter the competency code for the new task: ")
    roadmap_cursor.execute("SELECT competency_code, competency_name FROM roadmap WHERE competency_code = ?", (selected_competency,))
    competency = roadmap_cursor.fetchone()

    if not competency:
        print(f"No competency found with code {selected_competency}.")
        roadmap_con.close()
        return
    
    skill_name = input("Enter skill name for the task: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    #calculate task duration
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-  %d")
    task_duration = (end_date_obj - start_date_obj).days

    roadmap_cursor.execute(
        "INSERT INTO roadmap (competency_code, competency_name, skill_name, start_date, end_date, duration) VALUES (?, ?, ?, ?, ?, ?)",
        (competency[0], competency[1], skill_name, start_date, end_date, task_duration)
    )
    roadmap_con.commit()
    print("New task has been added to roadmap.db with a duration of", task_duration, "days.")

    roadmap_con.close()
        

def modify_task(skill_code, new_skill_name, end_date):
    #connect to the database
    roadmap_con = sqlite3.connect('roadmap.db')
    roadmap_cursor = roadmap_con.cursor()

    roadmap_cursor.execute("SELECT * FROM roadmap WHERE skill_code = ?", (skill_code,))
    task = roadmap_cursor.fetchone()
    if not task:
        print(f"Task with skill code {skill_code} not found.")
        roadmap_con.close()
        return
   

    date_format = "%Y-%m-%d"

    new_start_date = datetime.now()
    new_end_date = datetime.strptime(end_date, date_format)

    updates = []
    params = []

    if new_skill_name:
        updates.append("skill_name = ?")
        params.append(new_skill_name)


        #calculate new duration if both dates are updated
    if new_end_date:
    
        new_duration = (new_end_date - new_start_date).days
        print(new_duration)
        updates.append("duration = ?")
        params.append(new_duration)
        
    
    if updates:
        params.append(skill_code)
        query = f"UPDATE roadmap SET {', '.join(updates)} WHERE skill_code = ?"
        print(f"Executing query: {query}")
        print(f"With parameters: {params}")

        try:
            roadmap_cursor.execute(query, params)
            roadmap_con.commit()
            print(f"Task with skill code {skill_code} has been successfully modified.")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    else:
        print("No updates to apply.")

def delete_task():
    roadmap_con = sqlite3.connect('roadmap.db')
    roadmap_cursor = roadmap_con.cursor()

    #get skill code
    skill_code = input("Enter the skill code you want to delete:")

    #check and confirm deletion
    roadmap_cursor.execute("SELECT * FROM tasks WHERE skill_code = ?", skill_code,)
    task = roadmap_cursor.fetchone()

    if not task:
        print(f"Task with skill code {skill_code} not found.")
        roadmap_con.close()
        return
    
    confirm = input(f"Are you sure you want to delete the task with skill_code {skill_code}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Deletion canceled.")
        roadmap_con.close()
        return

    #delete task
    roadmap_cursor.execute("DELETE FROM roadmap WHERE skill_code = ?", (skill_code,))
    roadmap_con.commit()

    print(f"Task with skill code {skill_code} has been successfully deleted.")

    roadmap_con.close()
    