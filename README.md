# Hololive Card Collector

This script collects card data from the Hololive Official Card Game website and stores it in JSON format.

## Features

- Automatically fetches all card data from the website
- Stores data in JSON format
- Checks for new cards hourly
- Maintains existing data and only updates when new cards are found
- Includes error handling and logging

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the script:
```bash
python card_collector.py
```

## Output

The script creates two main files:
- `card_data.json`: Contains all the collected card data
- `card_collector.log`: Contains logging information about the script's execution

The script runs continuously and checks for new cards every hour. You can modify the schedule in the script if you want to change the frequency.
