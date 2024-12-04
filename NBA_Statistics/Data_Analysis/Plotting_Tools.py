#Contains some basic plotting functions

import Analysis_Tools as at
import pandas as pd
import matplotlib.pyplot as plt

#types of charts - taken from pd docs
#represents type_of_chart parameter
'''
The kind of plot to produce:

‘line’ : line plot (default)
‘bar’ : vertical bar plot ----> probably best for this type of plot
‘barh’ : horizontal bar plot
‘hist’ : histogram
‘box’ : boxplot
‘kde’ : Kernel Density Estimation plot
‘density’ : same as ‘kde’
‘area’ : area plot
‘pie’ : pie plot
‘scatter’ : scatter plot
‘hexbin’ : hexbin plot.
'''

#plots head/tail average of Y = category, X = name for any stat
#example:
#plotSingleAxisAverage("Assists", numNames = 10, type_of_chart="bar")
def plotSingleAxisAverage(Y, numNames = 10, head = True, sizeX = 10, sizeY = 10, type_of_chart = "bar"):
    dataframe = at.getAllPlayerAverageDataFrame().sort_values(Y, ascending = not head).head(numNames)
    dataframe.plot(x = "Name", y = Y, figsize = (sizeX, sizeY), kind = type_of_chart)


#plots head/tail total of Y = category, X = name for any stat
#example:
#plotSingleAxisTotal("Assists", numNames = 10, type_of_chart="bar")
def plotSingleAxisTotal(Y, numNames = 10, head = True, sizeX = 10, sizeY = 10, type_of_chart = "bar"):
    dataframe = at.getAllPlayerTotalDataFrame().sort_values(Y, ascending = not head).head(numNames)
    dataframe.plot(x = "Name", y = Y, figsize = (sizeX, sizeY), kind = type_of_chart)

#plot specific players stats for the season
def plotSinglePlayerStats(player_name, category_name, head = True, sizeY = 20, type_of_chart = "line"):
    dataframe = at.getPlayerDataFrame(player_name)
    category_data = dataframe[category_name]
    category_data.plot(x = "Games", y = category_name, figsize = (category_data.size, sizeY), kind = type_of_chart)

def plotSinglePlayerThreeStats(player_name, category_name1, category_name2, category_name3, head = True, sizeY = 20, type_of_chart = "line"):
    dataframe = at.getPlayerDataFrame(player_name)
    category_data1 = dataframe[category_name1]
    category_data2 = dataframe[category_name2]
    category_data3 = dataframe[category_name3]
    cat_arr = [category_data1, category_data2, category_data3]
    x_arr = []
    for i in range(category_data1.size):
        x_arr.append(i)

    labels = [category_name1, category_name2, category_name3]
    fig, ax = plt.subplots(
        figsize = (category_data1.size, sizeY)
    )
    for i, label in enumerate(labels):
        ax.plot(x_arr, cat_arr[i], label=label)
    
    ax.set_xlabel("Games")
    ax.set_ylabel("Stats")
    ax.legend()
    plt.title(player_name)
    plt.savefig('NBA_Statistics/NBA_Statistics/Data_Analysis/Plots/' + player_name + '.png')
    plt.show()


#plotSingleAxisTotal("Points")
#plt.show()
#plotSingleAxisAverage("Points")
#plt.show()
#plotSinglePlayerStats("Devin Booker", "Points")
plotSinglePlayerThreeStats("Devin Booker", "Points", "Assists", "TRB")
#plt.savefig('Plots/BookStats.png')

#plotSinglePlayerThreeStats("Nikola Jokić", "Points", "Assists", "TRB")
plotSinglePlayerThreeStats("Kevin Durant", "Points", "Assists", "TRB")
#plt.savefig('Plots/KDStats.png')