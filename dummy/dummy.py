import csv
import os

curPath = os.path.abspath(os.path.dirname(__file__))

with open(curPath + '/Dummy data.csv','rt')as csvfile:
    reader = csv.DictReader(csvfile)
    idList = [row['\ufeffid'] for row in reader]

with open(curPath + '/Solution.csv',"w") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerow(["id","new_number"])
    for i in range(len(idList)):
        writer.writerow([idList[i],int(idList[i])+2])

