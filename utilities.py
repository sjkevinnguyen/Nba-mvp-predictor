import pandas as pd
import os

def process_team(team):
    east, west = team[0].copy(), team[1].copy()

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
    "Washington Wizards": "WAS",
    "Vancouver Grizzlies": "MEM",

    # Historical/renamed teams since 2004:
    "Seattle SuperSonics": "OKC",
    "New Jersey Nets": "BRK",
    "Charlotte Bobcats": "CHO",
    "New Orleans Hornets": "NOP",  # Also seen as "NOK" during Katrina years
    "New Orleans/Oklahoma City Hornets": "NOP"
    }
    
    east = east[east['Eastern Conference'].str.contains('Division') == False]
    west = west[west['Western Conference'].str.contains('Division') == False]
    east.rename(columns={'Eastern Conference':'Team'}, inplace=True) 
    west.rename(columns={'Western Conference':'Team'}, inplace=True)
    east = east.sort_values(by='W/L%', ascending=False)
    west = west.sort_values(by='W/L%', ascending=False)
    east['Seed'] = range(1, len(east) + 1)
    west['Seed'] = range(1, len(west) + 1)
    df = pd.concat([east, west], ignore_index=True)
    df['Team'] = df['Team'].str.replace(r'\s*\(\d+\)', '', regex=True)
    df['Team'] = df['Team'].str.replace(r'\*', '', regex=True)  
    df['Team'] = df['Team'].map(nba_teams)
    return df.loc[:, ['Team', 'W/L%', 'Seed']]

def combine_tables(total, advanced, mvp, team):
    team = process_team(team)
    
    # total data processing
    total = total.loc[:, ['Player','Team','G','GS', 'MP','FG%','3P%','2P%', 'eFG%', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 'PTS']].iloc[:-1]
    total['MP'] = round(total['MP']/total['G'], 1)
    total['TRB'] = round(total['TRB']/total['G'], 1)
    total['AST'] = round(total['AST']/total['G'], 1)
    total['STL'] = round(total['STL']/total['G'], 1)
    total['BLK'] = round(total['BLK']/total['G'], 1)
    total['PTS'] = round(total['PTS']/total['G'], 1)

    # advanced data processing
    advanced = advanced.loc[:,['Player', 'Team', 'PER', 'TS%','DRB%','TRB%','AST%','STL%','BLK%','USG%','OWS','DWS','BPM', 'VORP', 'WS','WS/48']].iloc[:-1]

    # mvp data processing
    if not mvp.empty:
        mvp_ = mvp.copy()
        mvp_.columns = mvp_.columns.get_level_values(1)
        mvp_ = mvp_.loc[:, ['Player', 'Share']]
    
    # combine total and advanced and then mvp
    stats = pd.merge(total, advanced, how='outer')
    replacements =  {
    "SEA": "OKC",
    "NJN": "BRK",
    "CHA": "CHO",
    "NHO": "NOP",  # Also seen as "NOK" during Katrina years
    "NOK": "NOP",
    "NOH": "NOP"
    }
    stats['Team'] = stats['Team'].replace(replacements)

    correct_teams = stats.drop_duplicates(subset=['Player'], keep='last', ignore_index=True)
    correct_teams = correct_teams.loc[:,['Player', 'Team']]
    stats = stats.drop_duplicates(subset=['Player'], keep='first', ignore_index=True)
    final = pd.merge(stats.drop(columns=('Team')), correct_teams, how='outer')
    cols = list(final.columns)
    cols.insert(1, cols.pop(cols.index("Team")))
    final = final[cols]

    if not mvp.empty:
        final = pd.merge(final, mvp_, how='outer').fillna(0)
    
    final = pd.merge(final, team, on='Team', how='left').fillna(0)
    return final

def combine_data_folder():
    folder = './data'
    files = sorted(os.listdir(folder), key=lambda f: int(f.split('.')[0]))
    df_all = pd.DataFrame()
    for file in files:
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)
        df_all = pd.concat([df_all, df], ignore_index=True)
    
    return df_all

def previous_seeds():
    folder = './data'
    files = sorted(os.listdir(folder), key=lambda f: int(f.split('.')[0]))
    df_all = pd.DataFrame()
    for file in files:
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)
        df['Year'] = df['Year'] + 1
        df['Year'] = df['Year'].astype(int)
        if df['Year'][0] == 2025:
            continue
        df = df.loc[:, ['Team', 'Year', 'Seed']]
        df.rename(columns={'Seed':'Previous Seed'}, inplace=True)
        df.drop_duplicates(subset=['Team'], inplace=True, ignore_index=True)
        df_all = pd.concat([df_all, df], ignore_index=True)
    return df_all

