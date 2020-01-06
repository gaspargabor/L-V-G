import csv

"""def get_data_from_csv(filename):
    #reads all data from .csv and returns a list with dictionaries
    data_from_csv = []
    with open(filename, newline='') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            data_line = dict(row)
            data_from_csv.append(data_line)
    return data_from_csv


def write_data_to_csv(filename, header, new_data_row, append=True):
    #reads in all data from .csv and either appends the new line OR finds a row based on id, updates it with the new
    #row and writes the updated list of dictionaries back to the .csv
    current_data = get_data_from_csv(filename)
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for row in current_data:
            if not append:
                if row['id'] == new_data_row['id']:
                    row = new_data_row
            writer.writerow(row)
        if append:
            writer.writerow(new_data_row)

def write_datas_to_csv(filename, header, datas):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for row in datas:
            writer.writerow(row)"""
