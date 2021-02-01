from datetime import datetime, timedelta
from pathlib import Path
import os
from os.path import isfile

import requests


_CSV_URL = "https://oracleselixir-downloadable-match-data.s3-us-west-2.amazonaws.com/2021_LoL_esports_match_data_from_OraclesElixir_{}.csv"


def _download_csv(date):
    csv_request = requests.get(_CSV_URL.format(date.strftime("%Y%m%d")))

    if not csv_request.ok:
        raise FileNotFoundError

    csv_name = f"games2021_{date}.csv"
    with open(csv_name, "wb") as csv_file:
        csv_file.write(csv_request.content)

    print("File updated successfully.")

    games2021_csvs = [file for file in os.listdir() if isfile(file) and file.startswith("games2021_") and file.endswith(".csv")]

    for csv in games2021_csvs:
        if csv == csv_name:
            continue
        os.remove(csv)

    return csv_name


def update_and_get_latest_csv():
    today = datetime.now().date()
    yesterday = datetime.now().date() - timedelta(days=1)
    todays_csv = f"games2021_{today}.csv"
    yesterdays_csv = f"games2021_{yesterday}.csv"

    print(f"Today's date is {today}.")

    if isfile(todays_csv):
        print("The csv file is up to date with data published today.")
        return todays_csv

    print("The csv file is not up to date with data published today. Updating...")
    try:
        return _download_csv(today)
    except FileNotFoundError:
        print("No csv file for today could not be found. It has likely not yet been published.")

    if isfile(yesterdays_csv):
        print("The csv file is up to date with data published yesterday. Using this data for now.")
        return yesterdays_csv

    print("The csv file is not up to date with data published yesterday. Updating...")
    return _download_csv(yesterday)
