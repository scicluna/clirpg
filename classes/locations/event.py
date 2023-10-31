from gameelement import GameElement
from classes.locations.choices import Choices, Choice


class Event(GameElement):
    def __init__(self, description: str, choices: Choices, player):
        self.description = description
        self.choices = choices
        self.player = player

    def trigger(self):
        # Present the event to the player
        print(self.description)
        self.choices.display_choices()

    def resolve_choice(self, choice: int):
        # Handle the outcome based on the player's choice
        self.choices.choose(choice, self.player)
