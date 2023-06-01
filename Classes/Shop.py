from termcolor import colored
import os
import keyboard


class Shop:
    def __init__(self, players):
        self.weapons = {"sword": 100, "bow": 80, "staff": 120}
        self.potions = {"healing": 50, "mana": 40, "antidote": 30}
        self.armors = {"leather": 150, "chainmail": 200, "plate": 250}
        self.food = {"bread": 5, "cheese": 10, "meat": 15}
        self.items = {"weapons": self.weapons, "potions": self.potions, "armors": self.armors, "food": self.food}
        self.players = players

    # ---------------------- Clear the screen ------------------------
    def clear_screen(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            pass

    def home_page(self):
        self.clear_screen()
        print("Welcome to the shop!\n")
        print("Categories:")
        for i, category in enumerate(self.items):
            print(f"{colored(i + 1, 'light_blue', attrs=['bold'])}. {category.title()}")
        print(f"Enter {colored('X', 'light_blue', attrs=['bold'])} to leave the shop\n")
        while True:
            choice = input("Select a category: ")
            if choice.lower() == "x":
                return
            try:
                category_num = int(choice) - 1
                if category_num < 0 or category_num >= len(self.items):
                    raise ValueError
            except ValueError:
                print("Invalid input. Please enter a number or X.")
            else:
                category = list(self.items.keys())[category_num]
                self.article_page(category)

    def article_page(self, category):
        self.clear_screen()
        print(f"\n{category.title()}:\n")
        for i, item in enumerate(self.items[category]):
            print(
                f"{colored(i + 1, 'light_blue', attrs=['bold'])}. {colored(item.title(), 'light_grey', attrs=['bold'])} - {colored(self.items[category][item], 'light_yellow', attrs=['bold'])} gold")
        print(f"Enter {colored('X', 'light_blue', attrs=['bold'])} to go back\n")

        while True:
            choice = input("Select an item: ")
            if choice.lower() == "x":
                return
            try:
                item_num = int(choice) - 1
                if item_num < 0 or item_num >= len(self.items[category]):
                    raise ValueError
            except ValueError:
                print("Invalid input. Please enter a number or X.")
            else:
                item = list(self.items[category].keys())[item_num]
                self.clear_screen()
                self.purchase_page(category, item)

    def purchase_page(self, category, item):
        item_price = self.items[category][item]
        item_name = item.title()
        item_category = ""
        if category == "weapons":
            item_category = "weapon"
        elif category == "armors":
            item_category = "armor"
        else:
            item_category = category[:-1]
        print(
            f"\n{colored(item_name, 'light_grey', attrs=['bold'])} - {colored(item_price, 'light_yellow', attrs=['bold'])} gold\n")
        print(f"Enter {colored('X', 'light_blue', attrs=['bold'])} to go back\n")

        while True:
            choice = input(
                f"Do you want to buy this item? ({colored('Y', 'light_green', attrs=['bold'])}/{colored('N', 'light_red', attrs=['bold'])}): ")
            if choice.lower() == "y":
                player_choice = None
                while player_choice not in range(len(self.players)):
                    print("\nSelect a player:")
                    for i, player in enumerate(self.players):
                        print(f"{i + 1}. {player.name}")
                    try:
                        player_choice = int(input()) - 1
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
                    if player_choice not in range(len(self.players)):
                        print("Invalid input. Please enter a valid number.")
                        continue
                    selected_player = self.players[player_choice]

                item_quantity = None
                while item_quantity is None or item_quantity < 1:
                    try:
                        item_quantity = int(input("Enter the quantity: "))
                    except ValueError:
                        print("Invalid input. Please enter a number greater than 0.")
                        continue
                    if item_quantity < 1:
                        print("Invalid input. Please enter a number greater than 0.")
                        continue
                    if item_quantity * self.items[category][item]:
                        print("Invalid input. Please enter a valid quantity.")
            elif choice.lower() == "n":
                self.home_page()

            # Check if player has enough money to make the purchase
            total_price = item_quantity * item_price
            if selected_player.money < total_price:
                print(
                    f"You don't have enough money to purchase {colored(item_quantity, light_cyan, attrs=['bold'])} {colored(item_name, 'light_grey', attrs=['bold'])}.")
            else:
                # Prompt player to confirm purchase
                print(
                    f"The total cost of {colored(item_quantity, 'light_red', attrs=['bold'])} {colored(item_name, 'light_grey', attrs=['bold'])} is {colored(total_price, 'light_yellow', attrs=['bold'])} gold coins.")
                confirm_purchase = input(
                    f"Do you want to confirm this purchase? ({colored('Y', 'light_green', attrs=['bold'])}/{colored('N', 'light_red', attrs=['bold'])})").lower()
                if confirm_purchase == "y":
                    # Deduct money from player's balance
                    selected_player.money -= total_price
                    print(f"Transaction successful. You now have {selected_player.money} gold coins.")

                    # Add purchased item(s) to player's inventory
                    if item_category in ["weapons", "armor"]:
                        # If item is a weapon or armor, check if player already has one equipped
                        for inventory_item in selected_player.inventory:
                            if isinstance(inventory_item, type(item)):
                                print("You already have a similar item equipped.")
                                break
                        else:
                            selected_player.inventory.append(item)
                            print(f"{item_name} added to your inventory.")
                    else:
                        # For potions and food, just add to inventory
                        for i in range(item_quantity):
                            selected_player.inventory.append(item)
                        print(f"{item_quantity} {item_name} added to your inventory.")
                else:
                    print("Transaction canceled.")


if __name__ == "__main__":
    boutique = Shop(["test", "test"])
    boutique.home_page()
