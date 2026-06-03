import Daily_Scraper as ds
import DailyNameGenerator as dng
import PlayoffStatsGenerator as posg
from datetime import date, timedelta

def Daily_Running():
    last_scraped = posg.get_last_scraped_date()
    start_date = last_scraped + timedelta(days=1)
    yesterday = date.today() - timedelta(days=1)

    if start_date > yesterday:
        print("Already up to date, nothing to do.")
        exit(0)

    print(f"Scraping from {start_date} to {yesterday}...")

    ds.Get_Teams_Date_Range(start_date)
    print("Daily teams were received and saved.")
    dng.Update_Name_URLs()
    print("Player reference was updated.")
    posg.Update_Player_Statistics()
    print("Playoff statistics have been updated for " + str(yesterday))

    exit(0)

Daily_Running()
