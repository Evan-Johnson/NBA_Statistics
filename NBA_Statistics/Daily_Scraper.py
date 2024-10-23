import json
import time
from datetime import date

import Scraper_Master

import csv

print()

def Get_Daily_Teams():
    
    player_reference = {}
    url = "https://www.basketball-reference.com/boxscores/index.fcgi?month=10&day=22&year=2024"

    team_soup = Scraper_Master.Scrape_From_Source(url)
    #<th scope="row" class="left " data-stat="date_game" csk="202410220BOS"><a href="/boxscores/index.fcgi?month=10&amp;day=22&amp;year=2024">Tue, Oct 22, 2024</a></th>




#Get_Daily_Teams(date.today().strftime("%B").lower())