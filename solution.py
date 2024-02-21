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

    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = list(csv.DictReader(f))

    return reader


def filter_data_by_date(data):
    """
    Filter data by date.
    """
    return sorted(data, key=lambda x: x.get("fordate"))


def month_data(data, month, idx):
    """
    Month data.
    """
    month_list = []
    while idx < len(data):
        record = data[idx]
        date_obj = datetime.strptime(record["fordate"], "%Y-%m-%d")

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
        month = datetime.strptime(record["fordate"], "%Y-%m-%d").month
        idx, month_list = month_data(data, month, idx)
        monthly_list.append(month_list)

    return monthly_list


def filter_by_shape(data):
    """
    Filter by shape.
    """
    shapes = ["Off-peak", "PeakWD", "PeakWE"]
    off_peak, peak_we, peak_wd = [], [], []

    for record in data:
        if record["shape"] == shapes[0]:
            off_peak.append(record)
        elif record["shape"] == shapes[1]:
            peak_wd.append(record)
        else:
            peak_we.append(record)

    return off_peak, peak_wd, peak_we


def main():
    """
    Main.
    """
    data = load_csv("HB_NORTH_CRR.csv")
    filtered_data = filter_data_by_date(data)
    monthly_records = monthly_data(filtered_data)
    records = []

    for month_record in monthly_records:
        off_peak_list, peak_wd_list, peak_we_list = filter_by_shape(month_record)

        off_peak = sorted(off_peak_list, key=lambda x: x.get("sequence"), reverse=True)[
            -1
        ]
        peak_wd = sorted(peak_wd_list, key=lambda x: x.get("sequence"), reverse=True)[
            -1
        ]
        peak_we = sorted(peak_we_list, key=lambda x: x.get("sequence"), reverse=True)[
            -1
        ]

        records += [off_peak, peak_wd, peak_we]

    filepath = os.getcwd() + "/answer.csv"

    with open(filepath, "w", encoding="utf-8") as f:
        headers = records[0].keys()
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    return filepath


if __name__ == "__main__":
    print(main())
