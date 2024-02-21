"""
    Module name :- solution
"""


import os
import csv
from datetime import datetime


def load_csv(filepath):
    """
        Load data.
    """
    filepath = os.path.abspath(filepath)

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))

    return reader


def filter_data_by_date(data):
    """
        Filter data by date.
    """
    return sorted(data, key = lambda x: x.get('fordate'))


def month_data(data, month, idx):
    """
        Month data.
    """
    month_list = []
    while idx < len(data):
        record = data[idx]
        date_obj = datetime.strptime(record['fordate'], '%Y-%m-%d')

        if date_obj.month != month:
            break

        month_list.append(record)
        idx += 1

    return idx, month_list


def monthly_data(data):
    """
        Monthly Data.
    """
    idx = 0
    monthly_list = []

    while idx < len(data):
        record = data[idx]
        month = datetime.strptime(record['fordate'], '%Y-%m-%d').month
        idx, month_list = month_data(data, month, idx)
        monthly_list.append(month_list)

    return monthly_list


def filter_by_shape(data, shapes):
    """
        Filter by shape.
    """
    shapes_dict = {}

    for shape in shapes:
        for record in data:
            if shape == record['shape']:
                shapes_dict[shape] = shapes_dict.get(shape, []) + [record]


    return shapes_dict


def main():
    """
        Main.
    """
    data = load_csv('HB_NORTH_CRR.csv')
    filtered_data = filter_data_by_date(data)
    monthly_records = monthly_data(filtered_data)
    shapes = {record['shape'] for record in data}
    records = []

    for month_record in monthly_records:
        shapes_dict = filter_by_shape(month_record, shapes)
        
        for record in shapes_dict.values():
            entry = sorted(record, key = lambda x: x.get('sequence'), reverse=True)[-1]
            if entry:
                records.append(entry)

    filepath = os.getcwd() + '/answer.csv'

    with open(filepath, 'w', encoding='utf-8') as f:
        headers = records[0].keys()
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    return filepath

if __name__ == '__main__':
    print(main())