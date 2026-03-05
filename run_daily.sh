#!/bin/bash

LOG_DIR="/Users/evanjohnson/Documents/personal/NBA_Statistics/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/run_$(date +%Y-%m-%d).log"

echo "=== NBA Daily Run: $(date) ===" >> "$LOG_FILE"

cd /Users/evanjohnson/Documents/personal/NBA_Statistics

# Run the scraper
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 NBA_Statistics/DailyController.py >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "Script failed, skipping git push." >> "$LOG_FILE"
    exit 1
fi

# Commit and push updated stats
git add NBA_Statistics/2026_player_data/ \
        NBA_Statistics/DailyPlayerReference.json \
        NBA_Statistics/DailyTeamReference.csv >> "$LOG_FILE" 2>&1

git diff --cached --quiet && echo "No changes to commit." >> "$LOG_FILE" && exit 0

git commit -m "Daily stats update: $(date +%Y-%m-%d)" >> "$LOG_FILE" 2>&1
git push origin master >> "$LOG_FILE" 2>&1

echo "Done." >> "$LOG_FILE"
