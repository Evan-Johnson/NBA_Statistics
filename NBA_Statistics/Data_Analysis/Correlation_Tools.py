#Basic tools to determine the correlation between one or two variables
import Analysis_Tools as at
import pandas as pd

#takes in playerName, category (C), and number (N) (optional win/loss, over/under, and dataframe)
#returns how many games a player has played where he has won/lossed a game
#and put up greater than/less than N in category C (i. e. < 5 assists, > 20 points)
def categoryToWin_PlayerTotal(playerName, C, N, over=True, win=True):
    df = at.getPlayerDataFrame(playerName)
    #convoluted but the best way to do it - let's count!
    if(win):
        if(over):
            return len(df.loc[(df[C] > N) & (df['Margin'] > 0)])
        else:
            return len(df.loc[(df[C] < N) & (df['Margin'] > 0)])
    else:
        if(over):
            return len(df.loc[(df[C] > N) & (df['Margin'] < 0)])
        else:
            return len(df.loc[(df[C] < N) & (df['Margin'] < 0)])
#EXAMPLE - prints number of times Devin Booker has lost while scoring over 20 points
#print(categoryToWin_PlayerTotal("Devin Booker", "Points", 20, over=True, win=False)
            
#same thing as categoryToWin_PlayerTotal, but returns dataframe instead of 
def categoryToWin_PlayerDataFrame(playerName, C, N, over=True, win=True):
    df = at.getPlayerDataFrame(playerName)
    #convoluted but the best way to do it - let's count!
    if(win):
        if(over):
            return df.loc[(df[C] > N) & (df['Margin'] > 0)]
        else:
            return df.loc[(df[C] < N) & (df['Margin'] > 0)]
    else:
        if(over):
            return df.loc[(df[C] > N) & (df['Margin'] < 0)]
        else:
            return df.loc[(df[C] < N) & (df['Margin'] < 0)]
#EXAMPLE - prints number of times Devin Booker has lost while scoring over 20 points
#print(categoryToWin_PlayerTotal("Devin Booker", "Points", 20, over=True, win=False)

#takes in playerName, category (C), and number (N) (optional win/loss, over/under)
#returns what percentage of games a player has played in and won/lossed
#and put up greater than/less than N in category C (i. e. < 5 assists, > 20 points)
#basedOnWins = what denominator to use. total games won = True, Total games played = False
def categoryToWin_PlayerCorrelation(playerName, C, N, over=True, win=True, basedOnWins=True):
    df = at.getPlayerDataFrame(playerName)
    
    totalPlayed = len(df)
    totalWins = len(df.loc[df['Margin'] > 0])
    totalWins_withParams=categoryToWin_PlayerTotal(playerName, C, N, over=over, win=win)
    
    if(basedOnWins):
        return totalWins_withParams/totalWins
    else:
        return totalWins_withParams/totalPlayed

#if devin booker averages 25 points per game over the reagular season how likely are they to make the playoffs?
#what are devin booker's averages when Kevin Durant is not playing?
def oneWithouttheOther(activePlayer, inactivePlayer):
    active_df = at.getPlayerDataFrame(activePlayer)
    inactive_df = at.getPlayerDataFrame(inactivePlayer)

    active_date_list = []
    inactive_date_list = []
    try:
        active_date_list = active_df['Date']
        inactive_date_list = inactive_df['Date']
    except:
        raise Exception("Could not find the dates played of the players...")
    
    print("nani?")
    date_list = list(set(active_date_list).difference(inactive_date_list))
    date_list = pd.to_datetime(date_list)
    active_df['Date'] = pd.to_datetime(active_df['Date'])

    rows = active_df.loc[active_df['Date'].isin(date_list)]
    print(rows)

#how does a player perform on the second day of a back to back
def backToBack(player):
    player_df = at.getPlayerDataFrame(player)

    player_df['Date'] = pd.to_datetime(player_df['Date'], errors='coerce')

    # Drop any rows with invalid dates (in case of parsing errors)
    player_df = player_df.dropna(subset=['Date'])

    # Sort by date
    player_df = player_df.sort_values(by='Date').reset_index(drop=True)

    # Create a shifted column for the previous date
    player_df['Prev_Date'] = player_df['Date'].shift(1)

    # Filter rows where the date is exactly one day after the previous date
    next_day_dates = player_df[player_df['Date'] - player_df['Prev_Date'] == pd.Timedelta(days=1)]
    

    rows = player_df.loc[player_df['Date'].isin(next_day_dates['Date'])]

    print(rows)

#backToBack('Michael Porter')
#backToBack('Nikola Jokić')
backToBack('Christian Braun')
#oneWithouttheOther('Ben Simmons', 'Cam Thomas')
    #date_list should contain all of the dates that one of the players played without the other.
    #still in the works for how we are going about this.
    



    

#print(categoryToWin_PlayerCorrelation("Devin Booker", "Points", 25))