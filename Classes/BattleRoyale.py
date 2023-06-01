from Classes.Caracter import *
from termcolor import colored
import time
import os


class BattleRoyale:
    def __init__(self):
        self.players_in_game = []

    # ---------------------- Battle royale ------------------------
    def battle_royale(self):
        self.clear_screen()
        num_players = len(self.players_in_game)
        current_player_index = 0
        while True:
            current_player = self.players_in_game[current_player_index]

            print()
            print(
                colored(f"Player {current_player_index + 1}: {current_player.get_name()} ({current_player.get_type()})",
                        'light_green'))
            input(f"{colored(current_player.get_name(), 'light_green')}, press Enter to take your turn...")

            target = self.choose_target(self.players_in_game)
            print(
                f"{colored(current_player.get_name(), 'light_green')} is attacking {colored(target.get_name(), 'red')}!")

            print("Rolling the dice...\n")
            time.sleep(2)
            attack_roll = current_player.attack(target)
            for player in self.players_in_game:
                player.show_health()

            print(f"{'_' * 100}")
            if self.is_game_over(self.players_in_game):
                print("Game over!")
                Caracter.save_game(self.players_in_game, "game_state.json")
                break
            current_player_index = (current_player_index + 1) % num_players

    # ---------------------- Choose target in battle royal mode ------------------------
    def choose_target(self, players):
        target = None
        while target is None:
            target_name = input("Choose a player to attack: ")
            for player in players:
                if player.get_name() == target_name:
                    target = player
                    break
            if target is None:
                print("Invalid player. Please choose a valid player.")
        return target

    # ---------------------- End of the game ------------------------
    def is_game_over(self, players):
        num_alive = 0
        for player in players:
            if player.is_alive():
                num_alive += 1
        return num_alive == 1

    # ---------------------- Clear the screen ------------------------
    def clear_screen(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            pass
