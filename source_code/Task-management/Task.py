#This source file is made to add, modfiy, and delete tasks
#inputs device date data, roadmap data
#Author Im and Matt
import os
import csv
import pandas as pd 


def task_info (roadmap_information, current_device_date, user_input_array):
    # Navigate to the specified directory and read from 'output.csv'
    os.chdir('../data-management')
    input_path = 'output.csv'
    output_path = 'roadmap_task.csv'
    # Read input CSV and save task data to a list
    roadmap_tasks = []
    with open(input_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            task = {
                'task_id': row['competency_code'],
                'competency_name': row['title'],
                'skill_code': row['assessed_skill_code'],
                'skill_name': row['title'],
                'start_date': None,   # Placeholder if dates need to be added
                'end_date': None
            }
            roadmap_tasks.append(task)

    # Write to roadmap_task.csv in the current directory
    with open(output_path, mode='w', newline='') as file:
        fieldnames = ['task_id', 'competency_name', 'skill_code', 'skill_name', 
                      'start_date', 'end_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for task in roadmap_tasks:
            writer.writerow(task)
    print(f"Data from {input_path} has been written to {output_path}.")
    
    #task name
    #task duration
    end_date = datetime.strptime(user_input_array.get('end_date'), "%Y-%m%d")
    start_date = datetime.strptime(current_device_date, "%Y-%m%d")
    task_duration = (end_date - start_date).days
    #task description

    with open(output_path, mode='w', newline='') as file:
        fieldnames = ['task_id', 'competency_name', 'skill_code', 'skill_name',
                      'start_date', 'end_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for task in roadmap_tasks:
            writer.writerow(task)
        print(f"Data from {input_path} has been written to {output_path} with calculatedtask duration of {task_duration} days.")
        
        

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

    
    
    
    
