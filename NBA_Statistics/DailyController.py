import Daily_Scraper as ds
import DailyNameGenerator as dng
import DailyStatsGenerator as dsg
#import Data_Analysis.Data_Builder as db
from datetime import date, timedelta

days_before = 2

#Hoping this can just be ran instead of running each file one by one
def Daily_Running():
    ds.Get_Daily_Teams(days_before)
    print("Daily teams were received and saved.")
    dng.Update_Name_URLs()
    print("Player reference was updated.")
    dsg.Update_Player_Statistics(2025)
    print("Player statistics have been updated for " + str(date.today() - timedelta(days=days_before)))

    #update the allPlayer stat files from Data_Builder
    #db.buildAllPlayerAverage()
    #db.buildAllPlayerTotal()

    #wondering if this helps it not run twice...
    exit()

Daily_Running()