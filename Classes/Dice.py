import random


class Dice():
    type = "dice"

    def __init__(self, faces=6):
        self.faces = faces

    def roll(self):
        return random.randint(1, self.faces)

    def __str__(self):
        return f"I'm a {self.faces} faces {type(self).type}"


