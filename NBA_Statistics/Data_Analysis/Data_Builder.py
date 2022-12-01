# Contains helper functions for everything related to the building and managing of non-individual player data
import Analysis_Tools as at
import csv

#Builds/Updates allPlayerAverage.csv
def buildAllPlayerAverage(digits_to_round = 2):
    path = "../allPlayerAverage.csv"
    
    #taken from StatsGenerator (does not include non-numeric columns)
    columns = ["Name", "Margin", "Minutes", "FGA", "FGM", "3PA", "3PM", "Rebounds", "Assists", "Steals", "Blocks", "Turnovers", "Fouls", "Points"]
    
    playerNames = at.getPlayerNames()
    
    allPlayerAverage_dict = {}
    
    #feelin' loopy
    for name in playerNames:
        playerDataIndividual = {}
        for column in columns:
            
            if(column == "Name"):
                playerDataIndividual[column] = name
            else:
                average = at.getPlayerAverage(name, column, digits_to_round)
                playerDataIndividual[column] = average
        
        allPlayerAverage_dict[name] = playerDataIndividual
    
    with open(path, 'w', encoding='utf-8', newline='') as averageFile:
        averageFile.truncate(0)
        
        writer = csv.DictWriter(averageFile, fieldnames=columns)
        writer.writeheader()
        
        for name in playerNames:
            writer.writerow(allPlayerAverage_dict[name])

#Builds/Updates allPlayerTotal.csv
def buildAllPlayerTotal(digits_to_round = 2):
    path = "../allPlayerTotal.csv"
    
    #taken from StatsGenerator (does not include non-numeric columns)
    columns = ["Name", "Margin", "Minutes", "FGA", "FGM", "3PA", "3PM", "Rebounds", "Assists", "Steals", "Blocks", "Turnovers", "Fouls", "Points"]
    
    playerNames = at.getPlayerNames()
    
    allPlayerTotal_dict = {}
    
    #feelin' loopy
    for name in playerNames:
        playerDataIndividual = {}
        for column in columns:
            
            if(column == "Name"):
                playerDataIndividual[column] = name
            else:
                total = at.getPlayerTotal(name, column, digits_to_round)
                playerDataIndividual[column] = total
        
        allPlayerTotal_dict[name] = playerDataIndividual
    
    with open(path, 'w', encoding='utf-8', newline='') as totalFile:
        totalFile.truncate(0)
        
        writer = csv.DictWriter(totalFile, fieldnames=columns)
        writer.writeheader()
        
        for name in playerNames:
            writer.writerow(allPlayerTotal_dict[name])

#replaces all strings "subject" in player_data folder with string "target"
def replaceAllInPlayerData(subject, target):
    names = at.getPlayerNames()
    
    for name in names:
        path = "../player_data/" + name + ".csv"
        
        new_file_content = ""
        
        #read and create string with new file
        fin = open(path, "r+", encoding='utf8')
        
        for line in fin:
            stripped_line = line.strip()
            new_line = stripped_line.replace(subject, target).replace(" ", "")
            new_file_content += new_line + "\n"
        
        fin.close()
        
        #delete contents and write back
        fout = open(path, "w", encoding='utf8')
        
        fout.truncate(0)
        fout.write(new_file_content)
        fout.close()

