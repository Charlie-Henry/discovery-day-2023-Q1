"""
pre-processes the raw output of the open data portal
"""

import pandas as pd
import os


def get_mean_std():
    group_cols = ["hour", "date", "year", "month", "zone_id"]
    years = [2020, 2021, 2022, 2023]
    months = range(1, 13)
    dfs = []
    for year in years:
        for month in months:
            filename = f"data/processed/{year}/{month}/parking_data.csv"
            if os.path.isfile(filename):
                dfs.append(pd.read_csv(filename))
    dfs = pd.concat(dfs)

    means = dfs.mean()
    stds = dfs.std()

    return means, stds


group_cols = ["hour", "date", "year", "month", "zone_id"]
years = [2020, 2021, 2022, 2023]
months = range(1, 13)
for year in years:
    for month in months:
        filename = f"data/raw/{year}/{month}/parking_data.csv"
        if os.path.isfile(filename):
            print(f"Processing {filename}")
            df = pd.read_csv(filename)
            df = df.dropna()
            df["date"] = pd.to_datetime(df["date"])
            df["date"] = pd.to_numeric(df["date"].values) / 10**9
            df = df.drop(["sum_duration_min"], axis=1)
            df = df[["date", "hour", "year", "month", "zone_id", "sum_amount"]]
            df = df.groupby(by=group_cols).sum()
            directory = f"data/processed/{year}/{month}/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            df.to_csv(f"data/processed/{year}/{month}/parking_data.csv")

# Now normalize data
mean, stds = get_mean_std()
pd.concat([mean, stds],axis=1).to_csv("mean_std.csv")
print(mean, stds)
years = [2020, 2021, 2022, 2023]
months = range(1, 13)
for year in years:
    for month in months:
        filename = f"data/processed/{year}/{month}/parking_data.csv"
        if os.path.isfile(filename):
            df = pd.read_csv(filename)
            df = df.astype(float)

            df = df.sub(mean).divide(stds)
            df.to_csv(
                f"data/processed/{year}/{month}/parking_data.csv", index=False
            )
