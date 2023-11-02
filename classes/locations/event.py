from .gameelement import GameElement
from .choices import Choices
from ..entities.player import Player


class Event(GameElement):
    def __init__(self, description: str, choices: Choices, player: Player):
        self.description = description
        self.choices = choices
        self.player = player
        self.completed = False

    def trigger(self):
        # Present the event to the player
        print(self.description)
        self.choices.display_choices()
        self.resolve_choice()

    def resolve_choice(self):
        """Resolves the player's choice."""
        while True:
            choice = input("Which choice do you make?")
            try:
                choice_num = int(choice)

                if choice_num not in range(1, len(self.choices.choices) + 1):
                    print(
                        f"Invalid choice. Please choose between 1 and {len(self.choices.choices)}.")
                else:
                    outcome = self.choices.choose(choice_num, self.player)
                    if not outcome.incomplete:
                        self.completed = True
                    break

            except ValueError:
                # This block will execute if the conversion to int fails
                print("Invalid input. Please enter a number.")
