# This code is used to store user's roadmap plan and modify the database itself
# Input is the CSV that is converted from 'read-data.py'

# Created by Supakorn Etitum (JackJack) on 23 October 2024
# Modified by Gold, 8 November 2024

import sqlite3
import pandas as pd

# Create/connect to the database
def init_database(inputfile):
    con = sqlite3.connect('roadmap.db')
    # Create a cursor to execute commands on the database
    cursor = con.cursor()
    
    
    # Check if there are any tables in the database
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='roadmap';")
    result = cursor.fetchone()[0]  # Fetch the count of tables with the name 'roadmap'


    if result > 0:
        print("Roadmap already imported.")
        con.close()
        return 0
    
    

    # Read the CSV file into a DataFrame with specified encoding
    df = pd.read_csv(inputfile)  # Change encoding as necessary

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    df.columns = ['competency_code', 'competency_name', 'skill_code', 'skill_name']  # Example of renaming

    
    # Debug print to check the DataFrame columns
    # print("Columns in DataFrame:", df.columns.tolist())

    # Create the table (if it doesn't exist already)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS roadmap (
        competency_code TEXT,
        competency_name TEXT,
        skill_code TEXT,
        skill_name TEXT,
        duration TEXT
    )
    ''')

    # Insert the data from the DataFrame into the table
    for index, row in df.iterrows():
        try:
            cursor.execute('''
            INSERT INTO roadmap (competency_code, competency_name, skill_code, skill_name)
            VALUES (?, ?, ?, ?)
            ''', (row['competency_code'], row['competency_name'], row['skill_code'], row['skill_name']))
        except KeyError as e:
            print(f"KeyError: {e} - Check if the column names in the CSV match the expected names.")

    cursor.execute('''UPDATE roadmap 
                   SET competency_code = RTRIM(competency_code)''')
    # Commit the transaction to save changes
    con.commit()

    # Close the connection
    con.close()

    return 1

def read_roadmap_data():
    con = sqlite3.connect('roadmap.db')
    # Read the data from the roadmap table into a DataFrame
    df = pd.read_sql_query("SELECT * FROM roadmap", con)
    
    # Print the DataFrame
    print(df)
    
    # Close the connection
    con.close()
    
def clear_roadmap():
    con = sqlite3.connect('roadmap.db')
    
    cursor = con.cursor()
    
    cursor.execute('DELETE FROM roadmap')
    
    con.commit()
    
    con.close()
    
    
    

   

if __name__ == "__main__":
     # Ensure to provide the correct path to the CSV file
    init_database('/Users/jayj/A1CE-study-planner/source_code/data-management/output.csv')  # Change this to your actual CSV file path
    
#     # Call read function to display the tasks
    read_roadmap_data()
    
    clear_roadmap()