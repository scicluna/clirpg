from gameelement import GameElement
from classes.locations.choices import Choices, Choice


class Event(GameElement):
    def __init__(self, description: str, choices: Choices):
        self.description = description
        self.choices = choices

    def trigger(self):
        # Present the event to the player
        print(self.description)

    def resolve_choice(self, choice: Choice):
        # Handle the outcome based on the player's choice
        outcome = self.choices.get(choice).outcome
        print(outcome)
