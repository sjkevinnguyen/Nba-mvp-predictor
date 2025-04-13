"""
@author: Kevin Nguyen, 2025
"""

# Necessary imports
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Basic Variables
years = range(2004, 2025)

url1 = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'
url2 = 'https://www.basketball-reference.com/leagues/NBA_{}_advanced.html'
url3 = 'https://www.basketball-reference.com/awards/awards_{}.html'
url4 = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'



# Webscrape NBA data, convert to csv, and place in appropriate folder

try:
    os.mkdir('data')
except FileExistsError:
    pass

for year in years:
    
    # Webscrape data
    total = pd.read_html(url1.format(year), header=0, attrs={'id':'totals_stats'})[0]
    advanced = pd.read_html(url2.format(year), header=0, attrs={'id':'advanced'})[0]
    mvp = pd.read_html(url3.format(year), header=1, attrs={'id':'mvp'})[0]
    per_game = pd.read_html(url4.format(year), header=0, attrs={'id':'per_game_stats'})[0]

    # Adjust DataFrames
    total = total.drop(['Rk', 'Age', 'Team', 'Pos', 'Awards'], axis=1).\
                iloc[:-1].\
                drop_duplicates(subset=['Player'], keep='first', ignore_index=True)
    advanced = advanced.drop(['Rk', 'Age', 'Team', 'Pos', 'Awards'], axis=1).\
                iloc[:-1].\
                drop_duplicates(subset=['Player'], keep='first', ignore_index=True)
    
    per_game = per_game.drop(['Rk', 'Team', 'Age','Pos', 'Awards'], axis=1).\
                iloc[:-1].\
                drop_duplicates(subset=['Player'], keep='first', ignore_index=True)

    mvp = mvp.drop(['Rank', 'Age', 'Tm'], axis=1)

    #Adjust per game columns to match mvp columns (b/c they were mislabeled on basketball reference)
    per_game = per_game.add_suffix('PG').drop(columns=['GPG', 'GSPG'], axis=1).rename(columns={'PlayerPG':'Player'})

    # Drop mvp columns instead of changing column names b/c I'm lazy
    mvp.drop(columns=['MP','PTS','TRB','AST','STL','BLK','FG%','3P%','FT%'])

    # Combine Total + Advanced and Per_Game + mvp DataFrames
    total_advanced = pd.merge(total, advanced, how='outer')
    per_game_mvp = pd.merge(per_game, mvp, how='outer')

    # Merge everything into the final DataFrame, Add First Point Share, and Year
    final = pd.merge(per_game_mvp, total_advanced, how='outer', on='Player').fillna(0)
    final['Pts Max'] = final['Pts Max'].max()
    final['First Pts Share'] = final['First'] / final['Pts Max']
    final['Year'] = year

    file_name = '{}.csv'
    final.to_csv(os.path.join('data/',file_name.format(year)))







    
    


