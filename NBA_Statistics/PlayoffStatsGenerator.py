
#HEADER

import json
import re
import time
from datetime import date, timedelta

import Scraper_Master

import csv
from bs4 import BeautifulSoup, Comment

# First day of the playoffs
PLAYOFFS_START = date(2026, 4, 18)


def get_playoff_urls():
    """Scrape the basketball-reference boxscores listing for each playoff date
    and return a list of full box score URLs."""
    urls = []
    yesterday = date.today() - timedelta(days=1)
    current = PLAYOFFS_START

    while current <= yesterday:
        listing_url = (
            f"https://www.basketball-reference.com/boxscores/"
            f"?month={current.month}&day={current.day}&year={current.year}"
        )
        print(f"Fetching game list for {current}...")
        soup = Scraper_Master.Scrape_From_Source(listing_url)
        if soup == -1:
            print(f"  Failed to fetch listing for {current}, skipping")
        else:
            for gamelink_td in soup.find_all("td", class_="gamelink"):
                a = gamelink_td.find("a")
                if a and a.get("href"):
                    urls.append("https://www.basketball-reference.com" + a["href"])

        current += timedelta(days=1)
        time.sleep(5)

    print(f"Found {len(urls)} playoff game(s): {urls}")
    return urls

columns = ["Date", "Team", "Opponent", "Home(0)/Away(1)", "Margin", "Minutes", "FGA", "FGM", \
           "3PA", "3PM", "FT", "FTA", "ORB", "TRB", "Assists", "Steals", "Blocks", "Turnovers", "Fouls", "Points", "p/m"]

stats_data_stats = ["mp", "fga", "fg", "fg3a", "fg3", "ft", "fta", "orb", "trb", "ast", "stl", "blk", "tov", "pf", "pts", "plus_minus"]


def find_team_tables(soup):
    tables = soup.find_all("table", id=re.compile(r"^box-.+-game-basic$"))
    if tables:
        return tables

    # Tables are often inside HTML comments on basketball-reference
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        if "game-basic" in comment:
            comment_soup = BeautifulSoup(comment, "html.parser")
            tables.extend(comment_soup.find_all("table", id=re.compile(r"^box-.+-game-basic$")))

    return tables


def get_final_scores(soup):
    """Return (away_score, home_score) from the scorebox, or (None, None) on failure."""
    scorebox = soup.find("div", class_="scorebox")
    if not scorebox:
        return None, None
    scores = []
    for score_div in scorebox.find_all("div", class_="score"):
        try:
            scores.append(int(score_div.text.strip()))
        except ValueError:
            pass
    if len(scores) == 2:
        return scores[0], scores[1]
    return None, None


def parse_box_score(url, ref_by_path):
    """Scrape one box score URL. Returns {player_name: game_row_dict}."""

    # Parse date and home team from URL filename e.g. "202604190LAC"
    filename = url.split("/")[-1].replace(".html", "")
    date_str = f"{filename[:4]}-{filename[4:6]}-{filename[6:8]}"
    home_team = filename[-3:]

    soup = Scraper_Master.Scrape_From_Source(url)
    if soup == -1:
        print(f"Failed to fetch {url}")
        return {}

    team_tables = find_team_tables(soup)
    if len(team_tables) < 2:
        print(f"Could not find both team tables in {url}")
        return {}

    all_teams = [t["id"].split("-")[1] for t in team_tables]
    away_score, home_score = get_final_scores(soup)

    results = {}

    for table in team_tables:
        team_abbr = table["id"].split("-")[1]
        opp_abbr = [t for t in all_teams if t != team_abbr][0]
        is_away = 1 if team_abbr != home_team else 0

        if away_score is not None:
            if team_abbr == home_team:
                margin = home_score - away_score
            else:
                margin = away_score - home_score
        else:
            margin = ""

        for row in table.find_all("tr"):
            player_td = row.find(["th", "td"], {"data-stat": "player"})
            if player_td is None:
                continue

            if any(s in row.text for s in ["Did Not Play", "Inactive", "Player Suspended", "Did Not Dress", "Not With Team"]):
                continue

            player_link = player_td.find("a")
            if player_link is None:
                continue

            href = player_link["href"].replace(".html", "")
            player_name = ref_by_path.get(href)
            if player_name is None:
                print(f"  Player not in reference: {href} ({player_link.text})")
                continue

            game_row = {
                "Date": date_str,
                "Team": team_abbr,
                "Opponent": opp_abbr,
                "Home(0)/Away(1)": is_away,
                "Margin": margin,
            }

            for data_stat, col_name in zip(stats_data_stats, columns[5:]):
                td = row.find("td", {"data-stat": data_stat})
                val = td.text.strip() if td else ""

                if data_stat == "plus_minus":
                    val = val.replace("(", "").replace("+", "").replace(" ", "")
                elif data_stat == "mp" and ":" in val:
                    mins = val.split(":")
                    val = mins[0] + str(round(int(mins[1]) / 60, 2))[1:]

                game_row[col_name] = val

            results[player_name] = game_row

    return results


def Update_Player_Statistics():
    with open('NBA_Statistics/DailyPlayerReference.json', 'r', encoding='utf8') as f:
        player_reference = json.load(f)

    # Reverse lookup: url path -> player name
    ref_by_path = {v: k for k, v in player_reference.items()}

    all_player_stats = {}

    playoff_urls = get_playoff_urls()

    print("Beginning playoff box score scraping...")
    for url in playoff_urls:
        print(f"Scraping {url}...")
        game_data = parse_box_score(url, ref_by_path)
        for player_name, row in game_data.items():
            if player_name not in all_player_stats:
                all_player_stats[player_name] = []
            all_player_stats[player_name].append(row)
        time.sleep(12)

    for player_name, rows in all_player_stats.items():
        write_csv(player_name, rows)
        print(f"{player_name} Complete")

    print(f"Playoff scraping complete. {len(all_player_stats)} players written.")


def write_csv(name, rows):
    with open(f'NBA_Statistics/2026_play_off/{name}.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    Update_Player_Statistics()
