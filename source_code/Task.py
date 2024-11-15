# This source file is made to add, modfiy, and delete tasks
# inputs device date data, roadmap data
# Author Im and Matt
# Modified by Gold, 13 November 2024
import os
import csv
import pandas as pd
import sqlite3
from datetime import datetime

def add_task(competency_code, competency_name, skill_code, skill_name, end_date):
    try:
        # Set start date to today
        start_date = datetime.now().strftime("%Y-%m-%d")
        
        # Calculate the duration
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        duration = (end_date_obj - start_date_obj).days
        # print(duration)

        # Connect to the database
        con = sqlite3.connect('roadmap.db')
        cursor = con.cursor()

        # Insert the new task with the start date and duration
        cursor.execute(
            "INSERT INTO roadmap (competency_code, competency_name, skill_code, skill_name, duration, end_date) VALUES (?, ?, ?, ?, ?, ?)",
            (competency_code, competency_name, skill_code, skill_name, duration, end_date_obj)
        )
        con.commit()
        con.close()

        return f"New task added successfully with a duration of {duration} days."
    except Exception as e:
        return f"Error: {str(e)}"
    

        

def modify_task(skill_code, new_skill_code, new_skill_name, end_date, msg_callback=None):
    # Connect to the database
    roadmap_con = sqlite3.connect('roadmap.db')
    roadmap_cursor = roadmap_con.cursor()

    roadmap_cursor.execute("SELECT * FROM roadmap WHERE skill_code = ?", (skill_code,))
    task = roadmap_cursor.fetchone()
    if not task:
        error_msg = f"Task with skill code {skill_code} not found."
        # print(error_msg)
        if msg_callback:
            msg_callback(error_msg)
        roadmap_con.close()
        return
   
    date_format = "%Y-%m-%d"
    new_end_date = ""
    new_start_date = datetime.now()
    if end_date != "YYYY-MM-DD":
        try:
            new_end_date = datetime.strptime(end_date, date_format)
        except ValueError:
            error_msg = "Invalid date format. Please use YYYY-MM-DD."
            # print(error_msg)
            if msg_callback:
                msg_callback(error_msg)
            roadmap_con.close()
            return

    updates = []
    params = []

    if new_skill_name:
        updates.append("skill_name = ?")
        params.append(new_skill_name)

    if new_skill_code:
        updates.append("skill_code = ?")
        params.append(new_skill_code)

    # Calculate new duration
    if new_end_date:
        new_duration = (new_end_date - new_start_date).days
        updates.append("duration = ?")
        updates.append("end_date = ?")
        params.append(new_duration)
        params.append(new_end_date)
        
    if updates:
        params.append(skill_code)
        query = f"UPDATE roadmap SET {', '.join(updates)} WHERE skill_code = ?"
        # print(f"Executing query: {query}")
        # print(f"With parameters: {params}")

        try:
            roadmap_cursor.execute(query, params)
            roadmap_con.commit()
            success_msg = f"Task with skill code {skill_code} has been successfully modified."
            # print(success_msg)
            if msg_callback:
                msg_callback(success_msg)
        except sqlite3.Error as e:
            error_msg = f"An error occurred: {e}"
            # print(error_msg)
            if msg_callback:
                msg_callback(error_msg)
    else:
        no_update_msg = "No updates to apply."
        # print(no_update_msg)
        if msg_callback:
            msg_callback(no_update_msg)

    roadmap_con.close()

def delete_task(skill_code):

    try:
        roadmap_con = sqlite3.connect('roadmap.db')
        roadmap_cursor = roadmap_con.cursor()
        
        # Execute the delete operation
        roadmap_cursor.execute("DELETE FROM roadmap WHERE skill_code = ?", (skill_code,))
        
        # Check if the row was deleted
        if roadmap_cursor.rowcount == 0:
            roadmap_con.commit()
            roadmap_con.close()
            return f"No task with skill code {skill_code} found."
        else:
            roadmap_con.commit()
            roadmap_con.close()
            return f"Task with skill code {skill_code} has been successfully deleted."
            
        
    except sqlite3.Error as e:
        roadmap_con.commit()
        roadmap_con.close()
        return f"An error occurred: {e}"
        

def mark_finish(skill_code):
    con_roadmap = sqlite3.connect('roadmap.db')
    cursor_roadmap = con_roadmap.cursor()
    
    # Connect to the task database
    con_task = sqlite3.connect('task.db')
    cursor_task = con_task.cursor()

    con_task.execute('''
    CREATE TABLE IF NOT EXISTS task (
        competency_code TEXT,
        competency_name TEXT,
        skill_code TEXT,
        skill_name TEXT,
        duration TEXT,
        end_date TEST
    )
    ''')
    
    # Retrieve the row to delete from roadmap
    cursor_roadmap.execute("SELECT * FROM roadmap WHERE skill_code = ?", (skill_code,))
    row = cursor_roadmap.fetchone()
    
    if row:
        # Insert the row into task database
        cursor_task.execute("""
            INSERT INTO task (competency_code, competency_name, skill_code, skill_name, duration, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, row)
        
        # Delete the row from roadmap
        cursor_roadmap.execute("DELETE FROM roadmap WHERE skill_code = ?", (skill_code,))
        
        # Commit both transactions
        con_roadmap.commit()
        con_task.commit()
    
    # Close connections
    con_roadmap.close()
    con_task.close()

        
    


    
    
    
    