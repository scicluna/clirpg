from .gameelement import GameElement
from .choices import Choices
from ..entities.player import Player


class Event(GameElement):
    def __init__(self, description: str, choices: Choices, player: Player):
        self.description = description
        self.choices = choices
        self.player = player

    def trigger(self):
        # Present the event to the player
        print(self.description)
        self.choices.display_choices()
        self.resolve_choice()

    def resolve_choice(self):
        # Handle the outcome based on the player's choice
        while True:
            choice = input("Which choice do you make?")
            try:
                # Attempt to convert the choice to an integer
                choice_num = int(choice)

                # Check if the choice number is valid
                if choice_num not in range(1, len(self.choices.choices) + 1):
                    print(
                        f"Invalid choice. Please choose between 1 and {len(self.choices.choices)}.")
                else:
                    self.choices.choose(choice_num, self.player)
                    break

            except ValueError:
                # This block will execute if the conversion to int fails
                print("Invalid input. Please enter a number.")
