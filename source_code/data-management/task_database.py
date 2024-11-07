#This code handles the database for the tasks
#Inputs: database name
#outputs: none
#Author Supakorn Etitum 26/10/2024

import sqlite3
import pandas as pd


def create_database():
    connect = sqlite3.connect('tasks.db')

    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (competency_code TEXT,competency_name TEXT,skill_code TEXT,task_description TEXT, duration TEXT)''')

def update_database():
    connect = sqlite3.connect('tasks.db')
    connect.commit()
    connect.close()
    
def read_task_database():
    con = sqlite3.connect('roadmap.db')
    # Read the data from the roadmap table into a DataFrame
    df = pd.read_sql_query("SELECT * FROM tasks", con)
    
    # Print the DataFrame
    print(df)
    
    # Close the connection
    con.close()


if __name__ == "__main__":
    # Ensure to provide the correct path to the CSV file
    create_database()  # Change this to your actual CSV file path
    
    # Call read function to display the tasks
    read_task_database()

