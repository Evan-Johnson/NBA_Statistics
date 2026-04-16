
#HEADER

import json
import time

import Scraper_Master

import csv
from bs4 import BeautifulSoup, Comment

# Play-in tournament start date — only rows on or after this date are kept
PLAY_IN_START = "2026-04-14"

def Update_Player_Statistics(year):

    player_stats = {}
    player_reference = {}

    with open('NBA_Statistics/DailyPlayerReference.json', 'r', encoding='utf8') as Player_Reference:
        player_reference = json.load(Player_Reference)

    player_limit = 0
    consecutive_failures = 0
    print("Beginning play-in player scraping...")

    for key in player_reference:
        url = "https://www.basketball-reference.com" + player_reference[key] + "/gamelog/" + str(year) + "/P/"

        columns = ["Date", "Team", "Opponent", "Home(0)/Away(1)", "Margin", "Minutes", "FGA", "FGM", \
               "3PA", "3PM", "FT", "FTA","ORB","TRB", "Assists", "Steals", "Blocks", "Turnovers", "Fouls", "Points", "p/m"]

        soup_columns = ["date", "team_name_abbr", "opp_name_abbr", "game_location", "game_result", "mp", "fga", "fg", \
                    "fg3a", "fg3", "ft", "fta","orb", "trb", "ast", "stl", "blk", "tov", "pf", "pts", "plus_minus"]

        player_soup = Scraper_Master.Scrape_From_Source(url)

        player_name = key

        player_data_all = []

        try:
            pgl_div = player_soup.find(name="div", attrs={"id": "all_player_game_log_playoffs"})
            if pgl_div is None:
                # Table may be inside an HTML comment — parse comments to find it
                for comment in player_soup.find_all(string=lambda text: isinstance(text, Comment)):
                    if "all_player_game_log_playoffs" in comment:
                        pgl_div = BeautifulSoup(comment, "html.parser").find(name="div", attrs={"id": "all_player_game_log_playoffs"})
                        break
            player_data_rows = pgl_div.findAll(name="tr")
        except AttributeError as e:
            print(player_name + " has no games found")
            consecutive_failures += 1
            if consecutive_failures >= 5:
                print(f"Rate limit detected ({consecutive_failures} consecutive failures) — taking a 10-minute break...")
                Scraper_Master.reset_scraper()
                time.sleep(600)
                consecutive_failures = 0
            continue

        consecutive_failures = 0

        for row in player_data_rows:

            date_td = row.find(name="td", attrs={"data-stat": "date"})
            if date_td is None or date_td.text.strip() == "":
                continue

            # Only keep play-in games
            if date_td.text.strip() < PLAY_IN_START:
                continue

            player_data_individual = {}

            index = 0

            for column in soup_columns:

                if("Did Not Play" in row.text or "Inactive" in row.text or "Player Suspended" in row.text or "Did Not Dress" in row.text or "Not With Team" in row.text):
                    break
                try:
                    player_data_cell_text = row.find(name="td", attrs = {"data-stat" : column}).text
                except:
                    print(row.text)

                if(column == "game_location"):
                    if(player_data_cell_text.strip() == ""):
                        player_data_cell_text = 0
                    else:
                        player_data_cell_text = 1

                elif(column == "game_result"):
                    try:
                        parts = player_data_cell_text.split(", ")
                        scores = parts[1].split("-")
                        player_data_cell_text = str(int(scores[0]) - int(scores[1]))
                    except:
                        player_data_cell_text = ""

                elif(column == "plus_minus"):
                    player_data_cell_text = player_data_cell_text.replace("(", "").replace("+", "").replace(" ", "")

                elif(column == "mp"):
                    if ':' in player_data_cell_text:
                        mins = player_data_cell_text.split(':')
                        mins[1] = str(round((int(mins[1]) / 60), 2))
                        player_data_cell_text = mins[0] + mins[1][1:]

                player_data_individual[columns[index]] = player_data_cell_text
                index += 1

            if(len(player_data_individual) > 0):
                player_data_all.append(player_data_individual)

        if len(player_data_all) == 0:
            print(player_name + " has no play-in games, skipping")
            player_limit += 1
            if (player_limit > 20):
                print("Taking a long break...")
                time.sleep(90)
                player_limit = 0
            time.sleep(12)
            continue

        player_stats[player_name] = player_data_all

        write_csv(player_name, columns, player_stats)

        print(player_name + " Complete")
        player_limit += 1
        if (player_limit > 20):
            print("Taking a long break...")
            time.sleep(90)
            player_limit = 0

        time.sleep(12)


def write_csv(name, columns, player_stats):
    with open('NBA_Statistics/2026_play_in/'+ name + '.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = columns)
        writer.writeheader()

        for games in player_stats[name]:
            writer.writerow(games)

        csvfile.close()



if __name__ == "__main__":
    Update_Player_Statistics(2026)
