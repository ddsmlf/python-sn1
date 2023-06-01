from Classes.Dice import *
from Classes.Caracter import *
from termcolor import colored


class Monster(Caracter):
    type = "monster"

    def __init__(self, name, max_health, attack, defense, dice, level):
        super().__init__(name, max_health, attack, defense, dice)
        self.level = level

    def attack(self, target):
        attack_value = self.attack_value + self.level * 5
        damage = self.dice.roll() + attack_value - target.get_defense()
        if damage > 0:
            target.decrease_health(damage)
            print(f"{colored(target.get_name(), 'red')} takes {colored(damage, 'red')} damage!")
        else:
            print(f"{colored(target.get_name(), 'red')} blocks the attack!")
        return damage

    def set_level(self):
        pass
