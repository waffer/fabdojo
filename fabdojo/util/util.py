import csv

def csv_reader(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
