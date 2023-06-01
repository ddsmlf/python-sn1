from Classes.Caracter import Caracter
from Classes.Monster import Monster
from termcolor import colored
import time
import os

class SoloMode:
    def __init__(self, player):
        self.player = player
        self.clear_screen()

    def solo_mode(self):
        monster_level = self.player.level
        while True:
            monster = Monster(f"Monster {monster_level}", self.player.max_health, self.player.attack_value, self.player.defense_value, self.player.dice, self.player.total_exp)
            print(f"A level {colored(monster_level, 'red')} {colored(type(monster).type, 'red')} appears!\n")
            time.sleep(2)

            while self.player.is_alive() and monster.is_alive():
                self.show_game_status(self.player, monster)
                self.player_turn(monster)
                if not monster.is_alive():
                    break
                self.monster_turn(monster, self.player)
            if self.player.is_alive():
                self.player_gain_exp(monster)
                self.player_gain_money(monster)
                self.clear_screen()
                print(f"You defeated the level {colored(monster_level, 'red')} {colored(type(monster).type, 'red')}!\n")
                monster_level += 1
            else:
                self.game_over()
                break

    def show_game_status(self, player, monster):
        self.clear_screen()
        print(player)
        player.show_health()
        print(monster)
        monster.show_health()

    def player_turn(self, monster):
        input(f"{colored(self.player.name, 'light_green')}, press Enter to take your turn...")
        attack_roll = self.player.attack(monster)
        print(f"{colored(self.player.name, 'light_green')} attacks {colored(type(monster).type, 'red')} with a roll of {colored(attack_roll, 'yellow')}")
        time.sleep(1)

    def monster_turn(self, monster, player):
        attack_roll = monster.attack(player)
        print(f"{colored(type(monster).type, 'red')} attacks {colored(player.name, 'light_green')} with a roll of {colored(attack_roll, 'yellow')}")
        time.sleep(1)

    def player_gain_exp(self, monster):
        exp_gained = monster.get_exp()
        self.player.total_exp += exp_gained
        print(f"{colored(self.player.name, 'light_green')} gains {colored(exp_gained, 'green')} experience points!")
        time.sleep(1)
        if self.player.level_up():
            print(f"{colored(self.player.name, 'light_green')} is now level {colored(self.player.level, 'red')}!\n")
            time.sleep(1)

    def player_gain_money(self, monster):
        money_gained = monster.get_money()
        self.player.money += money_gained
        print(f"{colored(self.player.name, 'light_green')} gains {colored(money_gained, 'green')} coins!")
        time.sleep(1)

    def game_over(self):
        print("You are defeated...")
        time.sleep(1)

    def clear_screen(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            pass
