
#HEADER

import json
import time

import Scraper_Master

import csv

def Update_Player_Statistics(year):
    
    player_stats = {}
    player_reference = {}
    
    
    with open('NBA_Statistics/DailyPlayerReference.json', 'r', encoding='utf8') as Player_Reference:
        player_reference = json.load(Player_Reference)

    
    urls = []
    player_limit = 0
    print("Beginning player scraping...")
    
    for key in player_reference:
        url = "https://www.basketball-reference.com" + player_reference[key] + "/gamelog/" + str(year) + "/"

        columns = ["Date", "Team", "Opponent", "Home(0)/Away(1)", "Margin", "Minutes", "FGA", "FGM", \
               "3PA", "3PM", "FT", "FTA","ORB","TRB", "Assists", "Steals", "Blocks", "Turnovers", "Fouls", "Points", "p/m"]
    
        soup_columns = ["date_game", "team_id", "opp_id", "game_location", "game_result", "mp", "fga", "fg", \
                    "fg3a", "fg3", "ft", "fta","orb", "trb", "ast", "stl", "blk", "tov", "pf", "pts", "plus_minus"]
    
        player_soup = Scraper_Master.Scrape_From_Source(url)
        
        player_name = key
        
        player_data_all = []
        
        try:
            player_data_rows = player_soup.find(name="div", attrs = {"id": "all_pgl_basic"}).findAll(name="tr")
        except AttributeError as e:
            print(player_name + " has no games found")
            continue
        
        for row in player_data_rows:
            
            if("Rk" in row.text):
                continue
            
            player_data_individual = {}
            
            index = 0
            
            for column in soup_columns:
                
                #clean out header rows
                if("Did Not Play" in row.text or "Inactive" in row.text or "Player Suspended" in row.text or "Did Not Dress" in row.text or "Not With Team" in row.text):
                    break    
                try:
                    player_data_cell_text = row.find(name="td", attrs = {"data-stat" : column}).text
                except:
                    print(row.text)
                
                #little adjustments to specific columns
                if(column == "game_location"):
                    if(player_data_cell_text == ""):
                        player_data_cell_text = 0
                    else:
                        player_data_cell_text = 1
                
                elif(column == "game_result"):
                    player_data_cell_text = player_data_cell_text[1:-1]
                    #this is certainly annoying to look at
                    player_data_cell_text = player_data_cell_text.replace("(", "").replace("+", "").replace(" ", "")
                    
                elif(column == "plus_minus"):
                    #this is certainly annoying to look at
                    player_data_cell_text = player_data_cell_text.replace("(", "").replace("+", "").replace(" ", "")
                
                elif(column == "mp"):
                    mins = player_data_cell_text.split(':')
                    mins[1] = str(round((int(mins[1]) / 60), 2))
                    player_data_cell_text = mins[0] + mins[1][1:]
                
                player_data_individual[columns[index]] = player_data_cell_text
                index += 1
            
            if(len(player_data_individual) > 0):
                player_data_all.append(player_data_individual)
        
        player_stats[player_name] = player_data_all
        
        write_csv(player_name, columns, player_stats)
        
        print(player_name + " Complete")
        player_limit += 1
        if (player_limit > 30):
            print("Taking a long break...")
            time.sleep(30)
            player_limit = 0
        
        time.sleep(5.5)
        
        
def write_csv(name, columns, player_stats):
    with open('NBA_Statistics/2025_player_data/'+ name + '.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = columns)
        writer.writeheader()
    
        for games in player_stats[name]:
            writer.writerow(games)
            
        csvfile.close()
        


Update_Player_Statistics(2025)