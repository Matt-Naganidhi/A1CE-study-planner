#This source code is used to read txt files and convert them into lists
#Inputs: input file path, output file path
#Outputs: records roadmap information to output.csv
#Author Supakorn Etitum (JackJack)
#Modified by Matt Naganidhi for filepath generalization
import pandas as pd
import csv
import os  # Import os to work with paths

def openFile(input_file_name, output_file_name):
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the running script

    # Construct the full input file path
    input_file_path = os.path.join(script_dir, input_file_name)

    # Read the CSV file with the specified delimiter, skipping the header and footer
    read_file = pd.read_csv(input_file_path, delimiter='|',skiprows=[1], skipfooter=2, engine='python')
    # Construct the full output file path
    
    output_file_path = os.path.join(script_dir, output_file_name)
    # Save the cleaned DataFrame to the output CSV file
    read_file.to_csv(output_file_path, index=False)

    # Open the output CSV file and print its content
    with open(output_file_path, mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            # Print lines that are not empty
            if lines:  # Check if the line is not empty
                print(lines)

openFile("JackJackRoadmap.txt", "output.csv")
