"""
@author Kevin Nguyen 2025
"""

# Necessary Import
import pandas as pd
import utilities
import numpy as np
from xgboost import XGBRegressor

#Variables
features = ['VORP', 'W/L%', 'USG%', 'WS/48', 'PER', 'Seed']
params = {'max_depth': 5 ,'learning_rate': 0.1,'n_estimators': 300, 'subsample': 0.8}

# Set up DataFrame for training
df = utilities.combine_data_folder()
df = df[df['Year'] > 2003]   

# Add previous seed to df
previous_seeds_df = utilities.previous_seeds()
df = pd.merge(df, previous_seeds_df, how='outer', on=['Team', 'Year'])

# Set up training data
df_new = df.copy()
df_new = df_new[df_new['GS'] >= 41]
df_new = df_new[df_new['G'] > 65]
df_new = df_new[df_new['MP'] > 25]
df_new = df_new[df_new['MP'] * df_new['G'] > 41]
df_new['Log Share'] = np.log(df_new['Share'] + 1e-5)


# fit the Model
X = df_new[features]
y = df_new['Log Share']
model = XGBRegressor(objective='reg:squarederror', **params)
model.fit(X, y)

# Grab 2024-2025 
total = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2025_totals.html#totals_stats')[0]
advanced = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2025_advanced.html#advanced')[0]
team = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2025.html#advanced-team')

df_2025 = utilities.combine_tables(total, advanced, mvp=pd.DataFrame(), team=team)
df_2025 = df_2025[df_2025 ['GS'] >= 41]
df_2025 = df_2025[df_2025 ['G'] > 65]
df_2025 = df_2025[df_2025 ['MP'] > 25]
df_2025 = df_2025 [df_2025 ['MP'] * df_2025 ['G'] > 41]

# Predict using 2025 Data
pred = model.predict(df_2025[features])
df_copy = df_2025.copy()
df_copy['Predicted Share'] = pred

df_copy.sort_values(by='Predicted Share', ascending=False, inplace=True)

def add_win_prob_column(df, share_col='Predicted Share', prob_col='Win Probability'):
    shares = df[share_col].values
    exp_shares = np.exp(shares)
    probs = exp_shares / np.sum(exp_shares)
    df[prob_col] = probs * 100
    return df

add_win_prob_column(df_copy)

probability = df_copy.iloc[0]['Win Probability']
mvp = df_copy.iloc[0]['Player']
print(f'\033[1mThe Predicted 2025 NBA MVP is {mvp} with a {probability:.3f}% chance of winning.\033[1m')









