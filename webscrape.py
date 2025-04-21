"""
@author: Kevin Nguyen, 2025
"""

# Necessary imports
import os
import pandas as pd
import time
import random
import utilities

path = './data'
try:
    os.mkdir(path)
    print("Folder %s created!" % path)
except FileExistsError:
    print("Folder %s already exists" % path)

# Seasons = 2003-2024 to 2023-2024
years = range(2004, 2025)

for year in years:
    file_path = f"./data/{year}.csv"
    if os.path.exists(file_path):
        print(f"{year}.csv exists.")
        continue
    total = pd.read_html(f'https://www.basketball-reference.com/leagues/NBA_{year}_totals.html#totals_stats')[0]
    advanced = pd.read_html(f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html#advanced')[0]
    mvp = pd.read_html(f'https://www.basketball-reference.com/awards/awards_{year}.html#mvp')[0]
    team = pd.read_html(f'https://www.basketball-reference.com/leagues/NBA_{year}.html#advanced-team')

    df = utilities.combine_tables(total=total, advanced=advanced, mvp=mvp, team=team)
    df['Year'] = year

    df.to_csv(file_path, index = False)
    sleep_time = random.uniform(30, 60)  # Sleep between 2–5 seconds
    print(f"Sleeping for {sleep_time:.2f} seconds...")
    time.sleep(sleep_time)



    











