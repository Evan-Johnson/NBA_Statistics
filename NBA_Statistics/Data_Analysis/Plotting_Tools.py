#Contains some basic plotting functions

import Analysis_Tools as at
import pandas as pd

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

plotSingleAxisTotal("Points")