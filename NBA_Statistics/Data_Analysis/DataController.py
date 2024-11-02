import Data_Builder as db
import Plotting_Tools as pt

def BuildAll():
    db.buildAllPlayerAverage()
    db.buildAllPlayerTotal()

def PlotPlayer(name):
    pt.plotSinglePlayerThreeStats(name, "Points", "Assists", "TRB")

#BuildAll()
PlotPlayer("Devin Booker")