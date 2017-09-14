import csv
import numpy as np

data_dict = {}

with open('surveyResults_AllGPSS.csv', 'rb') as f:
    data = np.asarray(csv.reader(f))
    for i in xrange(len(data[0])):
        column = data[:,i]
        data_dict[column[0]] = column[2:]
        print column
    