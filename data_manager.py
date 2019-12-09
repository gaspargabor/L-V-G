import csv
import os

"""Layer between the server and the data. Functions here should be called from the server.py and these should use generic functions from the connection.py"""


def get_data(filename):
    with open(filename, newline='') as data_file:
        data_as_rows = []
        reader = csv.DictReader(data_file)
        for row in reader:
            data_as_rows.append(row)
    return data_as_rows