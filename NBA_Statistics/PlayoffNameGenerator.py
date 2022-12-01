#This script will generate the urls of all current players in the NBA
#and push them to a text document. Stored as dictionaries containing
#{name: url, name : url, etc.}
#url is to basketball-reference.com

import Scraper_Master
import csv
import json

def Update_Name_URLs():
    
    #init datasets for later use
    teams = []
    name_urls = {} #used for final printing
    
    #get team names via TeamReference.csv
    with open('PlayoffTeamReference.csv', newline = '') as team_file:
        
        reader = csv.reader(team_file)
        
        for elem in reader:
            teams.append(elem[0])
    
    #create list for return
    for team in teams:
        
        print(team)
        
        url = 'https://www.basketball-reference.com/teams/' + team + '/2021.html'
        
        #see documentation in Scraper_Master.py
        #basically team_soup = beautifulsoup object from url above
        team_soup = Scraper_Master.Scrape_From_Source(url)
        
        player_td = team_soup.find_all(attrs={"data-stat":"player"})

        for player in player_td:
            
            url_name_tag = player.find(name='a')
            
            #Ignore column headers (<a> without href links)
            if(url_name_tag != None):
                name = url_name_tag.text.split(" ")[0] + " " + url_name_tag.text.split(" ")[1]
                
                href = url_name_tag['href'].replace(".html", "")
                
                #add to dictionary
                if(href not in name_urls.values()):
                    name_urls[name] = href
    
    #write file contents to json
    
    #clear contents first to avoid dangling data upon update
    #additionally if json file does not exist, create empty json
    player_reference_clear = open('PlayoffPlayerReference.json', 'w')
    player_reference_clear.close()
    
    with open('PlayoffPlayerReference.json', 'w', encoding='utf8') as player_file:
        
        #I used dumps instead of dump to ensure ASCII characters
        player_string = json.dumps(name_urls, ensure_ascii = False)
        
        #the only caveaut to using dumps it the fact that it creates a string,
        #so it is unable to beautify the json. Easily fixed.
        
        player_string = player_string.replace(",", ",\n\t")
        player_string = player_string.replace("{", "{\n\t")
        player_string = player_string.replace("}", "\n}")
        
        player_file.write(player_string)

Update_Name_URLs()
        