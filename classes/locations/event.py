from gameelement import GameElement


class Event(GameElement):
    def __init__(self, description, choices):
        self.description = description
        self.choices = choices  # This could be a dictionary mapping choices to outcomes

    def trigger(self):
        # Present the event to the player
        print(self.description)

    def resolve_choice(self, choice):
        # Handle the outcome based on the player's choice
        outcome = self.choices.get(choice)
        print(outcome)
