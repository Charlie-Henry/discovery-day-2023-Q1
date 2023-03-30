"""
Uses the open data portal to download parking data.
"""
import csv
import os

from dotenv import load_dotenv
from sodapy import Socrata

load_dotenv()

SOCRATA_KEY = os.getenv("SOCRATA_KEY")
SOCRATA_SECRET = os.getenv("SOCRATA_SECRET")
SOCRATA_TOKEN = os.getenv("SOCRATA_TOKEN")


def read_kiosk_lookup():
    f_name = "kisoks_to_zones.csv"
    key_column = "STATION_NUMBER"
    # create an empty list to store the data
    kisok_lookup = {}
    # open the CSV file and read the data into the list
    with open(f_name, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row.pop(key_column)
            kisok_lookup[key] = row["ZONE_DESCRIPTION"]
    return kisok_lookup


def download_data(client, month, year):
    data = client.get(
        "5bb2-gtef",
        select="date_extract_hh(start_time) as hour, date_trunc_ymd(start_time) as date, date_extract_y(start_time) as year, date_extract_m(start_time) as month, meter_id, zone_id, sum(amount), sum(duration_min)",
        where=f"month={month} AND year={year}",
        order="date",
        group="year,month,date,hour,meter_id,zone_id",
        limit=999999999,
        exclude_system_fields=True,
    )

    return data


def write_csv(data, kisok_lookup, month, year):
    directory = f"data/raw/{year}/{month}/"
    # create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # specify the output CSV filename
    output_filename = f"data/raw/{year}/{month}/parking_data.csv"

    # open the output CSV file for writing
    with open(output_filename, "w", newline="") as csvfile:
        # create a CSV writer object
        writer = csv.writer(csvfile)

        keys = list(data[0].keys())

        headers = []
        for h in keys:
            if h == "meter_id":
                h = "zone_id"
            headers.append(h)

        # write the header row
        writer.writerow(headers)

        # write the data rows
        for row in data:
            if "meter_id" in row:
                if row["meter_id"] in kisok_lookup:
                    row["meter_id"] = kisok_lookup[row["meter_id"]]
                    if row["meter_id"]:
                        writer.writerow(row.values())
            else:
                if row["zone_id"]:
                    writer.writerow(row.values())


def main():
    client = Socrata(
        "datahub.austintexas.gov",
        SOCRATA_TOKEN,
        username=SOCRATA_KEY,
        password=SOCRATA_SECRET,
        timeout=500,
    )
    kisok_lookup = read_kiosk_lookup()

    years = [2020, 2021, 2022, 2023]
    months = range(1, 13)
    for year in years:
        for month in months:
            data = download_data(client, month, year)
            if data:
                print(f"Writing file: {year}/{month}/parking_data.csv")
                write_csv(data, kisok_lookup, month, year)


main()
