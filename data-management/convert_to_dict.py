# This source file is made to read .txt file for the format
# of A1CE roadmap sent by Dr.Sally and convert the data
# into dictionary using competency code as a key.
# input: A1CE roadmap file .txt version
# output: none

# Crated by Gold, 18 October 2024

import pprint  # library imported for print the data structure for better visualization
import pandas as pd
import csv

# initialize dictionary
competency_dict = {}

# Prompt user for input .txt file
inputfile = input("Enter A1CE file:")

with open(inputfile, 'r') as file:
    # Read the content of the file
    lines = file.readlines()

# Delete header and last row in .txt
lines = lines[2:-2]


for line in lines:
    # split data instances in the row separated by |
    parts = line.split("|")

    # Assign parts to its supposed value
    competency_code = parts[0].strip()
    title = parts[1].strip()
    skill_code = parts[2].strip()
    skill_title = parts[3].strip()

    # if competency code is not in the dictionary yet
    if competency_code not in competency_dict:
        competency_dict[competency_code] = {
            "title": title,
            "skills": []
        }

    # Append the skill to the list under the competency code
    competency_dict[competency_code]["skills"].append({
        "assessed_skill_code": skill_code,
        "skill_title": skill_title
    })

# print dictionary
pprint.pprint(competency_dict)
