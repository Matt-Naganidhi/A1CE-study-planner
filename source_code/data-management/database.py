#This code is used to store user's roadmap plan and modify the database itself
#Input is the csv that is convert from 'read-data.py'

#Created by Supakorn Etitum (JackJack) on 23 October 2024

import sqlite3
from sqlite3 import SQLITE_PRAGMA
import pandas as pd

# Create/connect to the database
con = sqlite3.connect('roadmap.db')
# Create a cursor to execute commands on the database
cursor = con.cursor()

# Read the CSV file into a DataFrame
df = pd.read_csv('/Users/jayj/A1CE-study-planner/source_code/data-management/output.csv')

df.columns = df.columns.str.strip()
print(df.columns) 

print(df['title'])

# Create the table (if it doesn't exist already)
cursor.execute('''CREATE TABLE IF NOT EXISTS roadmap (competency_code TEXT,competency_name TEXT,skill_code TEXT,skill_name TEXT)''')

# Insert the data from the DataFrame into the table
for index, row in df.iterrows():
    cursor.execute('''
    INSERT INTO roadmap (competency_code, title, assessed_skill_code, title)
    VALUES (?, ?, ?, ?)
    ''', (row['competency_code'], row['competency_name'], row['skill_code'], row['skill_name']))

# Commit the transaction to save changes
con.commit()

# Fetch and print all rows from the 'roadmap' table
cursor.execute("SELECT * FROM roadmap")
rows = cursor.fetchall()

# Print all rows
for row in rows:
    print(row)

# Close the connection
con.close()