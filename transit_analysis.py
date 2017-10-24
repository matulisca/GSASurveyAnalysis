import csv
import numpy as np

data_dict = {}

def get_data():
    with open('surveyResults_AllGPSS.csv', 'rt') as f:
        data = np.asarray(list(csv.reader(f)))
    return data
    
def analyze_data():
    for i in xrange(len(data[0])):
        column = data[:,i]
        data_dict[column[0]] = column[2:]
        print(column)
    