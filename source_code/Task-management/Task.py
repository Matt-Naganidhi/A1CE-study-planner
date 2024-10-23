#This source file is made to add, modfiy, and delete tasks
#inputs device date data, roadmap data
#Author Im and Matt
import os
import csv
import pandas as pd 

def Task_info (roadmap_information, current_device_date, user_input_array):
    #task name
    #task duration
    task_duration = user_input_array[end_date] - current_device_date
    #task description


def modify_task():
    #connect to the database
    con = sqlite3.connect('roadmap.db')
    cursor = con.cursor()

    #get input to modify
    task_id, new_competency_name, new_skill_code, new_skill_name = user_input()

    #check if competency exists in the database
    cursor.execute("SELECT * FROM roadmap WHERE competency_code = ?", (task_id,))
    row = cursor.fetchone()
    
    if row is None:
        #print error and exit if not found
        print(f"Task with competency_code {task_id} not found.")
        con.close()
        return

    #modify the details and update only on provided input.
    if new_competency_name:
        cursor.execute("UPDATE roadmap SET competency_name = ? WHERE competency_code = ?", 
                       (new_competency_name, task_id))
    if new_skill_code:
        cursor.execute("UPDATE roadmap SET skill_code = ? WHERE competency_code = ?", 
                       (new_skill_code, task_id))
    if new_skill_name:
        cursor.execute("UPDATE roadmap SET skill_name = ? WHERE competency_code = ?", 
                       (new_skill_name, task_id))

    con.commit()

    #print a message to comfirm the updated task
    print(f"Task with competency_code {task_id} has been successfully modified.")

    # Close the database connection
    con.close()
#get task id, new competency name, skill code, skill name
def user_input():
    task_id = input("Enter the Task ID you want to modify (competency_code): ") 
    new_competency_name = input("Enter new competency name (leave blank to keep unchanged): ")  
    new_skill_code = input("Enter new skill code (leave blank to keep unchanged): ") 
    new_skill_name = input("Enter new skill name (leave blank to keep unchanged): ") 
    
    #return the user inputs as a tuple
    return task_id, new_competency_name, new_skill_code, new_skill_name
    
    
    
