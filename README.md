# Nba-mvp-predictor
This is a data science project that uses NBA mvp and player data from 2004-2024 (20 seasons) to accurately predict who will be awarded mvp this year.

# Project Structure
```text
nba-mvp-predictor/
├── data/                # 2003-2024 directory to store webscraped files
├── model.ipynb          # Thought process and creation of XGBoostRegressor Model
├── utilites.py          # File containing huge functions to de-clutter other files
├── predict.py           # Final player prediction for 2025
├── webscrape.py         # Webscrapes 2003-2024 data from basketball reference
└── README.md            # This file
```
# Overview
This project uses XGBoost Regressor to predict MVP vote shares and simulate MVP rankings.  

It includes:  
- Historical MVP data (2004–2024)
- Feature engineering using advanced player stats (e.g. VORP, PER, WS/48)
- Time-series aware cross-validation
- Log Share and probability estimation
- MVP prediction for the current season (2024-2025)

# Model
Algorithm - XGBoostRegressor  
Target: MVP vote share (log-transformed)  
Features: VORP, W/L%, USG%, WS/48, PER, Seed  

# How to run
```
pip install -r requirements.txt
python predict.py
```

# Final Prediction
The Predicted 2025 NBA MVP is **Shai Gilgeous-Alexander** with a **46.132%** chance of winning.

# Features to Improve
- Better webscraping
- Experiment with potentially better models, i.e. NeuralNetworks
- Better Hyperparameter Tuning (RandomizedSearchCV / GridSearchCV)
- Player-level contextual embeddings
- Team-level adjustments for name changes or relocations
- Rank-based loss functions for better top-5 predictions

# Requirements
```
pip install -r requirements.txt
```

# Sources
- https://www.basketball-reference.com

# Contact
Maintained by Kevin Nguyen. Will improve this crappy model more in the future.


