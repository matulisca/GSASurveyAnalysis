import csv
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from itertools import chain

data_dict = {}
GPSS_FILE = 'surveyResults_AllGPSS_True.csv'
GSAS_FILE = 'surveyResults_1PassCleanGradStudents.csv'
NUM_DATASETS = 2

def get_data(file):
    data = pd.read_csv(file, encoding = "ISO-8859-1")
    # with open('surveyResults_AllGPSS.csv', 'rt') as f:
    #     data = np.asarray(list(csv.reader(f)))
    return data.drop(data.index[1]) # Remove non-data rows
    
def analyze_data():
    for i in xrange(len(data[0])):
        column = data[:,i]
        data_dict[column[0]] = column[2:]
        print(column)

def clean_string(string, min_width=10):
    last_break = 0
    i = 0
    while i < len(string):
        if i > last_break + min_width and string[i] == ' ':
            string = string[:i] + '\n' + string[i:]
            last_break = i + 2
            i += 1
        i += 1
    return string

def hist_from_diff(data1, data2, col, split=True, **kwargs):
    counts_dict1, length1 = get_counts_dict(data1, col, split)
    counts_dict2, length2 = get_counts_dict(data2, col, split)

    counts_dict = {}
    for key in counts_dict1:
        if key in counts_dict2:
            counts_dict[key] = counts_dict1[key]-counts_dict2[key]
    length = length1 - length2

    plot_hist(counts_dict, length, **kwargs)

def hist_from_column(data, col, split=True, **kwargs):
    counts_dict, length = get_counts_dict(data, col, split)

    plot_hist(counts_dict, length, **kwargs)

def hist_from_column_parseWords(data, col, split=True, **kwargs):
    counts_dict, length = get_counts_dict_parseWords(data, col)

    plot_hist_parseWords(counts_dict, length, **kwargs)

def get_counts_dict(data, col, split):
    column = data[col][2:]
    length = len(column)
    if split:
        split_column = []
        for item in column:
            if item is not np.nan and ',' in item:
                split_column.extend(item.split(','))
            else:
                split_column.append(item)
        column = split_column

    counts_dict = Counter(column)
    if np.nan in counts_dict.keys():
        length -= counts_dict[np.nan]
        counts_dict.pop(np.nan)
    return counts_dict, length

def get_counts_dict_parseWords(data, col):
    column = data[col][2:]
    length = len(column)
    split_column = []
    for item in column:
        if item is not np.nan:
            split_column.extend(item.split())
    column = split_column
    counts_dict = Counter(column)

    entries_to_remove = ('the', 'and', 'No', 'no', 'I', 'to', 'of', 'at', 'on', 'between', 'street', 'Street', 'from', 'in', 'is', \
                        'St.', 'St', 'The', 'feel', 'safe', 'a', 'near', 'after', 'not', 'are', 'do', 'but', 'that', 'by', 'all')
    for k in entries_to_remove:
        length -= counts_dict[k]
        counts_dict.pop(k)
    print(counts_dict)
    return counts_dict, length

def plot_hist(counts_dict, length=None, label='', ax=None, offset=None, width=1):
    responses = list(counts_dict.keys())
    for i in range(len(responses)):
        responses[i] = clean_string(responses[i])

    counts = np.array(list(counts_dict.values()))
    if length is None:
        length = counts.sum()
    counts = counts / length * 100

    indexes = np.arange(len(responses), dtype='float64')
    if offset is not None:
        indexes += offset

    if ax is None:
        fig, ax = plt.subplots()
    ax.bar(indexes, counts, width, label='{} n={}'.format(label, length))
    ax.set_xticks(indexes - offset/2)
    ax.set_xticklabels(responses, rotation=0, ha='center')
    ax.set_xlabel('response')
    ax.set_ylabel('percent of responses')

def plot_hist_parseWords(counts_dict, length=None, label='', ax=None, offset=None, width=1):
    responses = list(counts_dict.keys())
    responses = responses[:30]
    for i in range(len(responses)):
        responses[i] = clean_string(responses[i])

    counts = np.array(list(counts_dict.values()))
    counts = counts[:30]

    indexes = np.arange(len(responses), dtype='float64')
    if offset is not None:
        indexes += offset

    if ax is None:
        fig, ax = plt.subplots()
    ax.bar(indexes, counts, width, label='{} n={}'.format(label, length))
    ax.set_xticks(indexes - offset/2)
    ax.set_xticklabels(responses, rotation=0, ha='center')
    ax.set_xlabel('response')
    ax.set_ylabel('percent of responses')

if __name__ == '__main__':
    GPSS_DATA = get_data(GPSS_FILE)
    GSAS_DATA = get_data(GSAS_FILE)


    for q in list(GSAS_DATA):
        if q in ['Q4_11_TEXT', 'Q5', 'Q6', 'Q6_5_TEXT', 'Q7A', 'Q17', 'Q7B_3_TEXT', 'Q8', 'Q9_5_TEXT', 'Q12A', 'Q13A', 'Q8 - Topics']:
            continue
        fig, ax = plt.subplots(figsize=[20, 20])
        hist_from_column(GPSS_DATA, q, label='GPSS', ax=ax, offset=0.0, width=0.3)
        hist_from_column(GSAS_DATA, q, label='GSAS', ax=ax, offset=0.3, width=0.3)
        hist_from_diff(GPSS_DATA, GSAS_DATA, q, label='PROF', ax=ax, offset=0.6, width=0.3)
        ax.set_title(GPSS_DATA[q][0])
        ax.legend()
        fig.tight_layout()
        fig.savefig(q + '.')

    for q in list(GSAS_DATA):
        if q in ['Q5']:
            fig, ax = plt.subplots(figsize=[20, 20])
            hist_from_column_parseWords(GPSS_DATA, q, 0, label='GPSS', ax=ax, offset=0.0, width=0.3);
            ax.set_title(GPSS_DATA[q][0])
            ax.legend()
            fig.tight_layout()
            fig.savefig(q + '.png')
