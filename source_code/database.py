# This code is used to store user's roadmap plan and modify the database itself
# Input is the CSV that is converted from 'read-data.py'

# Created by Supakorn Etitum (JackJack) on 23 October 2024

import sqlite3
import pandas as pd

# Create/connect to the database
def init_database(inputfile):
    con = sqlite3.connect('roadmap.db')
    # Create a cursor to execute commands on the database
    cursor = con.cursor()

    # Read the CSV file into a DataFrame with specified encoding
    df = pd.read_csv(inputfile, encoding='ISO-8859-1')  # Change encoding as necessary

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    # Debug print to check the DataFrame columns
    print("Columns in DataFrame:", df.columns.tolist())

    # Create the table (if it doesn't exist already)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS roadmap (
        competency_code TEXT,
        competency_name TEXT,
        skill_code TEXT,
        skill_name TEXT
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

    # Commit the transaction to save changes
    con.commit()

    # Close the connection
    con.close()

def read_roadmap_data():
    con = sqlite3.connect('roadmap.db')
    # Read the data from the roadmap table into a DataFrame
    df = pd.read_sql_query("SELECT * FROM roadmap", con)
    
    # Print the DataFrame
    print(df)
    
    # Close the connection
    con.close()

if __name__ == "__main__":
    # Ensure to provide the correct path to the CSV file
    init_database('/Users/jayj/A1CE-study-planner/source_code/data-management/output.csv')  # Change this to your actual CSV file path
    
    # Call read function to display the tasks
    read_roadmap_data()