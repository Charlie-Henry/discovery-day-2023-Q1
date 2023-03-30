"""
pre-processes the raw output of the open data portal
"""

import pandas as pd
import os

group_cols = ["hour","date","year","month","zone_id"] 
years = [2020, 2021, 2022, 2023]
months = range(1, 13)
for year in years:
    for month in months:
        filename = f"data/raw/{year}/{month}/parking_data.csv"
        if os.path.isfile(filename):
            print(f"Processing {filename}")
            df = pd.read_csv(filename)
            df = df.groupby(by=group_cols).sum()
            
            directory = f"data/processed/{year}/{month}/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            df.to_csv(f"data/processed/{year}/{month}/parking_data.csv")
            
