from Classes.Dice import *
from inspect import stack
from termcolor import colored
import json


class Caracter:
    type = "caracter"

    def __init__(self, name, max_health, attack, defense, dice, total_exp=0):
        self.levels = {20: 1, 50: 2, 100: 3, 175: 4, 250: 5, 350: 6, 500: 7, 750: 8, 1000: 9, 1500: 10, 2275: 11, 3000: 12,  3800: 13, 4900: 14, 6000: 15, 7500: 16, 9000: 17, 12000: 18, 18000: 19, 25000: 20}

        self.name = name
        self.max_health = max_health
        self.health = self.max_health
        self.attack_value = attack
        self.defense_value = defense
        self.dice = dice
        self.level = 0
        self.total_exp = total_exp
        self.set_level()
        self.power_unlocked = False
        self.description = "A character"

        # Ajout de l'argent et du sac à dos
        self.money = 0
        self.inventory = {}

    def __str__(self):
        return f"{colored(self.name, 'light_green')} the {colored(type(self).type, 'light_grey')} ({self.description}) is starting the fight with {colored(self.max_health, 'light_yellow')}hp ({colored(self.attack_value, 'light_red')} atk / {colored(self.defense_value, 'light_blue')} def)\n"

    def decrease_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def show_health(self):
        missing_health = self.max_health - self.health
        health_bar = f"{self.name} healthbar : [{'●' * self.health}{'○' * missing_health}] {self.health}/{self.max_health}hp\n"
        print(colored(health_bar, 'yellow'))

    def get_name(self):
        return self.name

    def get_type(self):
        return type(self).type

    def get_defense(self):
        return self.defense_value

    def set_level(self):
        for key in self.levels:
            if self.total_exp < key:
                self.level = self.levels[key]
                if stack()[1].function != "__init__" and stack()[1].function != "load_players":
                	self.level_up()
                break
        

    def compute_damages(self, roll, target):
        damages = roll + self.attack_value
        return damages

    def regenerate(self):
        self.health = self.max_health

    def attack(self, target):
        if self.is_alive():
            roll = self.dice.roll()
            damages = self.compute_damages(roll, target)
            print(
                f"⚔️ {colored(self.get_type(), 'light_green')} {colored(self.name, 'light_green')} attack with {colored(str(damages), 'blue')} damages (attack: {self.attack_value} + roll: {roll})")
            target.defend(damages)

    def compute_defense(self, roll, damages):
        return damages - roll - self.defense_value

    def defend(self, damages):
        roll = self.dice.roll()
        wounds = self.compute_defense(roll, damages)
        print(
            f"🛡️ {colored(self.get_type(), 'red')} {colored(self.name, 'red')} defend against {colored(str(damages), 'blue')} damages and take {colored(str(wounds), 'red')} wounds ({colored(str(damages), 'blue')} damages - {self.defense_value} defense - {roll} roll)")
        self.decrease_health(wounds)

        # Nouvelle méthode pour débloquer un pouvoir spécifique en fonction du type de personnage

    def unlock_power(self):
        self.power_unlocked = True
        print(f"{self.name} unlocked a new power !")

    # Nouvelle méthode pour augmenter le niveau et les statistiques en fonction du type de personnage
    def level_up(self):
        self.max_health += 5
        self.health = self.max_health
        self.attack_value += 2
        self.defense_value += 1
        self.show_level_up_message()

    def show_level_up_message(self):
        print(colored(f"{self.get_type()} {self.name} reached level {self.level}!", "green"))
        print(colored(f"{self.get_type()} {self.name} gained 5 max health (total: {self.max_health})", "green"))
        print(colored(f"{self.get_type()} {self.name} gained 2 attack points (total: {self.attack_value})", "green"))
        print(colored(f"{self.get_type()} {self.name} gained 1 defense point (total: {self.defense_value})", "green"))
        print(colored(f"{self.get_type()} {self.name} fully healed!", "green"))

    def save_game(characters, filename):
        data = {}
        for character in characters:
            data[character.name] = {
                "type": character.get_type(),
                "health": character.health,
                "max_health": character.max_health,
                "attack": character.attack_value,
                "defense": character.defense_value,
                "dice-faces": character.dice.faces,
                "total_exp": character.total_exp,
                "money": character.money,
                "inventory": character.inventory,
            }
        with open(filename, "w") as f:
            json.dump(data, f)


class Warrior(Caracter):
    type = "Warrior"

    # PAS MOYEN DE RÉUTILISER LE CONSTRUCTEUR DE CARACTER ?
    def __init__(self, name, max_health, attack, defense, dice, money=0, total_exp=0):
        super().__init__(name, max_health, attack, defense, dice, total_exp=0)
        self.money = money
        self.inventory = {}

    def __str__(self):
        return super().__str__() + f"Money: {self.money} gold\nInventory: {', '.join(self.inventory)}\n"

    def level_up(self):
        super().level_up()
        self.money += 10
        self.inventory.append("axe")

    def unlock_power(self):
        if self.level >= 5:
            print(colored("🎖️  Level 5 power unlocked: Whirlwind Strike ! 🌀", "green"))


class Mage(Caracter):
    type = "Mage"

    def __init__(self, name, max_health, attack, defense, dice, total_exp=0, money=0):
        super().__init__(name, max_health, attack, defense, dice, total_exp=0)
        self.money = money
        self.inventory = {}

    def __str__(self):
        return super().__str__() + f"Money: {self.money} gold\nInventory: {', '.join(self.inventory)}\n"

    def level_up(self):
        super().level_up()
        self.money += 5
        self.inventory.append("staff")

    def unlock_power(self):
        if self.level >= 5:
            print(colored("🎖️  Level 5 power unlocked: Fireball ! 🔥", "green"))

    def compute_defense(self, roll, damages):
        print("Bonus : Magic armor ! (-3 wournds)")
        return super().compute_defense(roll, damages) - 3


class Thief(Caracter):
    type = "Thief"

    def __init__(self, name, max_health, attack, defense, dice, total_exp=0, money=0):
        super().__init__(name, max_health, attack, defense, dice, total_exp=0)
        self.description = "A sneaky character, fast and precise in combat."
        self.money = 50
        self.inventory = {}

    def compute_damages(self, roll, target):
        print(f"Bonus : Backstab ! (+{target.get_defense()} damages)")
        return super().compute_damages(roll, target) + target.get_defense()

    def level_up(self):
        self.level += 1
        print(f"{self.name} reached level {self.level} !")
        self.max_health += 5
        self.health += 5
        self.attack_value += 2
        self.defense_value += 1
        print(f"{self.name} gained +5 max health, +5 current health, +2 attack, +1 defense.")

    def unlock_power(self):
        if self.level >= 3:
            print(f"{self.name} unlocked the power to throw a smoke bomb !")
            print("The smoke bomb blinds the enemy for one turn, preventing them from attacking.")
        else:
            print(f"{self.name} is not high enough level to unlock a power yet.")


if __name__ == "__main__":
    a_dice = Dice(6)

    car1 = Warrior("Mike", 20, 8, 3, a_dice)
    car2 = Mage("Helen", 20, 8, 3, a_dice)
    car3 = Thief("Robin", 20, 8, 3, a_dice)
    print(car1)
    print(car3)

    while (car1.is_alive() and car3.is_alive()):
        car1.attack(car3)
        car3.attack(car1)

    car3.level_up()
    car3.unlock_power()
