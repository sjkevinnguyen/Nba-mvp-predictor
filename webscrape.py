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
mvp_url = "https://www.basketball-reference.com/awards/awards_{}.html"
player_url = "https://www.basketball-reference.com/awards/awards_{}.html"

# Create folders for data
os.mkdir('./mvp-data')
os.mkdir('./player-data')

# Webscrape NBA data, convert to csv, and place in appropriate folder
for year in years:
    df = pd.read_html(url, header=1, attrs={})
