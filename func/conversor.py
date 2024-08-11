import glob
import csv

def get_csv_files(data_path):
    return glob.glob(data_path + '/*.csv')

def determine_delimiter(file_path):
    if 'brasil_ministerio_saude' in file_path:
        return ';'
    else:
        return ','

def read_csv_file(file_path, delimiter):
    with open(file_path, 'r', encoding='utf-8') as file:
        return list(csv.reader(file, delimiter=delimiter))

def get_data_from_csv(data_path):
    data = []
    csv_files = get_csv_files(data_path)
    for file_path in csv_files:
        delimiter = determine_delimiter(file_path)
        data.extend(read_csv_file(file_path, delimiter))
    return data