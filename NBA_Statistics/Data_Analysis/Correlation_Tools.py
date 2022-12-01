#Basic tools to determine the correlation between one or two variables
import Analysis_Tools as at

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
    

print(categoryToWin_PlayerCorrelation("Devin Booker", "Points", 40))