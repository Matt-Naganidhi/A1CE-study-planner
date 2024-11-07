import sqlite3
import pandas as pd


# Create/connect to the database
<<<<<<< HEAD
def init_database(inputfile):
    con = sqlite3.connect('roadmap.db')
    # Create a cursor to execute commands on the database
    cursor = con.cursor()
=======
con = sqlite3.connect('roadmap.db')
cursor = con.cursor()
>>>>>>> a68776a43ea105cfbe23a132eac1d7d1aa197436

    # Read the CSV file into a DataFrame
    df = pd.read_csv(inputfile)

<<<<<<< HEAD
    # Create the table (if it doesn't exist already)
    cursor.execute('''CREATE TABLE IF NOT EXISTS roadmap (competency_code TEXT,competency_name TEXT,skill_code TEXT,skill_name TEXT)''')

    df.columns = df.columns.str.strip()
    print(df.columns)

    print(df['title'])
=======
# Remove any extra spaces from column names
df.columns = df.columns.str.strip()

# Rename columns to avoid duplicates
df.columns = ['competency_code', 'competency_name', 'skill_code', 'skill_name']
>>>>>>> a68776a43ea105cfbe23a132eac1d7d1aa197436

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS roadmap (
        competency_code TEXT,
        competency_name TEXT,
        skill_code TEXT,
        skill_name TEXT
    )
''')

<<<<<<< HEAD

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
# for row in rows:
#     print(row)

# Close the connection
    con.close()
=======
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
>>>>>>> a68776a43ea105cfbe23a132eac1d7d1aa197436
