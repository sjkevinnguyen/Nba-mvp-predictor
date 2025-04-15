"""
@author: Kevin Nguyen, 2025
"""

# Necessary imports
import os
import pandas as pd

# Basic Variables
years = range(2004, 2025)
url1 = 'https://www.basketball-reference.com/awards/awards_{}.html'
url2 = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'
url3 = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'
url4 = 'https://www.basketball-reference.com/leagues/NBA_{}_advanced.html'

# Webscrape the data and condense all the seasons' data into one DataFrame

df = pd.DataFrame()

for year in years:

    # Webscrape each link for the stats table
    mvp = pd.read_html(url1.format(year), header=1, attrs={'id':'mvp'})[0]
    totals = pd.read_html(url2.format(year), header=0, attrs={'id':'totals_stats'})[0]
    per_game = pd.read_html(url3.format(year), header=0, attrs={'id':'per_game_stats'})[0]
    advanced = pd.read_html(url4.format(year), header=0, attrs={'id':'advanced'})[0]


    # Edit the features before combining
    mvp_ = mvp.drop(columns=['Rank', 'Age', 'Tm', 'First', 'Pts Won', 'Pts Max'], axis=1).\
        rename(columns={'MP':'MPPG', 'PTS':'PTSPG', 'TRB':'TRBPG', 'AST':'ASTPG', 'STL':'STLPG', 'BLK':'BLKPG'}).\
        fillna(0)
    
    totals_ = totals.drop(['Rk', 'Age', 'Team', 'Pos', 'Awards'], axis=1).\
                drop_duplicates(subset=['Player'], keep='first', ignore_index=True).\
                iloc[:-1].fillna(0)

    per_game_ = per_game.drop(['Rk', 'Age', 'Team', 'Pos', 'Awards'], axis=1).\
                    drop_duplicates(subset=['Player'], keep='first', ignore_index=True).\
                    rename(columns={'MP':'MPPG', 'FG':'FGPG', 'FGA':'FGAPG', '3P':'3PPG', '3PA':'3PAPG','2P':'2PPG', '2PA':'2PAPG', 'FT':'FTPG', 'FTA':'FTAPG',
                                    'ORB':'ORBPG', 'DRB':'DRBPG', 'TRB':'TRBPG', 'AST':'ASTPG', 'STL':'STLPG', 'BLK':'BLKPG', 'TOV':'TOVPG',
                                    'PF':'PFPG', 'PTS':'PTSPG'}).\
                    fillna(0).iloc[:-1]
    
    advanced_ = advanced.drop(['Rk', 'Age', 'Team', 'Pos', 'Awards'], axis=1).\
                    drop_duplicates(subset=['Player'], keep='first', ignore_index=True).\
                    fillna(0).iloc[:-1]
    
    # Merge the DataFrames together and add the year
    f = pd.merge(totals_, per_game_, how='outer')
    f = pd.merge(f, advanced_, how='outer')
    f = pd.merge(f, mvp_, how='outer').fillna(0)
    f['Year'] = year

    # Concatenate the DataFrame to the previous one vertically
    if df.empty:
        df = f
    else:
        df = pd.concat([df, f])
    
    # Print the progress along the way
    print(f'Season {year-1}-{year} DataFrame has been completed')

# Save the entire DataFrame to csv file
df.to_csv('data.csv', index = False)







    
    


