from naivebayes import NaiveBayes
from vertex import Vertex

import csv

def create_id3_tree():
    return None


def entropy():
    return None


def get_data():
    with open('../datasets/tic-tac-toe.data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        row_data = []
        for row in spamreader:
            split = row[0].split(",")
            row_data.append(split)

        for row in row_data:



        print(row_data)

