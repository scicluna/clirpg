class EventOutcome:
    def __init__(self, description: str, health_change=0, gold_change=0, item=None, special_effect=None):
        self.description = description
        self.health_change = health_change
        self.gold_change = gold_change
        self.item = item
        self.special_effect = special_effect

    def apply(self, player):
        """Apply the outcome to a player."""
        print(self.description)
        player.health += self.health_change
        player.gold += self.gold_change
        # Handle special_effect if needed
        # Handle item methods if needed


class Choice:
    def __init__(self, description: str, outcome: EventOutcome):
        self.description = description
        self.outcome = outcome


class Choices:
    def __init__(self, choices: list):
        self.choices = choices

    def display_choices(self):
        """Display all choices."""
        for index, choice in enumerate(self.choices):
            print(f"{index + 1}: {choice.description}")

    def choose(self, choice: int, player):
        """Apply the outcome of a choice."""
        self.choices[choice - 1].outcome.apply(player)
        print(f"{self.choices[choice - 1].description}")
