import pandas as pd
import csv


read_file = pd.read_csv("/Users/jayj/software engineering process/JackJackRoadmap.txt", delimiter='|', skiprows=[0, 1])

read_file.to_csv("/Users/jayj/software engineering process/output.csv", index=False)

with open("/Users/jayj/software engineering process/output.csv", mode='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        if lines == 2:
            continue
        else:
            print(lines)