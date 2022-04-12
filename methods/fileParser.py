import csv
'''
row:    [function,epsilon,max iteration]
'''
def csvreader(filename, skipFirstLine=False):
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        if skipFirstLine:
            next(reader, None)
        for row in reader:
            yield row