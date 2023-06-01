""" 
-------------------- GAME LAUCHER --------------------
"""

from Classes.Caracter import *
from Classes.Dice import *
from Classes.BattleRoyale import *
from Classes.SoloMode import *
from Classes.Shop import *
from termcolor import colored
import time
from ascii_magic import AsciiArt, Back
import json
from terminaltables import SingleTable
import keyboard
import os

class GameLauncher:
    def __init__(self):
        self.players = []
        self.players_in_game = []
        self.debug =  True
        self.battle_royale = BattleRoyale() 

    # ---------------------- Home page ------------------------
    def display_title(self):
            while True :     
                self.clear_screen()
                title_screen = AsciiArt.from_image('asset/kagnoca.jpg')
                title_screen.to_terminal(columns=170, width_ratio=2.5)
                title_screen = AsciiArt.from_image('asset/startscreen.jpg')
                print(colored(title_screen.to_ascii(columns=170, width_ratio=2), attrs=["blink"]))
                self.load_players()
                while True:
                    if keyboard.is_pressed("enter"):
                        self.clear_screen()
                        break
                    elif keyboard.read_key() is not "enter":
                        keyboard.press_and_release("\b")
                self.clear_screen()
                print(
                    f"\nPress {colored('i', 'light_blue')} to manage players, {colored('s', 'light_blue')} for shop or {colored('space', 'light_blue')} to start...\n")
                while True:
                    if keyboard.is_pressed("i"):
                        keyboard.press_and_release("\b")
                        self.clear_screen()
                        self.debug = True
                        self.select_players()  
                        break
                    if keyboard.is_pressed("s"):
                        keyboard.press_and_release("\b")
                        self.clear_screen()
                        boutique = Shop(self.players)
                        boutique.home_page()  
                        break
                    if keyboard.is_pressed(" "):
                        keyboard.press_and_release("\b")
                        self.clear_screen()
                        self.play_game()   
                        break
                    if keyboard.read_key() not in "i s":
                        keyboard.press_and_release("\b")


    # ---------------------- Clear the screen ------------------------
    def clear_screen(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            pass

    # ---------------------- Loading save players ------------------------
    def load_players(self):
        file_path = "data/game_state.json"
        try:
            with open(file_path, 'r') as file:
                player_data = json.load(file)

                for player_id, data in player_data.items():
                    player_type = data['type']
                    if player_type not in ['Mage', 'Thief', 'Warrior']:
                        raise ValueError('Invalid player type in file')

                    player_class = globals()[player_type]
                    player = player_class(
                        player_id,
                        data['max_health'],
                        data['attack'],
                        data['defense'],
                        Dice(data['dice-faces']),
                        data['total_exp']
                    )

                    player.health = data['health']
                    player.money = data['money']
                    player.inventory = data['inventory']
                    player.set_level()

                    self.players.append(player)
        except:
            print("No game saves found")

    # ---------------------- Create players ------------------------
    def display_player_creation(self, name=False):
        if not name:
            name = input(f"Choose a your name? ")
        valid_types = ["1", "2", "3"]
        player_type = ""
        while player_type not in valid_types:
            player_type = input(
                f"{colored(name, 'light_green')}, what type of character do you want to be? ({colored('1. warrior', 'light_red')}, {colored('2. mage', 'light_blue')}, {colored('3. thief', 'light_grey')}) ").lower()
            if player_type not in valid_types:
                print(
                    f"Invalid type. Please choose a valid number {colored('warrior', 'light_red')}, {colored('mage', 'light_blue')}, {colored('thief', 'light_grey')}.")

        if player_type == "1":
            self.players.append(Warrior(name, 20, 8, 3, Dice(6)))
        elif player_type == "2":
            self.players.append(Mage(name, 20, 8, 3, Dice(6)))
        elif player_type == "3":
            self.players.append(Thief(name, 20, 8, 3, Dice(6)))
        Caracter.save_game(self.players, "data/game_state.json")

    # ---------------------- Show table of players ------------------------
    def display_players(self):
        data = [
            [f"{colored('Name', 'light_green', attrs=['bold'])}", f"{colored('Type', 'light_grey', attrs=['bold'])}",
             f"{colored('Health', 'light_yellow', attrs=['bold'])}",
             f"{colored('Attack', 'light_red', attrs=['bold'])}", f"{colored('Defense', 'light_blue', attrs=['bold'])}",
             f"{colored('Level', 'light_magenta', attrs=['bold'])}", f"{colored('Exp', 'light_cyan', attrs=['bold'])}",
             f"{colored('Money', 'yellow', attrs=['bold'])}"]]
        for player in self.players:
            data.append(
                [player.name, player.get_type(), player.health, player.attack_value, player.defense_value, player.level,
                 player.total_exp, player.money])

        table = SingleTable(data)
        table.inner_row_border = True
        print(table.table)

    # ---------------------- Select / create / edit or delete players ------------------------
    def select_players(self, mode=True):
        self.display_players()

        # Select players for battle royal
        if mode == "1":
            self.players_in_game = []
            num_players = 0
            while not 2 <= num_players <= 6:
                try:
                    num_players = int(input("How many players? (2-6): "))
                except ValueError:
                    print("Invalid input. Please enter a number between 2 and 6.")

            print()
            while num_players > len(self.players):
                print("You have ", len(self.players), " players.\nPlease creacte ", num_players - len(self.players),
                      " more players !")
                self.display_player_creation()
                self.clear_screen()

            for x in range(num_players):
                for i, item in enumerate(self.players):
                    print(f"{colored(i + 1, 'light_blue')}. {item}")

                while True:
                    try:
                        selected = int(input(f"\nSelect player{x + 1} : ")) - 1
                        self.battle_royale.players_in_game.append(self.players[selected])
                        break
                    except:
                        print("Please enter a valid number")

        # Select players for solo mode
        elif mode == "2":     
            self.players_in_game = []
            for i, item in enumerate(self.players):
                print(f"{i + 1}. {item}")

            while True:
                try:
                    selected = int(input("\nSelect a player : ")) - 1
                    break
                except:
                    print("Please enter a valid number")

            self.players_in_game.append(self.players[selected])

        # Edit / create / delete players
        else:
            while True:
                print("Press X to escape\n")
                if self.debug:
                    player_name = input("")
                    self.debug = False
                player_name = input("Enter the name of a player to edit it or a new name to create one : ")
                index = None
                if player_name == "x" or player_name == "X":
                    break

                for i, player in enumerate(self.players):
                    if player.name == player_name:
                        index = i
                        while True:
                            print(player, "\n 1. Edit name\n 2. Delete\n 3. Return")
                            option = input("Select an option : ")
                            if option == "1":
                                new_name = input("New name : ")
                                player.name = new_name
                                Caracter.save_game(self.players, "data/game_state.json")
                                print("Saving successful !")
                                time.sleep(2)
                                self.clear_screen()
                                break
                            elif option == "2":
                                self.players.remove(player)
                                Caracter.save_game(self.players, "data/game_state.json")
                                print("Deleted successful !")
                                time.sleep(2)
                                self.clear_screen()
                                break
                            elif option == "3":
                                self.clear_screen()
                                break
                            else:
                                print("Please enter a valid value.\n")
                        continue
                # Create    
                if index is None:
                    self.display_player_creation(player_name)

                Caracter.save_game(self.players, "data/game_state.json")
                self.clear_screen()
                self.display_players()

    # ---------------------- Select game mode ------------------------
    def play_game(self):
        self.clear_screen()
        game_type = input(
            f"""
            {colored('1', 'light_blue')}. Battle Royale
            {colored('2', 'light_blue')}. Solo mode 
            {colored('3', 'light_blue')}. Return 
            Choose a game mode :""")
        if game_type == "1":
            print()
            print(f"{colored('BATTLE ROYALE', 'light_red', attrs=['blink'])}")
            self.select_players("1")
            self.battle_royale.battle_royale()
        elif game_type == "2":
            self.select_players("2")
            mode_solo = SoloMode(self.players_in_game[0])
            mode_solo.solo_mode()
        elif game_type == "3":
            self.clear_screen()
            self.display_title()
        else:
            print("Please enter a valid number")
            self.play_game()
