import json
import time
from datetime import date, timedelta

import Scraper_Master

import csv

print(date.today().day)

def Get_Daily_Teams():
    
    team_reference = []
    #test url with two games... 4 teams
    #url = "https://www.basketball-reference.com/boxscores/?month=10&day=23&year=2024"
    #real url going forward will be this (games that happened yesterday):
    today = date.today()
    yesterday = today - timedelta(days=2)
    print("Yesterday was: " + str(yesterday))
    url = "https://www.basketball-reference.com/boxscores/index.fcgi?month=" + str(yesterday.month) + "&day=" + str(yesterday.day) + "&year=" + str(yesterday.year)
    
    print(url)
    team_soup = Scraper_Master.Scrape_From_Source(url)

    team_rows = team_soup.find(name = "div", attrs = {"id": "content"}).findAll(name = "tr", class_=lambda x: x and any(c in x.split() for c in ["winner", "loser"]))
    
    #cleaning up the saved html to get the 3 letter team names
    for row in team_rows:
        team = str(row.contents[1].contents[0])
        #<a href="/teams/NYK/2025.html">New York</a>
        team = team[16:]
        team = team[:3]
        #team now stores str like "NYK"
        team_reference.append(team)

    with open('NBA_Statistics/NBA_Statistics/DailyTeamReference.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for teams in team_reference:
            writer.writerow([teams])
        

        csvfile.close()

Get_Daily_Teams()