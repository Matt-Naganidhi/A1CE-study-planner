import sqlite3
import pandas as pd

# Create/connect to the database
con = sqlite3.connect('roadmap.db')
cursor = con.cursor()

# Read the CSV file into a DataFrame
df = pd.read_csv('/Users/jayj/A1CE-study-planner/source_code/data-management/output.csv')

# Remove any extra spaces from column names
df.columns = df.columns.str.strip()

# Rename columns to avoid duplicates
df.columns = ['competency_code', 'competency_name', 'skill_code', 'skill_name']

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS roadmap (
        competency_code TEXT,
        competency_name TEXT,
        skill_code TEXT,
        skill_name TEXT
    )
''')

# Insert data into the table
for index, row in df.iterrows():
    cursor.execute('''
        INSERT INTO roadmap (competency_code, competency_name, skill_code, skill_name)
        VALUES (?, ?, ?, ?)
    ''', (row['competency_code'], row['competency_name'], row['skill_code'], row['skill_name']))

# Commit changes
con.commit()

# Fetch and print all rows
cursor.execute("SELECT * FROM roadmap")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
con.close()
