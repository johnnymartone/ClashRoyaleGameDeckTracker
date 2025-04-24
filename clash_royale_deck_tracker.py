import tkinter as tk
from tkinter import Entry, Button, ttk
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('CLASH_ROYALE_API_KEY')
if not api_key:
    raise ValueError("Please set CLASH_ROYALE_API_KEY in your .env file")

headers = {
    'Authorization': f'Bearer {api_key}',
}

def searchForClan(name):
    params = {
        'name': name,
    }

    response = requests.get('https://api.clashroyale.com/v1/clans', params=params, headers=headers)
    r = response.json()
    possibleClans = []
    for clan in r.get("items", []):
        if clan["name"].lower() == name.lower():
            possibleClans.append(clan["tag"][1:])
            
    return possibleClans

def getClanMembers(tag):
    response = requests.get(f"https://api.clashroyale.com/v1/clans/%23{tag}/members", headers=headers)
    return response.json().get("items", [])

def getPlayerByTag(tag):
    response = requests.get(f"https://api.clashroyale.com/v1/players/%23{tag[1:]}", headers=headers)
    return response.json()

def searchForPlayerTag(name, clanName):
    clans = searchForClan(clanName)
    for clanTag in clans:
        members = getClanMembers(clanTag)
        for member in members:
            if member["name"].lower() == name.lower():
                return member["tag"]
    return None

def getPlayerDeck(tag):
    player = getPlayerByTag(tag)
    return player.get("currentDeck", [])

def getPlayerDeckFromData(name, clanName):
    playerTag = searchForPlayerTag(name, clanName)
    if playerTag:
        return getPlayerDeck(playerTag)
    return None

class ClashRoyaleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Clash Royale Deck Tracker")

        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 14))
        style.configure('TFrame', background='#f0f0f0')

        main_container = ttk.Frame(master, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.label_name = ttk.Label(main_container, text="Player Name:")
        self.entry_name = ttk.Entry(main_container, width=40, font=('Arial', 12))
        
        self.label_clan = ttk.Label(main_container, text="Clan Name:")
        self.entry_clan = ttk.Entry(main_container, width=40, font=('Arial', 12))
        
        self.btn_search = ttk.Button(main_container, text="Search", command=self.search_player_deck)
        
        self.result_frame = ttk.Frame(main_container, borderwidth=2, relief="solid", padding="10")

        self.label_name.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)
        self.label_clan.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_clan.grid(row=1, column=1, padx=5, pady=5)
        self.btn_search.grid(row=2, column=0, columnspan=2, pady=10)
        self.result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

    def search_player_deck(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        name = self.entry_name.get()
        clan = self.entry_clan.get()

        if not name or not clan:
            self.show_error("Please enter both player name and clan name")
            return

        try:
            player_deck = getPlayerDeckFromData(name, clan)

            if player_deck:
                self.display_deck(player_deck)
            else:
                self.show_error("Player not found or deck not available")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def display_deck(self, deck):
        items_per_row = 4
        for i, card in enumerate(deck):
            row = i // items_per_row
            col = i % items_per_row
            
            card_frame = ttk.Frame(self.result_frame, borderwidth=1, relief="solid")
            card_frame.grid(row=row, column=col, padx=5, pady=5)
            
            level = card['level'] + (14 - card['maxLevel'])
            ttk.Label(
                card_frame,
                text=f"{card['name']}\nLevel {level}",
                justify=tk.CENTER
            ).pack(padx=5, pady=5)

    def show_error(self, message):
        error_label = ttk.Label(
            self.result_frame,
            text=message,
            foreground='red'
        )
        error_label.grid(row=0, column=0, columnspan=4, pady=10)

def main():
    root = tk.Tk()
    root.title("Clash Royale Deck Tracker")
    app = ClashRoyaleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 