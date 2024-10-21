#This source code is used to read txt files and convert them into lists
#Inputs: input file path, output file path
#Outputs: None
#Author Supakorn Etitum (JackJack)

import pandas as pd
import csv


def openFile(file_path,output_path):
    read_file = pd.read_csv(file_path, delimiter='|', skiprows=2, skipfooter=2, engine='python')

    read_file.to_csv(output_path, index=False)

    with open(output_path, mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if lines == 2:
                continue
            else:
                print(lines)
                
openFile("/Users/jayj/software engineering process/JackJackRoadmap.txt","/Users/jayj/software engineering process/output.csv")