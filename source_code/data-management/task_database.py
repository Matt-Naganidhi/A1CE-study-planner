#This code handles the database for the tasks
#Inputs: database name
#outputs: none
#Author Supakorn Etitum 26/10/2024

import sqlite3
import pandas as pd


def create_database(database_name):
    connect = sqlite3.connect('tasks.db')

    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (competency_code TEXT,competency_name TEXT,skill_code TEXT,task_description TEXT, duration TEXT)''')

def update_database():
    connect = sqlite3.connect('tasks.db')
    connect.commit()
    connect.close()




