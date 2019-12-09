import csv
import os

"""Layer between the server and the data. Functions here should be called from the server.py and these should use generic functions from the connection.py"""


def get_data_from_csv(filename):
    qs_or_as = []
    with open(filename, newline='') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            q_or_a = dict(row)
            qs_or_as.append(q_or_a)
    return qs_or_as
