# Clash Royale Deck Tracker

A simple Python GUI application that allows you to view any player's current deck lineup DURING GAME in Clash Royale by searching for their name and clan.

## Features
- Search for players by name and clan
- Display current deck with card levels
- Clean and simple GUI interface

## Setup

1. Clone this repository
```bash
git clone https://github.com/johnnymartone/clash-royale-deck-tracker.git](https://github.com/johnnymartone/ClashRoyaleGameDeckTracker.git
cd clash-royale-deck-tracker
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Clash Royale API key:
```
CLASH_ROYALE_API_KEY=your_api_key_here
```

To get an API key:
1. Go to https://developer.clashroyale.com
2. Create an account and log in
3. Create a new API key
4. Add your IP address to the allowed IPs list

## Usage

Run the application:
```bash
python clash_royale_deck_tracker.py
```

1. Enter the player's name
2. Enter their clan name
3. Click "Search" to view their current deck

## Note
This tool requires a valid Clash Royale API key to function. Make sure you have added your API key to the `.env` file before running the application. 
