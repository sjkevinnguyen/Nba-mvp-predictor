"""
@author: Kevin Nguyen, 2025
"""

# Necessary imports
import os
import pandas as pd

# Variables
years = range(2004, 2025)
url1 = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'
url2 = 'https://www.basketball-reference.com/leagues/NBA_{}_advanced.html'
url3 = 'https://www.basketball-reference.com/leagues/NBA_{}.html'
url4 = 'https://www.basketball-reference.com/awards/awards_{}.html'
df = pd.DataFrame()

nba_teams = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",  # Sometimes "BKN"
    "Chicago Bulls": "CHI",
    "Charlotte Hornets": "CHO",  # Sometimes "CHA"
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
}

# Webscrape from basketball reference
for year in years:
    
    total_stats = pd.read_html(url1.format(year), header=0, attrs={'id':'totals_stats'})[0]
    advanced_stats = pd.read_html(url2.format(year), header=0, attrs={'id':'advanced'})[0]
    try:
        east_stats = pd.read_html(url3.format(year), header=0, attrs={'id':'confs_standings_E'})[0]
        west_stats = pd.read_html(url3.format(year), header=0, attrs={'id':'confs_standings_W'})[0]
    except ValueError:
        east_stats = pd.read_html(url3.format(year), header=0, attrs={'id':'divs_standings_E'})[0]
        west_stats = pd.read_html(url3.format(year), header=0, attrs={'id':'divs_standings_W'})[0]
    mvp_stats = pd.read_html(url4.format(year), header=1, attrs={'id':'mvp'})[0]

    # Slight Data Processing
    
    # Abbreviate the Team Names for use with other tables and added their seed
    east_stats_ = east_stats.rename(columns={'Eastern Conference':'Team'}).loc[:,['Team', 'W/L%']]
    east_stats_['Team'] = east_stats_['Team'].str.replace('*','', regex=True)
    east_stats_['Seed'] = east_stats.index + 1
    west_stats_ = west_stats.rename(columns={'Western Conference':'Team'}).loc[:,['Team', 'W/L%']]
    west_stats_['Team'] = west_stats_['Team'].str.replace('*','', regex=True)
    west_stats_['Seed'] = west_stats.index + 1

    # Combine both conferences into one DataFrame
    team_stats_ = pd.concat([east_stats_, west_stats_])
    team_stats_.replace(nba_teams, inplace=True)

    # Select main columns for use in model, select the combined stats for players who have played for 2+ teams
    advanced_stats_ = advanced_stats.loc[:,['Player', 'Team', 'G', 'GS', 'MP', 'PER', 'TS%',
       '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%','USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']].iloc[:-1]
    advanced_stats_['MP'] = round(advanced_stats_['MP'] / advanced_stats_['G'], 1)
    advanced_stats_.drop_duplicates('Player', keep='first', inplace=True)
    total_stats_ = total_stats.loc[:, ['Player','FGA', 'FG%', '3P%', 'FT%','eFG%', 'PTS']].iloc[:-1]
    total_stats_.drop_duplicates('Player', keep='first', inplace=True)
    mvp_stats_ = mvp_stats.loc[:,['Player', 'Tm', 'Share', 'MP', 'FG%', '3P%', 'FT%', 'WS', 'WS/48']]
    mvp_stats_.rename(columns={'Tm':'Team'}, inplace=True)
    mvp_stats_

    # Find the team players finished the season with (used for the 2+ team players)
    last_teams = advanced_stats.copy()
    last_teams = last_teams.loc[:, ['Player', 'Team']]
    last_teams.drop_duplicates('Player', keep='last', inplace=True)
    
    # Change the teams in advanced to correct for the teams they finished the season with
    advanced_stats_ = advanced_stats_.merge(last_teams, on='Player', suffixes=('', '_Correct'))
    advanced_stats_['Team'] = advanced_stats_['Team_Correct']
    advanced_stats_.drop(columns=['Team_Correct'], inplace=True)

    f = pd.merge(advanced_stats_, total_stats_, how='outer')
    f = pd.merge(f, mvp_stats_, how='outer')
    f = pd.merge(f, team_stats_, how='outer').fillna(0)
    f['Year'] = year

    # Concatenate the DataFrame to the previous one vertically
    if df.empty:
        df = f
    else:
        df = pd.concat([df, f])

    #Print the progress along the way
    print(f'Season {year-1}-{year} DataFrame has been completed')

# Save the entire DataFrame to csv file
df.to_csv('data.csv', index = False)









